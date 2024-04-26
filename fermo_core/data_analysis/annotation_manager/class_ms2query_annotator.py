"""Runs the ms2query library annotation module.

Copyright (c) 2024 Mitja Maximilian Zdouc, PhD

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
import logging
import os
import pandas as pd
from pathlib import Path
from typing import Self, Optional

import func_timeout
from matchms.exporting import save_as_mgf
from ms2query.run_ms2query import run_complete_folder
from ms2query.ms2library import create_library_object_from_one_dir, MS2Library
from ms2query.utils import SettingsRunMS2Query
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.utils.utility_method_manager import UtilityMethodManager
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Match,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class MS2QueryAnnotator(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2query lib matching

    Attributes:
        features: Repository object, holds "General Feature" objects
        params: User-provided parameters
        active_features: a set of active features
        queries: a list of Spectra for which to perform matching
    """

    features: Repository
    params: ParameterManager
    active_features: set
    queries: Optional[list] = None

    def log_ms2query_timeout(self: Self):
        """Logs timeout due to long-running ms2query library matching"""
        logger.warning(
            f"'MS2QueryAnnotator': timeout of "
            f"MS2Query-based calculation: "
            f"took longer than maximum set time of '"
            f"{self.params.Ms2QueryAnnotationParameters.maximum_runtime}' seconds. "
            f"For unlimited runtime, set 'maximum_runtime' parameter to 0 (zero) - SKIP"
        )

    def return_features(self: Self) -> Repository:
        """Return the modified Feature objects as Repository

        Returns:
            A Repository with modified Feature objects
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
                    f"'MS2QueryAnnotator': feature with id "
                    f"'{feature.f_id}' has no associated MS2 spectrum - SKIP"
                )
                continue
            elif (
                feature.blank is True
                and self.params.Ms2QueryAnnotationParameters.exclude_blank is True
            ):
                logger.debug(
                    f"'MS2QueryAnnotator': feature with id "
                    f"'{feature.f_id}' is blank-associated and MS2Query is set to "
                    f"exclude blanks - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)

        if len(query_spectra) != 0:
            self.queries = query_spectra
        else:
            logger.warning(
                "'MS2QueryAnnotator': no query spectra could be "
                "collected for matching - SKIP "
            )
            raise RuntimeError

    def estimate_calc_time(self: Self):
        """Estimates the approximate calculation time and aborts if set time too low

        Raises:
            RuntimeError: no query spectra collected (None) or runtime too short
        """
        if self.queries is None:
            logger.error(
                "'MS2QueryAnnotator': 'self.queries' is None - run 'prepare_queries'."
            )
            raise RuntimeError

        if self.params.Ms2QueryAnnotationParameters.maximum_runtime != 0:
            if (
                len(self.queries) * 2.5
            ) > self.params.Ms2QueryAnnotationParameters.maximum_runtime:
                logger.warning(
                    f"'MS2QueryAnnotator': Estimated runtime of MS2Query for the "
                    f"annotation of "
                    f"'{len(self.queries)}' features is '{len(self.queries) * 2.5}' "
                    f"seconds. This exceeds the maximum allowed runtime of "
                    f"'{self.params.Ms2QueryAnnotationParameters.maximum_runtime}' "
                    f"seconds. Please increase the 'max_runtime' parameter or set to "
                    f"'0' for unlimited runtime - SKIP"
                )
                raise RuntimeError

    @staticmethod
    def create_ms2query_dirs():
        """Create dirs for running ms2query if not existing"""
        if not DefaultPaths().dirpath_ms2query_base.joinpath("queries").exists():
            os.mkdir(DefaultPaths().dirpath_ms2query_base.joinpath("queries"))

        if not DefaultPaths().dirpath_ms2query_base.joinpath("results").exists():
            os.mkdir(DefaultPaths().dirpath_ms2query_base.joinpath("results"))

    @staticmethod
    def remove_ms2query_temp_files():
        """Remove queries and results files to clean up before run"""
        if DefaultPaths().dirpath_ms2query_base.joinpath("queries").exists():
            if (
                DefaultPaths()
                .dirpath_ms2query_base.joinpath("queries/f_queries.mgf")
                .exists()
            ):
                os.remove(
                    DefaultPaths().dirpath_ms2query_base.joinpath(
                        "queries/f_queries.mgf"
                    )
                )

        if DefaultPaths().dirpath_ms2query_base.joinpath("results").exists():
            if (
                DefaultPaths()
                .dirpath_ms2query_base.joinpath("results/f_queries.csv")
                .exists()
            ):
                os.remove(
                    DefaultPaths().dirpath_ms2query_base.joinpath(
                        "results/f_queries.csv"
                    )
                )

    def assign_feature_info(self: Self, results_path: str | Path):
        """Load ms2query results and add annotation to feature

        Arguments:
            results_path: location of the ms2query results file
        """
        df = pd.read_csv(results_path)
        for _, row in df.iterrows():
            feature = self.features.get(int(row["id"]))

            if feature.Annotations is None:
                feature.Annotations = Annotations()
            if feature.Annotations.matches is None:
                feature.Annotations.matches = []

            if (
                float(row["ms2query_model_prediction"])
                >= self.params.Ms2QueryAnnotationParameters.score_cutoff
            ):
                match = Match(
                    id=row["analog_compound_name"],
                    library="ms2query",
                    algorithm="ms2query",
                    score=float(row["ms2query_model_prediction"]),
                    mz=float(row["precursor_mz_analog"]),
                    diff_mz=float(row["precursor_mz_difference"]),
                    module="MS2QueryAnnotator",
                )
                match.smiles = row["smiles"]
                match.inchikey = row["inchikey"]
                match.npc_class = row["npc_class_results"]

                feature.Annotations.matches.append(match)
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
            run_complete_folder(
                ms2library=library,
                folder_with_spectra=DefaultPaths().dirpath_ms2query_base.joinpath(
                    "queries"
                ),
                results_folder=DefaultPaths().dirpath_ms2query_base.joinpath("results"),
                settings=settings,
            )
        else:
            try:
                func_timeout.func_timeout(
                    timeout=self.params.Ms2QueryAnnotationParameters.maximum_runtime,
                    func=run_complete_folder,
                    kwargs={
                        "ms2library": library,
                        "folder_with_spectra": DefaultPaths().dirpath_ms2query_base.joinpath(
                            "queries"
                        ),
                        "results_folder": DefaultPaths().dirpath_ms2query_base.joinpath(
                            "results"
                        ),
                        "settings": settings,
                    },
                )
            except func_timeout.FunctionTimedOut as e:
                self.log_ms2query_timeout()
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
            filename=DefaultPaths().dirpath_ms2query_base.joinpath(
                "queries/f_queries.mgf"
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

        self.assign_feature_info(
            DefaultPaths().dirpath_ms2query_base.joinpath("results/f_queries.csv")
        )
