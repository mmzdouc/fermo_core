"""Based on user input, run filetype-specific methods to parse data.

***

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
from typing import Tuple

from fermo_core.input_output.dataclass_params_handler import ParamsHandler
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder.class_general_feature_director import (
    GeneralFeatureDirector,
)
from fermo_core.data_processing.builder.class_samples_director import SamplesDirector


class Parser:
    """Interface to process different input file types"""

    @staticmethod
    def parse_peaktable(params: ParamsHandler) -> Tuple[Stats, Repository, Repository]:
        """Parse peaktable depending on format

        Args:
            params: holds paths to peaktables among other parameters

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
            Repository

        Notes:
            Expanding towards other peaktable formats requires to add an
            elif condition to parse correct peaktable
        """
        if params.peaktable_mzmine3 is not None:
            stats = Stats()
            stats.parse_mzmine3(params)

            feature_repo = Repository()
            for _, row in pd.read_csv(params.peaktable_mzmine3).iterrows():
                if row["id"] in stats.features:
                    feature_repo.add(
                        row["id"], GeneralFeatureDirector.construct_mzmine3(row)
                    )

            sample_repo = Repository()
            for s_id in stats.samples:
                sample_repo.add(
                    s_id,
                    SamplesDirector.construct_mzmine3(
                        s_id, pd.read_csv(params.peaktable_mzmine3), stats.features
                    ),
                )

            return stats, feature_repo, sample_repo

        # elif: entry for other peaktable formats

        else:
            raise Exception("Abort: No (compatible) peaktable found.")

    @staticmethod
    def parse_msms(
        params: ParamsHandler, stats: Stats, feature_repo: Repository
    ) -> Tuple[Stats, Repository,]:
        """Parse peaktable depending on format

        Args:
            params: holds paths to msms data among other parameters
            stats: class summarizing overall info on features and samples
            feature_repo: Repository holding individual features

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
            Repository

        Notes:
            Expanding towards other ms/ms formats requires to add an elif condition to
            parse correct peaktable
        """
        # TODO(MMZ): Fill this up
        pass
