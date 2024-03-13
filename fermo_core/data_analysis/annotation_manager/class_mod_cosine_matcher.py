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
from typing import Self

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

    def run_analysis(self: Self):
        """Run filtering and library matching."""

        algorithm = matchms.similarity.ModifiedCosine(
            tolerance=self.params.SpectralLibMatchingCosineParameters.fragment_tol
        )

        for f_id in self.stats.active_features:
            feature = self.features.get(f_id)

            if feature.Spectrum is None:
                logger.info(
                    f"'ModCosineMatcher': feature with id '{feature.f_id}' has no "
                    f"associated MS2 spectrum - SKIP"
                )
                continue

            subset_ids = self.subset_spectral_library(feature)
            if len(subset_ids) == 0:
                continue
            subset = [self.stats.spectral_library[i].Spectrum for i in subset_ids]

            scores = matchms.calculate_scores(
                references=subset,
                queries=[feature.Spectrum],
                similarity_function=algorithm,
            )

            feature = self.assign_matches(feature, scores)
            self.features.modify(f_id, feature)

        return self.features

    def subset_spectral_library(self: Self, feature: Feature) -> set:
        """Based on mod cosine filters, create a subset of lib spectra to match against

        Arguments:
            feature: the feature in question

        Returns:
             A set of library ids to match against
        """
        subset = set()
        for key, spectrum in self.stats.spectral_library.items():
            if (
                abs(spectrum.exact_mass - feature.mz)
                <= self.params.SpectralLibMatchingCosineParameters.max_precursor_mass_diff
            ):
                subset.add(key)

        return subset

    def assign_matches(self: Self, feature: Feature, scores: matchms.Scores) -> Feature:
        """Add spectral library match information to Feature

        Arguments:
            feature: the feature in question
            scores: a matchms score object with spectral library matches

        Returns:
             The modified feature
        """
        matches = scores.scores_by_query(
            feature.Spectrum, name="ModifiedCosine_score", sort=True
        )

        filtered = []
        for match in matches:
            if (
                match[1][0]
                >= self.params.SpectralLibMatchingCosineParameters.score_cutoff
                and match[1][1]
                >= self.params.SpectralLibMatchingCosineParameters.min_nr_matched_peaks
            ):
                filtered.append(match)

        if len(filtered) > 0:
            if feature.Annotations is None:
                feature.Annotations = Annotations()

            if feature.Annotations.matches is None:
                feature.Annotations.matches = []

            for match in filtered:
                feature.Annotations.matches.append(
                    Match(
                        id=match[0].metadata.get("id"),
                        library=str(self.params.SpecLibParameters.filepath.resolve()),
                        algorithm="modified cosine",
                        score=float(match[1][0].round(2)),
                        mz=match[0].metadata.get("precursor_mz"),
                        diff_mz=abs(match[0].metadata.get("precursor_mz") - feature.mz),
                    )
                )
            return feature
        else:
            return feature
