"""Parses phenotype files depending on file format.

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


class PhenotypeParser:
    """Interface to parse different input peak tables.

    Attributes:
        phenotype_filepath: a filepath string
        phenotype_format: a peaktable format string
        phenotype_mode: indicating the data type
        phenotype_algorithm: algorithm to use for processing
    """

    def __init__(
        self: Self,
        phenotype_filepath: str,
        phenotype_format: str,
        phenotype_mode: str,
        phenotype_algorithm: str,
    ):
        self.phenotype_filepath = phenotype_filepath
        self.phenotype_format = phenotype_format
        self.phenotype_mode = phenotype_mode
        self.phenotype_algorithm = phenotype_algorithm

    def parse(
        self: Self, stats: Stats, sample_repo: Repository
    ) -> Tuple[Stats, Repository]:
        """Parses the phenotype/bioactivity information based on file format.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects

        Returns:
            Tuple containing Stats and Sample repository objects with added bioactivity
            info.

        Notes:
            Adjust here for additional phenotype formats.
        """
        match self.phenotype_format:
            case "fermo":
                return self.parse_fermo(stats, sample_repo)
            case _:
                logging.warning(
                    "Could not recognize phenotype/bioactivity data file format - SKIP."
                )
                return stats, sample_repo

    def parse_fermo(
        self: Self, stats: Stats, sample_repo: Repository
    ) -> Tuple[Stats, Repository]:
        """Parses a fermo-style phenotype/bioactivity data file.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects

        Returns:
            Tuple containing Stats and Sample repository objects with added
            phenotype/bioactivity info.
        """
        logging.debug(
            f"Started parsing phenotype/bioactivity data from "
            f"'{self.phenotype_filepath}'."
        )
        df = pd.read_csv(self.phenotype_filepath)

        experiments = dict()
        for col in df.columns:
            if col != "sample_name":
                experiments[col] = []

        # Uses the column (experiment) names to extract sample measurement information
        for experiment in experiments.keys():
            df_actives = df[df[experiment] != 0]
            for _, row in df_actives.iterrows():
                experiments[experiment].append(row["sample_name"])
                sample_repo = self.add_phenotype_to_sample(
                    sample_repo,
                    row["sample_name"],
                    experiment,
                    row[experiment],
                    concentration=1,
                )

        # Add data to stats object
        if not isinstance(stats.phenotypes, dict):
            stats.phenotypes = dict()
        stats.phenotype_format = self.phenotype_format
        stats.phenotype_mode = self.phenotype_mode
        stats.phenotype_algorithm = self.phenotype_algorithm
        for experiment in experiments:
            stats.phenotypes[experiment] = tuple(experiments.get(experiment))

        logging.debug(
            f"Completed parsing of phenotype/bioactivity data from 'fermo'-style file "
            f"'{self.phenotype_filepath}'."
        )
        return stats, sample_repo

    def add_phenotype_to_sample(
        self: Self,
        sample_repo: Repository,
        sample_id: str,
        experiment: str,
        measurement: int | float,
        concentration: int | float,
    ) -> Repository:
        """Adds phenotype information to the Sample objects in the Repository.

        Arguments:
            sample_repo: Repository holding sample objects
            sample_id: a sample identifier
            experiment: an experiment/measurement type identifier
            measurement: the measurement for the sample
            concentration: at which concentration the measurement was made

        Returns:
            A (modified) Repository object
        """
        try:
            sample = sample_repo.get(sample_id)
            if not isinstance(sample.phenotypes, dict):
                sample.phenotypes = dict()
            sample.phenotypes[experiment] = Phenotype(
                value=measurement,
                concentration=concentration,
            )
            sample_repo.modify(sample_id, sample)
            return sample_repo
        except KeyError:
            logging.warning(
                f"Could not find sample ID '{sample_id}' from "
                "phenotype/bioactivity file "
                f"'{self.phenotype_filepath}' "
                f"in the previously processed peaktable file."
                f"Are you sure that the files match?"
            )
            return sample_repo
