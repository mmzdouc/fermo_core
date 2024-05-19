"""Parses fermo-style group metadata file

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
from typing import Any, Self

from pydantic import BaseModel

from fermo_core.data_processing.class_stats import Group, Stats

logger = logging.getLogger("fermo_core")


class MetadataFermoParser(BaseModel):
    """Interface to parse fermo-style group metadata file.

    Attributes:
        stats: a Stats object instance
        df: a Pandas dataframe to extract data from
    """

    stats: Stats
    df: Any

    def return_stats(self: Self) -> Stats:
        """Return the modified objects

        Returns:
             The modified stats object
        """
        return self.stats

    def validate_sample_names(self: Self):
        """Validate overlap of sample names from peaktable and group metadata file

        Raises:
            RuntimeError: sample names in df do not match peaktable-extracted ones
        """
        diff_samples = set(self.df["sample_name"]).difference(set(self.stats.samples))

        if len(diff_samples) != 0:
            raise RuntimeError(
                f"'MetadataFermoParser': sample names in group metadata file do not "
                f"match the ones extracted from the peaktable. Offending sample names: "
                f"'{', '.join(diff_samples)}' - SKIP."
            )

    def unassign_default_set(self: Self):
        """Validate that all samples from peaktable can be found in metadata file"""
        self.stats.GroupMData.default_s_ids = (
            self.stats.GroupMData.default_s_ids.difference(set(self.df["sample_name"]))
        )

        if len(self.stats.GroupMData.default_s_ids) != 0:
            logger.warning(
                f"'MetadataFermoParser': group metadata assignment not found for all "
                f"samples. The following samples will not partake in group comparison: "
                f"'{', '.join(self.stats.GroupMData.default_s_ids)}'"
            )

    def extract_blanks(self: Self):
        """Extract all samples that were assigned the signal word 'BLANK'."""
        result = self.df.isin(["BLANK"])
        df_blank = self.df[result.any(axis=1)]
        df_filtered = self.df[~result.any(axis=1)]

        if len(df_filtered) < len(self.df):
            self.stats.GroupMData.blank_s_ids = set(df_blank["sample_name"])
            self.stats.GroupMData.nonblank_s_ids = set(df_filtered["sample_name"])
            self.df = df_filtered
            logger.debug(
                f"'MetadataFermoParser': Samples marked as 'BLANK' detected. The "
                f"following samples will not partake in group comparisons: "
                f"{', '.join(self.stats.GroupMData.blank_s_ids)}'"
            )
        else:
            return

    def prepare_ctgrs(self: Self):
        """Extract categories and groups from dataframe and assign to stats"""
        ctgrs = [col for col in self.df.columns if col != "sample_name"]
        for ctg in ctgrs:
            self.stats.GroupMData.ctgrs[ctg] = {}
            for group in self.df[ctg].unique():
                s_ids = self.df[self.df[ctg] == group]["sample_name"].tolist()
                if group in self.stats.GroupMData.ctgrs[ctg]:
                    self.stats.GroupMData.ctgrs[ctg][group].s_ids.update(set(s_ids))
                else:
                    self.stats.GroupMData.ctgrs[ctg][group] = Group(s_ids=set(s_ids))

    def run_parser(self: Self):
        """Parse the corresponding metadata file and assign data"""
        logger.info(
            "'MetadataFermoParser': started parsing fermo-style group metadata file."
        )
        self.df = self.df.astype(str)
        self.validate_sample_names()
        self.unassign_default_set()
        self.extract_blanks()
        self.prepare_ctgrs()

        logger.info(
            "'MetadataFermoParser': completed parsing fermo-style group metadata file."
        )
