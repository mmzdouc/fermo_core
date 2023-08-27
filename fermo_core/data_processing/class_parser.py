"""Based on user input, run filetype-specific methods to parse data.

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

import pandas as pd
from pyteomics import mgf
from typing import Tuple, Self

from fermo_core.input_output.dataclass_params_handler import ParamsHandler
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.class_general_feature_director import (
    GeneralFeatureDirector,
)
from fermo_core.data_processing.builder_sample.class_samples_director import (
    SamplesDirector,
)


class Parser:
    """Interface to process different input file types"""

    @staticmethod
    def parse_peaktable_mzmine3(
        params: ParamsHandler,
    ) -> Tuple[Stats, Repository, Repository]:
        """Parse a mzmine3 style peaktable.

        Args:
            params: holds paths to peak tables among other parameters

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
            Repository
        """
        stats = Stats()
        stats.parse_mzmine3(params)
        logging.debug(f"Created Stats object from {params.peaktable_mzmine3}.")

        feature_repo = Repository()
        for _, row in pd.read_csv(params.peaktable_mzmine3).iterrows():
            if row["id"] in stats.features:
                feature_repo.add(
                    row["id"], GeneralFeatureDirector.construct_mzmine3(row)
                )
        logging.debug(f"Crated Feature object(s) from {params.peaktable_mzmine3}.")

        sample_repo = Repository()
        for s_id in stats.samples:
            sample_repo.add(
                s_id,
                SamplesDirector.construct_mzmine3(
                    s_id, pd.read_csv(params.peaktable_mzmine3), stats.features
                ),
            )
        logging.debug(f"Crated Sample object(s) from {params.peaktable_mzmine3}.")

        logging.info(f"Completed parsing of peaktable '{params.peaktable_mzmine3}'.")
        return stats, feature_repo, sample_repo

    def parse_peaktable(
        self: Self, params: ParamsHandler
    ) -> Tuple[Stats, Repository, Repository]:
        """Call peaktable parser for appropriate format

        Args:
            params: holds paths to peak tables among other parameters

        Returns:
            A tuple with an instance of Stats, a Feature Repository, and a Sample
            Repository

        Notes:
            Expanding towards other peaktable formats requires to add an
            elif condition to parse correct peaktable
        """
        if params.peaktable_mzmine3 is not None:
            logging.debug(f"Peaktable {params.peaktable_mzmine3} is in MZmine3 format.")
            return self.parse_peaktable_mzmine3(params)
        else:
            try:
                raise RuntimeError("Abort: No peaktable found.")
            except RuntimeError as e:
                logging.error(str(e))
                raise e

    @staticmethod
    def parse_msms_mgf(params: ParamsHandler, feature_repo: Repository) -> Repository:
        """Parse MS/MS information from a .mgf file.

        Args:
            params: holds paths to msms data among other parameters
            feature_repo: Repository holding individual features

        Returns:
            A Repository containing Features with added MS2 spectra.

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling

        """
        with open(params.msms_mgf) as infile:
            for spectrum in mgf.read(infile, use_index=False):
                try:
                    feature = feature_repo.get(
                        int(spectrum.get("params").get("feature_id"))
                    )
                    feature.msms = (
                        tuple(spectrum.get("m/z array").tolist()),
                        tuple(spectrum.get("intensity array").tolist()),
                    )
                    feature_repo.modify(
                        int(spectrum.get("params").get("feature_id")), feature
                    )
                except KeyError:
                    logging.info(
                        f"Could not add MS/MS spectrum with the feature ID "
                        f"'{spectrum.get('params').get('feature_id')}'. "
                        "This feature ID does not exist in peaktable or was filtered "
                        "out."
                    )

        logging.info(
            f"Completed parsing of MS/MS .mgf file '{params.peaktable_mzmine3}'."
        )
        return feature_repo

    def parse_msms(
        self: Self, params: ParamsHandler, feature_repo: Repository
    ) -> Repository:
        """Parse MS/MS file depending on format.

        Args:
            params: holds paths to msms data among other parameters
            feature_repo: Repository holding individual features

        Returns:
            Repository containing the features with added MS2 information

        Notes:
            Expanding towards other ms/ms formats requires to add an elif condition to
            parse correct peaktable
        """
        if params.msms_mgf is not None:
            logging.debug(f"MS/MS file '{params.msms_mgf}' is in '.mgf' format.")
            return self.parse_msms_mgf(params, feature_repo)
        else:
            logging.warning(
                "No MS/MS file provided - functionality of FERMO is limited. "
                "For more information, consult the documentation."
            )
            return feature_repo

    @staticmethod
    def parse_group_mzmine3(df: pd.DataFrame, stats: Stats, sample_repo: Repository):
        """Parse group metadata/information from a fermo-style group file.

        Args:
            df: the group metadata file as Pandas DataFrame
            stats: holds stats and metadata about analysis run, features and samples
            sample_repo: Repository holding individual samples

        Returns:
            Tuple containing Stats and Sample repository objects with added group info.

        Notes:
            Adding group info to features and any other calculation are performed later
            in 'data analysis'.
        """

        def _remove_sample_id_from_group_general(stats_obj: Stats, s_id: str) -> Stats:
            try:
                stats_obj.groups["DEFAULT"].remove(s_id)
            except ValueError:
                logging.warning(
                    f"Could not find sample ID '{s_id}' from group metadata file "
                    f"in the previously processed peaktable file."
                    f"Are you sure that the files match?"
                )
            return stats_obj

        def _add_group_id_to_sample_repo(samples: Repository) -> Repository:
            sample = samples.get(sample_id)
            sample.groups.add(group_id)
            if "DEFAULT" in sample.groups:
                sample.groups.remove("DEFAULT")
            return samples.modify(sample_id, sample)

        # TODO(MMZ): Write the tests for this function right away

        for _, row in df.iterrows():
            sample_id = row["sample_name"]
            stats = _remove_sample_id_from_group_general(stats, sample_id)
            for group_id in row:
                if group_id == sample_id:
                    pass
                elif group_id not in stats.groups:
                    stats.groups[group_id] = [sample_id]
                    sample_repo = _add_group_id_to_sample_repo(sample_repo)
                else:
                    stats.groups[group_id].append(sample_id)
                    sample_repo = _add_group_id_to_sample_repo(sample_repo)

        logging.info("Completed parsing of fermo-style group metadata file.")
        return stats, sample_repo

    def parse_group_metadata(
        self: Self,
        params: ParamsHandler,
        stats: Stats,
        sample_repo: Repository,
    ):
        """Parse group/metadata file depending on format.

        Args:
            params: holds paths to file, among other information
            stats: holds stats and metadata about analysis run, features and samples
            sample_repo: Repository holding individual samples

        Returns:
            Tuple containing Stats and Sample repository objects with added group info.

        Notes:
            Once additional group metadata formats are adopted,
             they need to be added here.
        """
        if params.group_fermo is not None:
            logging.debug(
                f"Group metadata file '{params.group_fermo}' is in FERMO format."
            )
            return self.parse_group_mzmine3(
                pd.read_csv(params.group_fermo), stats, sample_repo
            )
        else:
            logging.warning(
                "No group metadata file provided. Sample grouping is not performed."
            )
            return stats, sample_repo
