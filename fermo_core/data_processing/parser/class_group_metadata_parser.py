"""Parses group metadata information files depending on file format.

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
from typing import Self, Tuple

from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository


class GroupMetadataParser:
    """Interface to parse different input group metadata files.

    Attributes:
        group_filepath: a file path string
        group_format: a string indicating the format of the grouping file
    """

    def __init__(
        self: Self,
        group_filepath: str,
        group_format: str,
    ):
        self.group_filepath = group_filepath
        self.group_format = group_format

    def parse(
        self: Self, stats: Stats, sample_repo: Repository
    ) -> Tuple[Stats, Repository]:
        """Parses the group metadata information based on format.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects

        Returns:
            Tuple containing Stats and Sample repository objects with added group info.

        Notes:
            Adjust here for additional group formats.
        """
        match self.group_format:
            case "fermo":
                return self.parse_fermo(stats, sample_repo)
            case _:
                logging.warning(
                    "Could not recognize group metadata file format - SKIP."
                )
                return stats, sample_repo

    def parse_fermo(
        self: Self, stats: Stats, sample_repo: Repository
    ) -> Tuple[Stats, Repository]:
        """Parses a fermo-style group metadata file.

        Arguments:
            stats: Stats object holding various information of overall data
            sample_repo: Repository holding Sample objects

        Returns:
            Tuple containing Stats and Sample repository objects with added group info.
        """
        logging.debug(
            f"Started parsing group metadata information from '{self.group_filepath}'."
        )
        df = pd.read_csv(self.group_filepath)
        for _, row in df.iterrows():
            sample_id = row["sample_name"]
            stats = self.remove_sample_id_from_group_default(stats, sample_id)
            for group_id in row:
                if group_id == sample_id:
                    pass
                elif group_id not in stats.groups:
                    stats.groups[group_id] = {sample_id}
                    sample_repo = self.add_group_id_to_sample_repo(
                        sample_repo, sample_id, group_id
                    )
                else:
                    stats.groups[group_id].add(sample_id)
                    sample_repo = self.add_group_id_to_sample_repo(
                        sample_repo, sample_id, group_id
                    )

        logging.debug(
            f"Completed parsing of group metadata from 'fermo'-style file "
            f"'{self.group_filepath}'."
        )
        return stats, sample_repo

    def remove_sample_id_from_group_default(
        self: Self, stats_obj: Stats, sample_id: str
    ) -> Stats:
        """Removes the sample id from the group 'DEFAULT' in Stats object.

        Arguments:
            stats_obj: holds group information among other info
            sample_id: a sample identifier string

        Returns:
            A (modified) stats object
        """
        try:
            stats_obj.groups.get("DEFAULT").remove(sample_id)
            return stats_obj
        except KeyError:
            logging.warning(
                f"Could not find sample ID '{sample_id}' from group metadata file "
                f"'{self.group_filepath}' "
                f"in the previously processed peaktable file."
                f"Are you sure that the files match?"
            )
            return stats_obj

    def add_group_id_to_sample_repo(
        self: Self, sample_repo: Repository, sample_id: str, group_id: str
    ) -> Repository:
        """Adds the group information to the Sample objects in the Repository.

        Arguments:
            sample_repo: Repository holding sample objects
            sample_id: a sample identifier string
            group_id: a group identifier string

        Returns:
            A (modified) Repository object
        """
        try:
            sample = sample_repo.get(sample_id)
            sample.groups.add(group_id)
            if "DEFAULT" in sample.groups:
                sample.groups.remove("DEFAULT")
            sample_repo.modify(sample_id, sample)
            return sample_repo
        except KeyError:
            logging.warning(
                f"Could not find sample ID '{sample_id}' from group metadata file "
                f"'{self.group_filepath}' "
                f"in the previously processed peaktable file."
                f"Are you sure that the files match?"
            )
            return sample_repo