"""Parses MZMine3 peaktable file

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

import logging
from typing import Self

import pandas as pd

from fermo_core.data_processing.builder_feature.class_general_feature_director import (
    GeneralFeatureDirector,
)
from fermo_core.data_processing.builder_sample.class_samples_director import (
    SamplesDirector,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.parser.peaktable_parser.abc_peaktable_parser import (
    PeaktableParser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class PeakMzmine3Parser(PeaktableParser):
    """Interface to parse MZmine3 style peaktable."""

    def parse(
        self: Self, params: ParameterManager
    ) -> tuple[Stats, Repository, Repository]:
        """Parse a mzmine3 style peaktable.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
                Repository
        """
        logger.info(
            f"'PeakMzmine3Parser': started parsing MZmine3-style peaktable file "
            f"'{params.PeaktableParameters.filepath.name}'"
        )

        stats = self.extract_stats(params)

        feature_repo = self.extract_features(params)

        sample_repo = self.extract_samples(stats, params)

        logger.info(
            f"'PeakMzmine3Parser': completed parsing MZmine3-style peaktable file "
            f"'{params.PeaktableParameters.filepath.name}'"
        )

        return stats, feature_repo, sample_repo

    @staticmethod
    def extract_stats(params: ParameterManager) -> Stats:
        """Extract stats from MZmine3-style peaktable.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            A Stats object summarizing general information about peaktable.
        """
        stats = Stats()
        stats.parse_mzmine3(params)
        return stats

    @staticmethod
    def extract_features(params: ParameterManager) -> Repository:
        """Extract features from MZmine3-style peaktable.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            A Repository object containing Feature objects
        """
        feature_repo = Repository()
        for _, row in pd.read_csv(params.PeaktableParameters.filepath).iterrows():
            feature_repo.add(row["id"], GeneralFeatureDirector.construct_mzmine3(row))
        return feature_repo

    @staticmethod
    def extract_samples(stats: Stats, params: ParameterManager) -> Repository:
        """Extract samples from MZmine3-style peaktable.

        Arguments:
            stats: An instance of the Stats class
            params: An instance of the ParameterManager class

        Returns:
            A Repository object containing Sample objects
        """
        sample_repo = Repository()
        df = pd.read_csv(params.PeaktableParameters.filepath)
        for s_id in stats.samples:
            sample_repo.add(
                s_id,
                SamplesDirector.construct_mzmine3(s_id, df),
            )
        return sample_repo
