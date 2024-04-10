"""Runs the ms2deepscore library matching module.

Copyright (c) 2022-2023 Mitja Maximilian Zdouc, PhD

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
from typing import Self, List
import urllib.error

import func_timeout
import matchms
from ms2deepscore import MS2DeepScore
from ms2deepscore.models import load_model
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultSettings
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    Annotations,
    Match,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager

logger = logging.getLogger("fermo_core")


class Ms2deepscoreMatcher(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2deepscore matching

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository

    @staticmethod
    def log_ms2deepscore_timeout(max_time: str):
        """Logs timeout due to long-running ms2deepscore library matching

        Arguments:
            max_time: the set maximum calculation time
        """
        logger.warning(
            f"'AnnotationManager/Ms2deepscoreMatcher': timeout of MS2DeepScore-based "
            f"spectral library matching calculation. Calculation "
            f"took longer than '{max_time}' seconds. Increase the "
            f"'spectral_library_matching/ms2deepscore/maximum_runtime' parameter"
            f" or set it to 0 (zero) for unlimited runtime. Alternatively, "
            f"filter out low-intensity/area peaks with 'feature_filtering' - "
            f"SKIP."
        )

    def run_analysis(self: Self) -> Repository:
        """Run filtering and library matching."""

        if self.params.PeaktableParameters.polarity != "positive":
            logger.warning(
                "'AnnotationManager/Ms2deepscoreMatcher': data polarity not "
                "positive. Currently, only positive ion mode is supported - SKIP"
            )
            return self.features

        try:
            if not UtilityMethodManager().check_ms2deepscore_req():
                UtilityMethodManager().download_ms2deepscore_req(
                    self.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime
                )
        except urllib.error.URLError:
            return self.features

        query_spectra = self.prepare_query_spectra()

        if len(query_spectra) == 0:
            logger.warning(
                "'AnnotationManager/Ms2deepscoreMatcher': no features with MS2 spectra"
                " available for library matching - SKIP"
            )
            return self.features

        try:
            scores = self.calculate_scores_ms2deepscore(query_spectra=query_spectra)
        except func_timeout.FunctionTimedOut:
            return self.features

        for spectrum in query_spectra:
            feature = self.features.get(int(spectrum.metadata.get("id")))

            sorted_matches = scores.scores_by_query(
                spectrum, name="MS2DeepScore", sort=True
            )
            for match in sorted_matches:
                feature = self.annotate_feature(feature, match)

            self.features.modify(int(spectrum.metadata.get("id")), feature)

        return self.features

    def prepare_query_spectra(self: Self) -> List[matchms.Spectrum]:
        """Prepare a filtered list of query spectra for matching

        Returns:
            A list of matchms.Spectrum objects
        """
        query_spectra = []
        for f_id in self.stats.active_features:
            feature = self.features.get(f_id)

            if feature.Spectrum is None:
                logger.debug(
                    f"'AnnotationManager/Ms2deepscoreMatcher': feature with id "
                    f"'{feature.f_id}' has no associated MS2 spectrum - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)
        return query_spectra

    def calculate_scores_ms2deepscore(
        self: Self,
        query_spectra: list,
    ) -> matchms.Scores:
        """Calculate matchms scores with ms2deepscore model

        Arguments:
            query_spectra: a list of matchms Spectrum objects

        Returns:
            A matchms Scores object

        Raises:
            func_timeout.FunctionTimedOut: ms2deepscore calc takes too long.
        """
        model = load_model(
            DefaultSettings().dirpath_ms2deepscore.joinpath(
                DefaultSettings().filename_ms2deepscore
            )
        )

        sim_algorithm = MS2DeepScore(model=model, progress_bar=False)

        if self.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime == 0:
            return matchms.calculate_scores(
                references=self.stats.spectral_library,
                queries=query_spectra,
                similarity_function=sim_algorithm,
            )
        else:
            try:
                return func_timeout.func_timeout(
                    timeout=self.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime,
                    func=matchms.calculate_scores,
                    kwargs={
                        "references": self.stats.spectral_library,
                        "queries": query_spectra,
                        "similarity_function": sim_algorithm,
                    },
                )
            except func_timeout.FunctionTimedOut as e:
                self.log_ms2deepscore_timeout(
                    str(
                        self.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime
                    )
                )
                raise e

    def annotate_feature(self: Self, feature: Feature, match: tuple) -> Feature:
        """Filter matches for user-specified params and assign annotation to feature

        Arguments:
            feature: a Feature object
            match: a Tuple of library reference spectrum and the score
        """
        if match[1] < self.params.SpectralLibMatchingDeepscoreParameters.score_cutoff:
            return feature
        elif (
            abs(match[0].metadata.get("precursor_mz") - feature.mz)
            > self.params.SpectralLibMatchingDeepscoreParameters.max_precursor_mass_diff
        ):
            return feature
        else:
            if feature.Annotations is None:
                feature.Annotations = Annotations()

            if feature.Annotations.matches is None:
                feature.Annotations.matches = []

            feature.Annotations.matches.append(
                Match(
                    id=match[0].metadata.get("compound_name"),
                    library=str(self.params.SpecLibParameters.filepath.resolve()),
                    algorithm="ms2deepscore",
                    score=float(match[1].round(2)),
                    mz=match[0].metadata.get("precursor_mz"),
                    diff_mz=round(
                        abs(match[0].metadata.get("precursor_mz") - feature.mz), 4
                    ),
                )
            )
            return feature
