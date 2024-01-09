"""Organize the calling of data analysis modules.

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
from typing import Tuple, Self

from pydantic import BaseModel

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats

from fermo_core.data_analysis.chrom_trace_calculator.class_chrom_trace_calculator import (
    ChromTraceCalculator,
)
from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter


class AnalysisManager(BaseModel):
    """Pydantic-based class to organize calling and logging of analysis methods

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

    def return_attributes(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def analyze(self: Self):
        """Organizes calling of data analysis steps."""
        logging.info("'AnalysisManager': started analysis steps.")

        self.run_feature_filter()

        # TODO(MMZ 9.1.24): add call to run sim network manager

        self.run_chrom_trace_calculator()

        logging.info("'AnalysisManager': completed analysis steps.")

    def run_feature_filter(self: Self):
        """Run optional FeatureFilter analysis step"""
        if self.params.FeatureFilteringParameters.activate_module is False:
            logging.info(
                "'FeatureFiltering': module 'feature_filtering' not activated - SKIP."
            )
            return

        feature_filter = FeatureFilter(
            params=self.params,
            stats=self.stats,
            features=self.features,
            samples=self.samples,
        )
        feature_filter.filter()
        self.stats, self.features, self.samples = feature_filter.return_values()

    # TODO(MMZ 9.1.24): Add method to call SimNetworksManager; also handle
    #  non-activated module (if not there: skip); skip if no MSMS data was given

    def run_chrom_trace_calculator(self: Self):
        """Run mandatory ChromTraceCalculator analysis step."""
        self.samples = ChromTraceCalculator().modify_samples(self.samples, self.stats)
