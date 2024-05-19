"""Assign group information.

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
from typing import Self

from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats

logger = logging.getLogger("fermo_core")


class GroupAssigner(BaseModel):
    """Pydantic-based class to organize group metadata assignment.

    Attributes:
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
    """

    stats: Stats
    features: Repository

    def return_attrs(self: Self) -> tuple[Stats, Repository]:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing modified Stats and Feature Repository objects.
        """
        return self.stats, self.features

    def assign_groups(self: Self):
        """Assign the group information to features and stats"""
        for f_id in self.stats.active_features:
            if f_id in self.stats.GroupMData.blank_f_ids:
                continue

            feature = self.features.get(f_id)
            feature.groups = {}
            for ctgr, cat_dict in self.stats.GroupMData.ctgrs.items():
                for group, val in cat_dict.items():
                    if not val.s_ids.isdisjoint(feature.samples):
                        self.stats.GroupMData.ctgrs[ctgr][group].f_ids.add(f_id)
                        if ctgr in feature.groups:
                            feature.groups[ctgr].add(group)
                        else:
                            feature.groups[ctgr] = {group}

            self.features.modify(f_id, feature)

    def run_analysis(self: Self):
        """Run group assignment analysis"""
        logger.info("'GroupAssigner': started group assignment.")

        if len(self.stats.active_features) == 0:
            logger.warning("'GroupAssigner': no active features found - SKIP")
            return

        self.assign_groups()

        logger.info("'GroupAssigner': completed group assignment.")
