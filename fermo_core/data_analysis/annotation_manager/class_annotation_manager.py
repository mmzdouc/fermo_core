"""Organize the calling of annotation modules.

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
from typing import Self, Tuple
import urllib.error

import func_timeout
from pydantic import BaseModel

from fermo_core.data_analysis.annotation_manager.class_mod_cosine_matcher import (
    ModCosineMatcher,
)
from fermo_core.data_analysis.annotation_manager.class_ms2deepscore_matcher import (
    Ms2deepscoreMatcher,
)
from fermo_core.data_analysis.annotation_manager.class_mod_cos_annotator import (
    ModCosAnnotator,
)
from fermo_core.data_analysis.annotation_manager.class_ms2deepscore_annotator import (
    Ms2deepscoreAnnotator,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Match,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class AnnotationManager(BaseModel):
    """Pydantic-based class to organize calling and logging of annotation modules

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository

    def return_attrs(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Returns modified attributes from AnnotationManager to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""
        logger.info("'AnnotationManager': started analysis steps.")

        modules = (
            (
                self.params.SpectralLibMatchingCosineParameters.activate_module,
                self.run_user_lib_mod_cosine_matching,
            ),
            (
                self.params.SpectralLibMatchingDeepscoreParameters.activate_module,
                self.run_user_lib_ms2deepscore_matching,
            )
            # (
            #     self.params.SpectralLibMatchingCosineParameters.activate_module,
            #     self.run_modified_cosine_matching,
            # ),
            # (
            #     self.params.SpectralLibMatchingDeepscoreParameters.activate_module,
            #     self.run_ms2deepscore_matching,
            # )
            # TODO(MMZ 13.03.24): Add additional annotation modules e.g. adduct,
            #  ms2query
        )

        for module in modules:
            if module[0]:
                module[1]()

        logger.info("'AnnotationManager': completed analysis steps.")

    def run_user_lib_mod_cosine_matching(self: Self):
        """Match features against a user-provided spectral library using mod cosine."""
        logger.info(
            "'AnnotationManager': started matching of features against a "
            "user-provided spectral library using the modified cosine algorithm."
        )

        if self.params.SpecLibParameters is None:
            logger.warning(
                "'AnnotationManager': no spectral library parameters provided - SKIP"
            )
            return
        elif self.stats.spectral_library is None:
            logger.warning(
                "'AnnotationManager': no spectral library file provided - SKIP"
            )
            return
        elif len(self.stats.spectral_library) == 0:
            logger.warning("'AnnotationManager': spectral library file is empty - SKIP")
            return

        mod_cosine_annotator = ModCosAnnotator(
            features=self.features,
            active_features=self.stats.active_features,
            library=self.stats.spectral_library,
            max_time=self.params.SpectralLibMatchingCosineParameters.maximum_runtime,
            fragment_tol=self.params.SpectralLibMatchingCosineParameters.fragment_tol,
            score_cutoff=self.params.SpectralLibMatchingCosineParameters.score_cutoff,
            min_nr_matched_peaks=self.params.SpectralLibMatchingCosineParameters.min_nr_matched_peaks,
            max_precursor_mass_diff=self.params.SpectralLibMatchingCosineParameters.max_precursor_mass_diff,
        )
        try:
            mod_cosine_annotator.prepare_queries()
            mod_cosine_annotator.calculate_scores_mod_cosine()
            scores = mod_cosine_annotator.return_scores()

            for spectrum in mod_cosine_annotator.queries:
                feature = self.features.get(int(spectrum.metadata.get("id")))
                sorted_matches = scores.scores_by_query(
                    spectrum, name="ModifiedCosine_score", sort=True
                )

                for match in sorted_matches:
                    if mod_cosine_annotator.filter_match(match, feature.mz):
                        if feature.Annotations is None:
                            feature.Annotations = Annotations()

                        if feature.Annotations.matches is None:
                            feature.Annotations.matches = []

                        feature.Annotations.matches.append(
                            Match(
                                id=match[0].metadata.get("compound_name"),
                                library=str(
                                    self.params.SpecLibParameters.filepath.resolve()
                                ),
                                algorithm="modified cosine",
                                score=float(match[1][0].round(2)),
                                mz=match[0].metadata.get("precursor_mz"),
                                diff_mz=round(
                                    abs(
                                        match[0].metadata.get("precursor_mz")
                                        - feature.mz
                                    ),
                                    4,
                                ),
                            )
                        )
                self.features.modify(int(spectrum.metadata.get("id")), feature)
        except RuntimeError:
            return
        except func_timeout.FunctionTimedOut:
            return

        logger.info(
            "'AnnotationManager': completed matching of features against a "
            "user-provided spectral library using the modified cosine algorithm."
        )

    def run_user_lib_ms2deepscore_matching(self: Self):
        """Match features against a user-provided spectral library using ms2deepscor."""
        logger.info(
            "'AnnotationManager': started matching of features against a "
            "user-provided spectral library using the ms2deepscore algorithm."
        )

        if self.params.SpecLibParameters is None:
            logger.warning(
                "'AnnotationManager': no spectral library parameters provided - SKIP"
            )
            return
        elif self.stats.spectral_library is None:
            logger.warning(
                "'AnnotationManager': no spectral library file provided - SKIP"
            )
            return
        elif len(self.stats.spectral_library) == 0:
            logger.warning("'AnnotationManager': spectral library file is empty - SKIP")
            return

        ms2deepscore_annotator = Ms2deepscoreAnnotator(
            features=self.features,
            active_features=self.stats.active_features,
            polarity=self.params.PeaktableParameters.polarity,
            library=self.stats.spectral_library,
            max_time=self.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime,
            score_cutoff=self.params.SpectralLibMatchingDeepscoreParameters.score_cutoff,
            max_precursor_mass_diff=self.params.SpectralLibMatchingDeepscoreParameters.max_precursor_mass_diff,
        )

        try:
            ms2deepscore_annotator.prepare_queries()
            ms2deepscore_annotator.calculate_scores_ms2deepscore()
            scores = ms2deepscore_annotator.return_scores()

            for spectrum in ms2deepscore_annotator.queries:
                feature = self.features.get(int(spectrum.metadata.get("id")))
                sorted_matches = scores.scores_by_query(
                    spectrum, name="MS2DeepScore", sort=True
                )

                for match in sorted_matches:
                    if ms2deepscore_annotator.filter_match(match, feature.mz):
                        if feature.Annotations is None:
                            feature.Annotations = Annotations()

                        if feature.Annotations.matches is None:
                            feature.Annotations.matches = []

                        feature.Annotations.matches.append(
                            Match(
                                id=match[0].metadata.get("compound_name"),
                                library=str(
                                    self.params.SpecLibParameters.filepath.resolve()
                                ),
                                algorithm="ms2deepscore",
                                score=float(match[1].round(2)),
                                mz=match[0].metadata.get("precursor_mz"),
                                diff_mz=round(
                                    abs(
                                        match[0].metadata.get("precursor_mz")
                                        - feature.mz
                                    ),
                                    4,
                                ),
                            )
                        )
                self.features.modify(int(spectrum.metadata.get("id")), feature)
        except RuntimeError:
            return
        except func_timeout.FunctionTimedOut:
            return
        except urllib.error.URLError:
            return

        logger.info(
            "'AnnotationManager': completed matching of features against a "
            "user-provided spectral library using the ms2deepscore algorithm."
        )

    def run_modified_cosine_matching(self: Self):
        """Run modified cosine-based spectral library search on features."""
        logger.info(
            "'AnnotationManager': started modified cosine-based spectral library "
            "matching."
        )

        if self.params.SpecLibParameters is None:
            logger.warning(
                "'AnnotationManager': no spectral library parameters provided - SKIP"
            )
            return
        elif self.stats.spectral_library is None:
            logger.warning(
                "'AnnotationManager': no spectral library file provided - SKIP"
            )
            return
        elif len(self.stats.spectral_library) == 0:
            logger.warning("'AnnotationManager': spectral library file is empty - SKIP")
            return

        mod_cosine_matcher = ModCosineMatcher(
            params=self.params,
            stats=self.stats,
            features=self.features,
        )

        self.features = mod_cosine_matcher.run_analysis()

        logger.info(
            "'AnnotationManager': completed modified cosine-based spectral library "
            "matching."
        )

    def run_ms2deepscore_matching(self: Self):
        """Run ms2deepscore-based spectral library search on features."""
        logger.info(
            "'AnnotationManager': started ms2deepscore-based spectral library "
            "matching."
        )

        if self.params.SpecLibParameters is None:
            logger.warning(
                "'AnnotationManager': no spectral library parameters provided - SKIP"
            )
            return
        elif self.stats.spectral_library is None:
            logger.warning(
                "'AnnotationManager': no spectral library file provided - SKIP"
            )
            return
        elif len(self.stats.spectral_library) == 0:
            logger.warning("'AnnotationManager': spectral library file is empty - SKIP")
            return

        ms2deepscore_matcher = Ms2deepscoreMatcher(
            params=self.params,
            stats=self.stats,
            features=self.features,
        )

        self.features = ms2deepscore_matcher.run_analysis()

        logger.info(
            "'AnnotationManager': completed ms2deepscore-based spectral library "
            "matching."
        )
