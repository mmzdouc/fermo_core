"""Parses fermo-style phenotype data file.

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
import pandas as pd
import logging
from typing import Self, Tuple

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_sample.dataclass_sample import Phenotype
from fermo_core.data_processing.parser.phenotype_parser.acb_phenotype_parser import (
    PhenotypeParser,
)

from fermo_core.input_output.class_parameter_manager import ParameterManager


class PhenotypeFermoParser(PhenotypeParser):
    """Interface to parse fermo-style phenotype file."""

    def parse(
        self: Self, stats: Stats, sample_repo: Repository, params: ParameterManager
    ) -> Tuple[Stats, Repository]:
        """Parses a fermo-style phenotype/bioactivity data file.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects
            params: Instance of ParameterManager holding user input

        Returns:
            Tuple containing Stats and Sample repository objects with added
            phenotype/bioactivity info.

        Notes:
            the fermo bioactivity/phenotype data format assumes the same
            concentration of all experiments (1).
            TODO(MMZ 13.12.23): fermo bioactivity format needs to be changed.
        """
        logging.info(
            f"'PhenotypeFermoParser': started parsing fermo-style phenotype data file "
            f"'{params.PhenotypeParameters.filepath.name}'"
        )

        df = pd.read_csv(params.PhenotypeParameters.filepath)

        assays = dict()
        for assay_type in df.columns:
            if assay_type != "sample_name":
                assays[assay_type] = []

        for assay in assays.keys():
            df_actives = df[df[assay] != 0]
            for _, row in df_actives.iterrows():
                assays[assay].append(row["sample_name"])
                sample_repo = self.add_phenotype_to_sample(
                    sample_repo,
                    row["sample_name"],
                    assay,
                    row[assay],
                    concentration=1,
                )

        if not isinstance(stats.phenotypes, dict):
            stats.phenotypes = dict()

        for assay in assays:
            stats.phenotypes[assay] = tuple(assays.get(assay))

        logging.info(
            f"'PhenotypeFermoParser': completed parsing fermo-style phenotype data file"
            f" '{params.PhenotypeParameters.filepath.name}'"
        )

        return stats, sample_repo

    @staticmethod
    def add_phenotype_to_sample(
        sample_repo: Repository,
        sample_id: str,
        assay: str,
        measurement: int | float,
        concentration: int | float,
    ) -> Repository:
        """Adds phenotype information to the Sample objects in the Repository.

        Arguments:
            sample_repo: Repository holding sample objects
            sample_id: a sample identifier
            assay: an experiment/measurement type identifier
            measurement: the measurement for the sample
            concentration: at which concentration the measurement was made

        Returns:
            A (modified) Repository object
        """
        try:
            sample = sample_repo.get(sample_id)

            if not isinstance(sample.phenotypes, dict):
                sample.phenotypes = dict()

            sample.phenotypes[assay] = Phenotype(
                value=measurement,
                conc=concentration,
            )

            sample_repo.modify(sample_id, sample)

            return sample_repo
        except KeyError:
            logging.warning(
                f"Could not find sample ID '{sample_id}' from "
                "phenotype/bioactivity file "
                f"in the previously processed peaktable file."
                f"Is this the correct file?"
            )
            return sample_repo
