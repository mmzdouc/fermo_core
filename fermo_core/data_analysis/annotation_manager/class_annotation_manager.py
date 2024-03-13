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

import func_timeout
from pydantic import BaseModel

from fermo_core.data_analysis.annotation_manager.class_mod_cosine_matcher import (
    ModCosineMatcher,
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
                self.run_modified_cosine_matching,
            ),
            (
                self.params.SpectralLibMatchingDeepscoreParameters.activate_module,
                self.run_ms2deepscore_matching,
            )
            # TODO(MMZ 13.03.24): Add additional annotation modules e.g. adduct,
            #  ms2query
        )

        for module in modules:
            if module[0]:
                module[1]()

        logger.info("'AnnotationManager': completed analysis steps.")

    def run_modified_cosine_matching(self: Self):
        """Run modified cosine-based spectral library search on features."""
        logger.info(
            "'AnnotationManager': started modified cosine-based spectral library "
            "matching."
        )

        if self.stats.spectral_library is None:
            logger.warning(
                "'AnnotationManager': could not run modified cosine-based library "
                "matching: no spectral library file provided "
                "- SKIP"
            )
            return

        mod_cosine_matcher = ModCosineMatcher(
            params=self.params,
            stats=self.stats,
            features=self.features,
        )

        try:
            # TODO(MMZ 13.03.24): put this into the timeout function right away here
            self.features = mod_cosine_matcher.run_analysis()
        except func_timeout.FunctionTimedOut:
            logger.warning(
                f"'AnnotationManager/ModCosineMatcher': timeout of modified "
                f"cosine spectral library matching calculation. Calculation "
                f"took longer than "
                f"'{self.params.SpectralLibMatchingCosineParameters.maximum_runtime}' "
                f"seconds. Increase the "
                f"'spectral_library_matching/modified_cosine/maximum_runtime' parameter"
                f" or set it to 0 (zero) for unlimited runtime. Alternatively, "
                f"filter out low-intensity/area peaks with 'feature_filtering' - SKIP."
            )
            return

        logger.info(
            "'AnnotationManager': completed modified cosine-based spectral library "
            "matching."
        )
