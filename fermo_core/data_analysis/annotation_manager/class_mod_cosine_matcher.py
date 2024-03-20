"""Runs the modified cosine library matching module.

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
from typing import Self, List, Tuple

import func_timeout
import matchms
from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    Annotations,
    Match,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class ModCosineMatcher(BaseModel):
    """Pydantic-based class to organize calling and logging of annotation modules

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository

    def run_analysis(self: Self) -> Repository:
        """Run filtering and library matching."""

        query_spectra = self.prepare_query_spectra()

        if self.params.SpectralLibMatchingCosineParameters.maximum_runtime == 0:
            scores = matchms.calculate_scores(
                references=self.stats.spectral_library,
                queries=query_spectra,
                similarity_function=matchms.similarity.ModifiedCosine(
                    tolerance=self.params.SpectralLibMatchingCosineParameters.fragment_tol
                ),
            )
        else:
            try:
                scores = func_timeout.func_timeout(
                    timeout=self.params.SpectralLibMatchingCosineParameters.maximum_runtime,
                    func=matchms.calculate_scores,
                    kwargs={
                        "references": self.stats.spectral_library,
                        "queries": query_spectra,
                        "similarity_function": matchms.similarity.ModifiedCosine(
                            tolerance=self.params.SpectralLibMatchingCosineParameters.fragment_tol
                        ),
                    },
                )
            except func_timeout.FunctionTimedOut:
                logger.warning(
                    f"'AnnotationManager/ModCosineMatcher': timeout of modified "
                    f"cosine spectral library matching calculation. Calculation "
                    f"took longer than "
                    f"'{self.params.SpectralLibMatchingCosineParameters.maximum_runtime}' "
                    f"seconds. Increase the "
                    f"'spectral_library_matching/modified_cosine/maximum_runtime' "
                    f"parameter"
                    f" or set it to 0 (zero) for unlimited runtime. Alternatively, "
                    f"filter out low-intensity/area peaks with 'feature_filtering' - "
                    f"SKIP."
                )
                return self.features

        for spectrum in query_spectra:
            feature = self.features.get(int(spectrum.metadata.get("id")))

            sorted_matches = scores.scores_by_query(
                spectrum, name="ModifiedCosine_score", sort=True
            )
            for match in sorted_matches:
                feature = self.annotate_feature(feature, match)

            self.features.modify(int(spectrum.metadata.get("id")), feature)

        return self.features

    def prepare_query_spectra(self: Self) -> List[matchms.Spectrum]:
        """Prepare a filtred list of query spectra for matching

        Returns:
            A list of matchms.Spectrum objects
        """
        query_spectra = []
        for f_id in self.stats.active_features:
            feature = self.features.get(f_id)

            if feature.Spectrum is None:
                logger.debug(
                    f"'ModCosineMatcher': feature with id '{feature.f_id}' has no "
                    f"associated MS2 spectrum - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)
        return query_spectra

    def annotate_feature(self: Self, feature: Feature, match: Tuple) -> Feature:
        """Filter matches for user-specified params and assign annotation to feature

        Arguments:
            feature: a Feature object
            match: a Tuple of library reference spectrum and the score
        """
        if match[1][0] < self.params.SpectralLibMatchingCosineParameters.score_cutoff:
            return feature
        elif (
            match[1][1]
            < self.params.SpectralLibMatchingCosineParameters.min_nr_matched_peaks
        ):
            return feature
        elif (
            abs(match[0].metadata.get("precursor_mz") - feature.mz)
            > self.params.SpectralLibMatchingCosineParameters.max_precursor_mass_diff
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
                    algorithm="modified cosine",
                    score=float(match[1][0].round(2)),
                    mz=match[0].metadata.get("precursor_mz"),
                    diff_mz=round(
                        abs(match[0].metadata.get("precursor_mz") - feature.mz), 4
                    ),
                )
            )
            return feature
