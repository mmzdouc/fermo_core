"""Organize the calling of data analysis modules.

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
from typing import Self

from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class BlankAssigner(BaseModel):
    """Pydantic-based class for performing blank assignment analysis

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository

    def return_attrs(self: Self) -> tuple[Stats, Repository]:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing modified Stats and Feature Repository objects.
        """
        return self.stats, self.features

    def calc_rprsnt(self: Self, vals: list) -> float:
        """Calculate representative value from list using user-specified algorithm

        Arguments:
            vals: a list of int values representing height or area

        Returns:
            The determined representative value

        Raises:
            RuntimeError: unexpected algorithm
        """
        if self.params.BlankAssignmentParameters.algorithm == "mean":
            return float(statistics.mean(vals))
        elif self.params.BlankAssignmentParameters.algorithm == "median":
            return float(statistics.median(vals))
        elif self.params.BlankAssignmentParameters.algorithm == "maximum":
            return float(max(vals))
        else:
            raise RuntimeError("'BlankAssigner': unexpected algorithm found - SKIP.")

    def collect_area(self: Self, f_id: int) -> tuple[list, list]:
        """Collect area for nonblanks vs blanks

        Returns:
            A tuple of [values from nonblanks] and [values from blanks]

        Raises:
            RuntimeError: one of blanks or non-blanks is empty
        """
        non_blks = []
        blks = []
        feature = self.features.get(f_id)
        for obj in feature.area_per_sample:
            if obj.s_id in self.stats.GroupMData.blank_s_ids:
                blks.append(obj.value)
            else:
                non_blks.append(obj.value)

        if len(non_blks) == 0 or len(blks) == 0:
            raise RuntimeError(f"'BlankAssigner': feature id '{f_id}' invalid area.")

        return non_blks, blks

    def collect_height(self: Self, f_id: int) -> tuple[list, list]:
        """Collect height for nonblanks vs blanks

        Returns:
            A tuple of [values from nonblanks] and [values from blanks]

        Raises:
            RuntimeError: one of blanks or non-blanks is empty
        """
        non_blks = []
        blks = []
        feature = self.features.get(f_id)
        for obj in feature.height_per_sample:
            if obj.s_id in self.stats.GroupMData.blank_s_ids:
                blks.append(obj.value)
            else:
                non_blks.append(obj.value)

        if len(non_blks) == 0 or len(blks) == 0:
            raise RuntimeError(f"'BlankAssigner': feature id '{f_id}' invalid height.")

        return non_blks, blks

    def determine_blank(self: Self):
        """Determine blank/nonblank status of features based on presence in samples"""
        for f_id in self.stats.active_features:
            feature = self.features.get(f_id)
            if feature.samples.isdisjoint(self.stats.GroupMData.blank_s_ids):
                feature.blank = False
                self.features.modify(f_id, feature)
                self.stats.GroupMData.nonblank_f_ids.add(f_id)
            elif feature.samples.isdisjoint(self.stats.GroupMData.nonblank_s_ids):
                feature.blank = True
                self.features.modify(f_id, feature)
                self.stats.GroupMData.blank_f_ids.add(f_id)
            else:
                if self.params.BlankAssignmentParameters.value == "area":
                    non_blks, blks = self.collect_area(f_id)
                else:
                    non_blks, blks = self.collect_height(f_id)

                if (
                    self.calc_rprsnt(non_blks) / self.calc_rprsnt(blks)
                ) >= self.params.BlankAssignmentParameters.factor:
                    feature.blank = False
                    self.features.modify(f_id, feature)
                    self.stats.GroupMData.nonblank_f_ids.add(f_id)
                else:
                    feature.blank = True
                    self.features.modify(f_id, feature)
                    self.stats.GroupMData.blank_f_ids.add(f_id)

    def validate_assignment(self):
        """Validate if assignment has been performed properly

        Raises:
            RuntimeError
        """
        if (
            len(self.stats.GroupMData.blank_f_ids)
            + len(self.stats.GroupMData.nonblank_f_ids)
        ) != len(self.stats.active_features):
            raise RuntimeError(
                "'BlankAssigner': sum of 'blank' and 'non-blank' does not equal the "
                "total number of active features."
            )

    def run_analysis(self: Self):
        """Run blank assignment analysis"""
        logger.info("'BlankAssigner': started blank assignment.")

        if len(self.stats.active_features) == 0:
            logger.warning("'BlankAssigner': no active features found - SKIP")
            return

        self.determine_blank()
        self.validate_assignment()

        logger.info("'BlankAssigner': completed blank assignment.")
