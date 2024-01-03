"""Organize the calling of various data analysis modules.

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
from typing import Tuple

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats

from fermo_core.data_analysis.chrom_trace_calculator.class_chrom_trace_calculator import (
    ChromTraceCalculator,
)
from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter


class AnalysisManager:
    """Interface to organize calling of specific data analysis methods."""

    @staticmethod
    def analyze(
        params: ParameterManager,
        stats: Stats,
        features: Repository,
        samples: Repository,
    ) -> Tuple[Stats, Repository, Repository]:
        """Organizes calling of data analysis steps.

        Arguments:
            params: stores parameters for data processing
            stats: summarizing stats of experiment run
            features: Repository containing Feature Objects
            samples: Repository containing Sample Objects

        Returns:
            A tuple with modified Stats, Sample Repository, Feature Repository

        Notes:
            Adjust here for additional data analysis steps/methods.
        """

        # TODO(MMZ 03.01.24): uncomment once fully tested
        # stats, features, samples = FeatureFilter().filter(
        #     params,
        #     stats,
        #     features,
        #     samples
        # )

        # TODO(MMZ) 26.12.23: proceed with annotations, bioactivity etc.
        # TODO(MMZ) 26.12.23: when calculating fold changes, also add group info to
        #  features

        samples = ChromTraceCalculator().modify_samples(samples, stats)

        return stats, features, samples
