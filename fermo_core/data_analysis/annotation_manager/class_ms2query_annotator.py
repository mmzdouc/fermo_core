"""Runs the ms2query library annotation module.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import contextlib
import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Self

import func_timeout
import pandas as pd
from matchms.exporting import save_as_mgf
from ms2query.ms2library import MS2Library, create_library_object_from_one_dir
from ms2query.run_ms2query import run_complete_folder
from ms2query.utils import SettingsRunMS2Query
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Match,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager

logger = logging.getLogger("fermo_core")


class MS2QueryAnnotator(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2query lib matching

    Attributes:
        features: Repository object, holds "General Feature" objects
        params: User-provided parameters
        active_features: a set of active features
        cutoff: a float between 0 and 1 indicating the minimum accepted score
        queries: a list of Spectra for which to perform matching
    """

    features: Repository
    params: ParameterManager
    active_features: set
    cutoff: float
    queries: Optional[list] = None

    def return_features(self: Self) -> Repository:
        """Return the modified Feature objects as Repository object

        Returns:
            A Repository object with modified Feature objects
        """
        return self.features

    def prepare_queries(self: Self):
        """Prepare a filtered list of query spectra for matching

        Raise:
            RuntimeError: no query spectra collected (empty list)
        """
        query_spectra = []

        for f_id in self.active_features:
            feature = self.features.get(f_id)
            if feature.Spectrum is None or len(feature.Spectrum.peaks.mz) == 0:
                logger.debug(
                    f"'AnnotationManager/MS2QueryAnnotator': feature with id "
                    f"'{feature.f_id}' has no associated MS2 spectrum - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)

        if len(query_spectra) != 0:
            self.queries = query_spectra
            return
        else:
            raise RuntimeError(
                "'AnnotationManager/MS2QueryAnnotator': no query spectra qualify for "
                "matching - SKIP"
            )

    def estimate_calc_time(self: Self):
        """Estimates the approximate calculation time and aborts if set time too low

        Raises:
            RuntimeError: no query spectra collected (None) or runtime too short
        """
        if self.queries is None:
            raise RuntimeError(
                "'AnnotationManager/MS2QueryAnnotator': 'self.queries' is None."
                "Did you run 'self.prepare_queries()'?"
            )

        if self.params.Ms2QueryAnnotationParameters.maximum_runtime != 0 and (
            (len(self.queries) * 2.5)
            > self.params.Ms2QueryAnnotationParameters.maximum_runtime
        ):
            raise RuntimeError(
                f"'AnnotationManager/MS2QueryAnnotator': Estimated runtime of "
                f"MS2Query for the "
                f"annotation of "
                f"'{len(self.queries)}' features is '{len(self.queries) * 2.5}' "
                f"seconds. This exceeds the maximum allowed runtime of "
                f"'{self.params.Ms2QueryAnnotationParameters.maximum_runtime}' "
                f"seconds. Please increase the 'max_runtime' parameter or set to "
                f"'0' for unlimited runtime - SKIP"
            )

    def create_ms2query_dirs(self: Self):
        """Create ms2query helper directories in results dir"""
        self.params.OutputParameters.directory_path.joinpath(
            "temp_ms2query_queries"
        ).mkdir(exist_ok=True)

    def remove_ms2query_temp_files(self: Self):
        """Remove queries files to clean up before run"""
        with contextlib.suppress(FileNotFoundError):
            os.remove(
                self.params.OutputParameters.directory_path.joinpath(
                    "temp_ms2query_queries/f_queries.mgf"
                )
            )

        with contextlib.suppress(FileNotFoundError):
            os.remove(
                self.params.OutputParameters.directory_path.joinpath(
                    "temp_ms2query_queries/f_queries.csv"
                )
            )

    def remove_temp_ms2query_dirs(self: Self):
        """Remove temporary ms2query files after run"""
        self.remove_ms2query_temp_files()
        tempdir = self.params.OutputParameters.directory_path.joinpath(
            "temp_ms2query_queries"
        )
        if tempdir.exists():
            tempdir.rmdir()

    def move_ms2query_results(self: Self):
        """Copies the written ms2query.csv results from the temp folder"""
        src = self.params.OutputParameters.directory_path.joinpath(
            "temp_ms2query_queries/f_queries.csv"
        )
        dst = self.params.OutputParameters.directory_path.joinpath(
            "out.fermo.ms2query_results.csv"
        )
        if src.exists:
            shutil.move(src=src, dst=dst)

    def assign_feature_info(self: Self, results_path: str | Path):
        """Load ms2query results and add annotation to Feature objects

        Arguments:
            results_path: location of the ms2query results file
        """
        df = pd.read_csv(results_path)
        df.fillna("unknown", inplace=True)

        for _, row in df.iterrows():
            if int(row["id"]) not in self.active_features:
                logger.debug(
                    f"'AnnotationManager/MS2QueryAnnotator': in MS2Query results, "
                    f"feature with ID "
                    f"'{row['id']}' is not part of set of currently active features. "
                    f"This feature might have been filtered out due to fermo_core "
                    f"filter settings. Alternatively, the wrong MS2Query results file "
                    f"was provided - SKIP"
                )
                continue
            else:
                if float(row["ms2query_model_prediction"]) >= self.cutoff:
                    feature = self.features.get(int(row["id"]))

                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.matches is None:
                        feature.Annotations.matches = []

                    feature.Annotations.matches.append(
                        Match(
                            id=row["analog_compound_name"],
                            library="ms2query",
                            algorithm="ms2query",
                            score=float(row["ms2query_model_prediction"]),
                            mz=float(row["precursor_mz_analog"]),
                            diff_mz=float(row["precursor_mz_difference"]),
                            module="ms2query_annotation",
                            smiles=str(row["smiles"]),
                            inchikey=str(row["inchikey"]),
                            npc_class=str(row["npc_class_results"]),
                        )
                    )
                    self.features.modify(int(row["id"]), feature)

    def start_ms2query_algorithm(self: Self, library: MS2Library):
        """Run ms2query algorithm with given library and timeout

        Arguments:
            library: the generated MS2Library in positive or negative mode

        Raises:
            func_timeout.FunctionTimedOut
        """
        settings = SettingsRunMS2Query(additional_metadata_columns=("id",))

        if self.params.Ms2QueryAnnotationParameters.maximum_runtime == 0:
            logger.info(
                "'AnnotationManager/MS2QueryAnnotator': Started MS2Query algorithm "
                "with no timeout set."
            )
            run_complete_folder(
                ms2library=library,
                folder_with_spectra=str(
                    self.params.OutputParameters.directory_path.joinpath(
                        "temp_ms2query_queries"
                    ).resolve()
                ),
                results_folder=str(
                    self.params.OutputParameters.directory_path.joinpath(
                        "temp_ms2query_queries"
                    ).resolve()
                ),
                settings=settings,
            )
        else:
            try:
                logger.info(
                    f"'AnnotationManager/MS2QueryAnnotator': Started MS2Query "
                    f"algorithm with a timeout "
                    f"of '{self.params.Ms2QueryAnnotationParameters.maximum_runtime}' "
                    f"seconds."
                )
                func_timeout.func_timeout(
                    timeout=self.params.Ms2QueryAnnotationParameters.maximum_runtime,
                    func=run_complete_folder,
                    kwargs={
                        "ms2library": library,
                        "folder_with_spectra": str(
                            self.params.OutputParameters.directory_path.joinpath(
                                "temp_ms2query_queries"
                            ).resolve()
                        ),
                        "results_folder": str(
                            self.params.OutputParameters.directory_path.joinpath(
                                "temp_ms2query_queries"
                            ).resolve()
                        ),
                        "settings": settings,
                    },
                )
            except func_timeout.FunctionTimedOut as e:
                logger.warning(
                    f"'AnnotationManager/MS2QueryAnnotator': timeout of "
                    f"MS2Query-based calculation:"
                    f"took longer than maximum set time of '"
                    f"{self.params.Ms2QueryAnnotationParameters.maximum_runtime}'. "
                    f"seconds. For unlimited runtime, "
                    f"set 'maximum_runtime' parameter to 0 (zero) - SKIP"
                )
                raise e

    def run_ms2query(self: Self):
        """Prepare dump/load locations and annotate features with ms2query"""

        self.prepare_queries()
        self.estimate_calc_time()
        UtilityMethodManager().check_ms2query_req(
            self.params.PeaktableParameters.polarity
        )
        self.create_ms2query_dirs()
        self.remove_ms2query_temp_files()
        save_as_mgf(
            spectrums=self.queries,
            filename=str(
                self.params.OutputParameters.directory_path.joinpath(
                    "temp_ms2query_queries/f_queries.mgf"
                ).resolve()
            ),
        )

        if self.params.PeaktableParameters.polarity == "positive":
            ms2library = create_library_object_from_one_dir(
                DefaultPaths().dirpath_ms2query_pos
            )
            self.start_ms2query_algorithm(ms2library)
        else:
            ms2library = create_library_object_from_one_dir(
                DefaultPaths().dirpath_ms2query_neg
            )
            self.start_ms2query_algorithm(ms2library)

        self.move_ms2query_results()
        self.assign_feature_info(
            self.params.OutputParameters.directory_path.joinpath(
                "out.fermo.ms2query_results.csv"
            )
        )
        self.remove_temp_ms2query_dirs()
