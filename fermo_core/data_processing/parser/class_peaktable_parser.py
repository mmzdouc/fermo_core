"""Parses peaktable files depending on peaktable format.

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

from fermo_core.data_processing.builder_feature.class_general_feature_director import (
    GeneralFeatureDirector,
)
from fermo_core.data_processing.builder_sample.class_samples_director import (
    SamplesDirector,
)

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


class PeaktableParser:
    """Interface to parse different input peak tables.

    Attributes:
        peaktable_filepath: a filepath string
        peaktable_format: a peaktable format string
        rel_int_range: range to retain/exclude features
        ms2query_range: range to retain/exclude features for ms2query annotation
    """

    def __init__(
        self: Self,
        peaktable_filepath: str,
        peaktable_format: str,
        rel_int_range: Tuple[float, float],
        ms2query_range: Tuple[float, float],
    ):
        self.peaktable_filepath = peaktable_filepath
        self.peaktable_format = peaktable_format
        self.rel_int_range = rel_int_range
        self.ms2query_range = ms2query_range

    def parse(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Parses the peaktable based on format.

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
                Repository

        Notes:
            Adjust here for additional peaktable formats.
        """
        match self.peaktable_format:
            case "mzmine3":
                return self.parse_mzmine3()
            case _:
                logging.fatal("Could not recognize peaktable file - ABORT.")
                raise RuntimeError

    def parse_mzmine3(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Parse a mzmine3 style peaktable.

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
            Repository
        """
        logging.debug(
            f"Started parsing MZmine3-style peaktable" f"'{self.peaktable_filepath}.'"
        )

        logging.debug(
            f"Started creating Stats object from '{self.peaktable_filepath}'."
        )
        stats = Stats()
        stats.parse_mzmine3(
            self.peaktable_filepath, self.rel_int_range, self.ms2query_range
        )
        logging.debug(
            f"Completed creating Stats object from '{self.peaktable_filepath}'."
        )

        logging.debug(
            f"Started creating Feature object(s) from '{self.peaktable_filepath}'."
        )
        feature_repo = Repository()
        for _, row in pd.read_csv(self.peaktable_filepath).iterrows():
            if row["id"] in stats.features:
                feature_repo.add(
                    row["id"], GeneralFeatureDirector.construct_mzmine3(row)
                )
        logging.debug(
            f"Completed creating Feature object(s) from '{self.peaktable_filepath}'."
        )

        logging.debug(
            f"Started creating Sample object(s) from '{self.peaktable_filepath}'."
        )
        sample_repo = Repository()
        for s_id in stats.samples:
            sample_repo.add(
                s_id,
                SamplesDirector.construct_mzmine3(
                    s_id, pd.read_csv(self.peaktable_filepath), stats.features
                ),
            )
        logging.debug(
            f"Completed creating Sample object(s) from '{self.peaktable_filepath}'."
        )

        logging.debug(
            f"Completed parsing MZmine3-style peaktable '{self.peaktable_filepath}'."
        )

        return stats, feature_repo, sample_repo
