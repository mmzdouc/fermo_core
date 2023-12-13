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

from fermo_core.input_output.class_parameter_manager import ParameterManager

# TODO(MMZ 13.12.23): continue here - fix class, add test adding reference


class PhenotypeParser:
    """Interface to parse different input peak tables."""

    def parse(
        self: Self, stats: Stats, sample_repo: Repository, params: ParameterManager
    ) -> Tuple[Stats, Repository]:
        """Parses the phenotype/bioactivity information based on file format.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects
            params: Instance of ParameterManager holding user input

        Returns:
            Tuple of Stats and Sample repository, modified for bioactivity info.

        Notes:
            Adjust here for additional phenotype formats.

        # TODO(MMZ 13.12.23): Cover with tests
        """
        match params.PhenotypeParameters.format:
            case "fermo":
                return self.parse_fermo(stats, sample_repo, params)
            case _:
                return stats, sample_repo

    def parse_fermo(
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

        # TODO(MMZ 13.12.23): Cover with tests
        """
        logging.info(
            f"'PhenotypeParser': started parsing fermo-style phenotype data file "
            f"'{params.PhenotypeParameters.filepath.name}'"
        )

        df = pd.read_csv(params.PhenotypeParameters.filepath)

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

        if not isinstance(stats.phenotypes, dict):
            stats.phenotypes = dict()

        for experiment in experiments:
            stats.phenotypes[experiment] = tuple(experiments.get(experiment))

        logging.info(
            f"'PhenotypeParser': completed parsing fermo-style phenotype data file "
            f"'{params.PhenotypeParameters.filepath.name}'"
        )

        return stats, sample_repo

    @staticmethod
    def add_phenotype_to_sample(
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

        # TODO(MMZ 13.12.23): Cover with tests
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
                f"in the previously processed peaktable file."
                f"Is this the correct file?"
            )
            return sample_repo
