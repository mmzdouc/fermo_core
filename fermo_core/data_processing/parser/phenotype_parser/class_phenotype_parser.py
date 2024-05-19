"""Parses phenotype data files.

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

from fermo_core.data_processing.class_stats import PhenoData, SamplePhenotype, Stats

logger = logging.getLogger("fermo_core")


class PhenotypeParser(BaseModel):
    """Interface to parse phenotype files.

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

    @staticmethod
    def message(msg: str):
        logger.info(f"'PhenotypeParser': {msg} parsing phenotype data file.")

    def validate_sample_names(self: Self):
        """Validate overlap of sample names from peaktable and phenotype file

        Raises:
            RuntimeError: sample names in df do not match peaktable-extracted ones
        """
        diff_samples = set(self.df["sample_name"]).difference(set(self.stats.samples))

        if len(diff_samples) != 0:
            raise RuntimeError(
                f"'PhenotypeParser': sample names in phenotype file do not "
                f"match the ones extracted from the peaktable. Offending sample names: "
                f"'{', '.join(diff_samples)}'."
            )

    def parse_qualitative(self: Self):
        """Parse data from qualitative phenotype file

        Raises:
            RuntimeError: no negative (inactive) samples: no active/inactive
            determination possible
        """
        s_ids_active = set(self.df["sample_name"])
        s_negative = set(self.stats.samples).difference(s_ids_active)

        if len(s_negative) == 0:
            raise RuntimeError(
                "'PhenotypeParser': no negative (inactive) samples found and "
                "therefore, factor (fold)-based phenotype determination not possible."
            )

        self.stats.phenotypes = [
            PhenoData(
                datatype="qualitative",
                category="qualitative",
                s_phen_data=[SamplePhenotype(s_id=s_id) for s_id in s_ids_active],
                s_negative=s_negative,
            )
        ]

    def parse_quantitative_percentage(self: Self, algorithm: str):
        """Parse data from quantitative percentage phenotype file

        Arguments:
            algorithm: the algorithm to summarize duplicate measurements per sample
                for each assay.

        """
        assay_cols = [assay for assay in self.df.columns if assay.startswith("assay:")]

        for assay in assay_cols:
            self.df.loc[self.df[assay] < 0, assay] = 0

        self.stats.phenotypes = []

        for num, assay in enumerate(assay_cols):
            self.stats.phenotypes.append(
                PhenoData(datatype="quantitative-percentage", category=assay)
            )

            if algorithm == "mean":
                summarized_vals = self.df.groupby("sample_name")[assay].mean()
            else:
                summarized_vals = self.df.groupby("sample_name")[assay].median()

            for idx, val in summarized_vals.items():
                self.stats.phenotypes[num].s_phen_data.append(
                    SamplePhenotype(s_id=idx, value=val)
                )

    def parse_quantitative_concentration(self: Self, algorithm: str):
        """Parse data from quantitative concentration phenotype file

        Arguments:
            algorithm: the algorithm to summarize duplicate measurements per sample
                for each assay.
        """
        assay_cols = [assay for assay in self.df.columns if assay.startswith("assay:")]

        self.stats.phenotypes = []

        for num, assay in enumerate(assay_cols):
            self.stats.phenotypes.append(
                PhenoData(datatype="quantitative-concentration", category=assay)
            )

            if algorithm == "mean":
                summarized_vals = self.df.groupby("sample_name")[assay].mean()
            else:
                summarized_vals = self.df.groupby("sample_name")[assay].median()

            for idx, val in summarized_vals.items():
                self.stats.phenotypes[num].s_phen_data.append(
                    SamplePhenotype(s_id=idx, value=val)
                )
