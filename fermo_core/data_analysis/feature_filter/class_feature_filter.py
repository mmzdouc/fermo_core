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
from typing import Self, Tuple

from pydantic import BaseModel

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


# TODO(MMZ 9.1.24): Add a clean-up step to exclude features that have been filtered
#  from analysis run via FeatureFilter class


class FeatureFilter(BaseModel):
    """Pydantic-based class to organize molecular feature filtering methods.

    Attributes:
        params: holds user-provided parameters
        stats: general information about analysis run
        features: holds Feature objects
        samples: holds Sample objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository

    def return_values(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Returns modified attributes for further processing.

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def filter(self: Self):
        """Call feature filtering methods dependent on given parameters."""
        logging.info("'FeatureFilter': started filtering of molecular features.")

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

        # TODO(MMZ 9.1.24): add clean-up step here

        logging.info("'FeatureFilter': completed filtering of molecular features.")

    def filter_rel_int_range(self: Self):
        """Retain features inside relative int range in at least one sample."""
        logging.info("'FeatureFilter': started filtering for relative intensity.")

        inactive = self.filter_features_for_range(
            self.stats,
            self.samples,
            self.params.FeatureFilteringParameters.filter_rel_int_range,
        )

        for feature in inactive:
            logging.debug(
                f"'FeatureFilter': feature with ID '{feature}' filtered from"
                f" analysis run: outside 'filter_rel_int_range' settings."
            )

        self.stats.inactive_features.update(inactive)

        self.stats.active_features = self.stats.active_features.difference(
            self.stats.inactive_features
        )

        logging.info("'FeatureFilter': completed filtering for relative intensity.")

    def filter_rel_area_range(self: Self):
        """Retain features inside relative area range in at least one sample."""
        logging.info("'FeatureFilter': started filtering for relative area.")

        inactive = self.filter_features_for_range(
            self.stats,
            self.samples,
            self.params.FeatureFilteringParameters.filter_rel_area_range,
        )

        for feature in inactive:
            logging.debug(
                f"'FeatureFilter': feature with ID '{feature}' filtered from"
                f" analysis run: outside 'filter_rel_area_range' settings."
            )

        self.stats.inactive_features.update(inactive)

        self.stats.active_features = self.stats.active_features.difference(
            self.stats.inactive_features
        )

        logging.info("'FeatureFilter': completed filtering for relative area.")

    @staticmethod
    def filter_features_for_range(
        stats: Stats, samples: Repository, r_list: list
    ) -> set:
        """Determine features with values outside of given range

        Arguments:
            stats: a Stats object
            samples: a repository object
            r_list: a list of two floats indicating the range

        Returns:
            A set of features that have no occurrences inside range.
        """
        inside_range = set()
        outside_range = set()

        for sample_id in stats.samples:
            sample = samples.get(sample_id)
            for feature_id in sample.feature_ids:
                feature = sample.features.get(feature_id)
                if r_list[0] <= feature.rel_intensity <= r_list[1]:
                    inside_range.add(feature.f_id)
                else:
                    outside_range.add(feature.f_id)

        return outside_range.difference(inside_range)
