"""Class to manage methods to filter features for various parameters.

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

from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class FeatureFilter(BaseModel):
    """Pydantic-based class to organize molecular feature filtering methods.

    Attributes:
        params: holds user-provided parameters
        stats: general information about analysis run
        features: holds Feature objects
        samples: holds Sample objects

    Notes:
        Should be called as first step in data analysis
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository

    def return_values(self: Self) -> tuple[Stats, Repository, Repository]:
        """Returns modified attributes for further processing.

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def filter(self: Self):
        """Call feature filtering methods dependent on given parameters."""
        logger.info("'FeatureFilter': started filtering of molecular features.")

        modules = (
            (
                self.params.FeatureFilteringParameters.filter_rel_int_range,
                self.filter_rel_int_range,
            ),
            (
                self.params.FeatureFilteringParameters.filter_rel_area_range,
                self.filter_rel_area_range,
            ),
        )

        for module in modules:
            if module[0] is not None:
                module[1]()

        self.remove_filtered_features()

        logger.info("'FeatureFilter': completed filtering of molecular features.")

    def remove_filtered_features(self: Self):
        """Remove features that have been filtered out due to the given settings"""
        if len(self.stats.inactive_features) == 0:
            return

        for f_id in self.stats.inactive_features:
            logger.debug(
                f"'FeatureFilter': feature with ID '{f_id}' filtered from"
                f" analysis run: outside filter settings."
            )
            self.features.remove(f_id)
            for s_id in self.stats.samples:
                sample = self.samples.get(s_id)
                if f_id in sample.feature_ids:
                    sample.feature_ids.remove(f_id)
                    del sample.features[f_id]
                    self.samples.modify(s_id, sample)

    def filter_rel_int_range(self: Self):
        """Retain features inside relative intensity range in at least one sample."""
        logger.info("'FeatureFilter': started filtering for relative intensity.")

        inactive = self.filter_features_for_range(
            self.stats,
            self.samples,
            self.params.FeatureFilteringParameters.filter_rel_int_range,
            "rel_intensity",
        )

        self.stats.inactive_features.update(inactive)

        self.stats.active_features = self.stats.active_features.difference(
            self.stats.inactive_features
        )

        logger.info("'FeatureFilter': completed filtering for relative intensity.")

    def filter_rel_area_range(self: Self):
        """Retain features inside relative area range in at least one sample."""
        logger.info("'FeatureFilter': started filtering for relative area.")

        inactive = self.filter_features_for_range(
            self.stats,
            self.samples,
            self.params.FeatureFilteringParameters.filter_rel_area_range,
            "rel_area",
        )

        self.stats.inactive_features.update(inactive)

        self.stats.active_features = self.stats.active_features.difference(
            self.stats.inactive_features
        )

        logger.info("'FeatureFilter': completed filtering for relative area.")

    @staticmethod
    def filter_features_for_range(
        stats: Stats, samples: Repository, r_list: list, param: str
    ) -> set:
        """Determine features with values outside of given range

        Arguments:
            stats: a Stats object
            samples: a repository object
            r_list: a list of two floats indicating the range
            param: the parameter to check against range

        Returns:
            A set of features that have no occurrences in "inside range" (not in any
            sample).
        """
        inside_range = set()
        outside_range = set()

        for sample_id in stats.samples:
            sample = samples.get(sample_id)
            for feature_id in sample.feature_ids:
                feature = sample.features.get(feature_id)
                if r_list[0] <= getattr(feature, param) <= r_list[1]:
                    inside_range.add(feature.f_id)
                else:
                    outside_range.add(feature.f_id)

        return outside_range.difference(inside_range)
