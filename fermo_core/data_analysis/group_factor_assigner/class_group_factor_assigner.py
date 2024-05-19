"""Assign group factor information.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

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
import statistics
from itertools import combinations
from typing import Self

from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import GroupFactor
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class GroupFactorAssigner(BaseModel):
    """Pydantic-based class to organize group factor (fold change) assignment.

    Attributes:
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository

    def return_features(self: Self) -> Repository:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing the modified Feature Repository object.
        """
        return self.features

    def calc_rprsnt(self: Self, vals: list) -> float:
        """Calculate representative value from list using user-specified algorithm

        Arguments:
            vals: a list of int values representing height or area

        Returns:
            The determined representative value

        Raises:
            RuntimeError: unexpected algorithm
        """
        if self.params.GroupFactAssignmentParameters.algorithm == "mean":
            return float(statistics.mean(vals))
        elif self.params.GroupFactAssignmentParameters.algorithm == "median":
            return float(statistics.median(vals))
        elif self.params.GroupFactAssignmentParameters.algorithm == "maximum":
            return float(max(vals))
        else:
            raise RuntimeError(
                "'GroupFactorAssigner': unexpected algorithm found - SKIP."
            )

    def get_value(self: Self, f_id: int, sample_ids: set) -> float:
        """Retrieve values for sample ids from feature and calculate repres. value

        Arguments:
            f_id: a feature ID
            sample_ids: the sample Ids to retrieve

        Returns:
            The determined representative value

        Raises:
            RuntimeError: unexpected value
        """
        feature = self.features.get(f_id)
        values_s_ids = []

        if self.params.GroupFactAssignmentParameters.value == "area":
            for entry in feature.area_per_sample:
                if entry.s_id in sample_ids:
                    values_s_ids.append(entry.value)
        else:
            for entry in feature.height_per_sample:
                if entry.s_id in sample_ids:
                    values_s_ids.append(entry.value)

        return self.calc_rprsnt(values_s_ids)

    def assign_group_factors(self: Self):
        """Calculate group factors and assign to Features and Stats instances"""
        for f_id in self.stats.active_features:
            if f_id in self.stats.GroupMData.blank_f_ids:
                continue

            feature = self.features.get(f_id)
            feature.group_factors = {}
            for categ, vals in feature.groups.items():
                if len(vals) < 2:
                    continue

                for comb in combinations(vals, r=2):
                    group1_s_ids = feature.samples.intersection(
                        self.stats.GroupMData.ctgrs[categ][comb[0]].s_ids
                    )
                    group2_s_ids = feature.samples.intersection(
                        self.stats.GroupMData.ctgrs[categ][comb[1]].s_ids
                    )
                    gr1_val = self.get_value(f_id, group1_s_ids)
                    gr2_val = self.get_value(f_id, group2_s_ids)

                    facts = [(gr1_val / gr2_val), (gr2_val / gr1_val)]
                    facts.sort(reverse=True)
                    if categ in feature.group_factors:
                        feature.group_factors[categ].append(
                            GroupFactor(group1=comb[0], group2=comb[1], factor=facts[0])
                        )
                    else:
                        feature.group_factors[categ] = [
                            GroupFactor(group1=comb[0], group2=comb[1], factor=facts[0])
                        ]
            self.features.modify(f_id, feature)

    def run_analysis(self: Self):
        """Run group factor assignment analysis"""
        logger.info("'GroupFactorAssigner': started group factor (fold) assignment.")

        if len(self.stats.active_features) == 0:
            logger.warning("'GroupFactorAssigner': no active features found - SKIP")
            return

        self.assign_group_factors()

        logger.info("'GroupFactorAssigner': completed group factor (fold) assignment.")
