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
from typing import Self, Tuple

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


class FeatureFilter:
    """Interface to organize molecular feature filtering methods."""

    def filter(
        self: Self,
        params: ParameterManager,
        stats: Stats,
        features: Repository,
        samples: Repository,
    ) -> Tuple[Stats, Repository, Repository]:
        """Calls feature filtering methods dependent on given parameters

        Arguments:
            params: stores parameters for data processing
            stats: summarizing stats of experiment run
            features: Repository containing Feature Objects
            samples: Repository containing Sample Objects

        Returns:
            A tuple with modified Stats, Sample Repository, Feature Repository
        """
        return stats, features, samples

    # TODO(MMZ 03.01.24): move to FeatureFiltering class
    # def _get_features_in_range_mzmine3(
    #     self: Self, df: pd.DataFrame, rng: List[float]
    # ) -> Tuple[Tuple, Tuple]:
    #     """Separate features into two sets based on their relative intensity.
    #
    #     Filter features based on their relative intensity compared against the feature
    #     with the highest intensity in the sample. For a range between 0-1,
    #     for each feature, test if feature lies inside the given range in at least one
    #     sample. Only exclude features that are below the relative intensity in all
    #     samples in which they are detected.
    #
    #     Args:
    #         df: pandas DataFrame resulting from mzmine3 style peaktable
    #         rng: user-provided range
    #
    #     Returns:
    #         Two tuples: one "included" (features inside of range), one "excluded" (
    #         features outside of range)
    #     """
    #     incl = set()
    #     excl = set()
    #
    #     # Extract overall most intense feature per sample as ref for relative intensity
    #     sample_max_int = dict()
    #     for sample in self.samples:
    #         sample_max_int[sample] = df.loc[
    #             :, f"datafile:{sample}:intensity_range:max"
    #         ].max()
    #
    #     # Get feature intensity per sample, prepare for comparison
    #     for _, row in df.iterrows():
    #         sample_values = row.dropna().filter(regex=":intensity_range:max")
    #         feature_int = dict()
    #         for index, value in sample_values.items():
    #             sample = index.split(":")[1]
    #             feature_int[sample] = value
    #
    #         # Retain features that are inside rel int range for at least one sample
    #         if any(
    #             (sample_max_int[sample] * rng[0])
    #             <= feature_int[sample]
    #             <= (sample_max_int[sample] * rng[1])
    #             for sample in feature_int
    #         ):
    #             incl.add(row["id"])
    #         else:
    #             excl.add(row["id"])
    #             logging.debug(
    #                 f"Molecular feature with feature ID '{row['id']}' was filtered "
    #                 f"from dataset due to range settings."
    #             )
    #
    #     return tuple(incl), tuple(excl)
