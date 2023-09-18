"""Parses msms information files depending on msms file format.

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
from pyteomics import mgf
from typing import Self

from fermo_core.data_processing.class_repository import Repository


class MsmsParser:
    """Interface to parse different input msms files.

    Attributes:
        msms_filepath: a file path string
        msms_format: a string indicating the format of the msms file
    """

    def __init__(
        self: Self,
        msms_filepath: str,
        msms_format: str,
    ):
        self.msms_filepath = msms_filepath
        self.msms_format = msms_format

    def parse(self: Self, feature_repo: Repository) -> Repository:
        """Parses the msms information based on format.

        Arguments:
            feature_repo: Repository holding individual features

        Returns:
            A (modified) Feature Repository

        Notes:
            Adjust here for additional msms formats.
        """
        logging.info("Started MS/MS information parsing.")

        match self.msms_format:
            case "mgf":
                logging.debug(
                    f"Started parsing mgf-style MS/MS file" f"'{self.msms_filepath}.'"
                )
                return self.parse_mgf(feature_repo)
            case _:
                logging.warning(
                    "No MS/MS file provided - functionality of FERMO is limited. "
                    "For more information, consult the documentation."
                )
                return feature_repo

    def parse_mgf(self: Self, feature_repo: Repository) -> Repository:
        """Parses a mgf file for MS/MS information and adds info to molecular features.

        Arguments:
            feature_repo: Repository holding individual features

        Returns:
            A (modified) Feature Repository

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling
        """
        logging.debug(f"Started adding MS/MS information from '{self.msms_filepath}'.")
        with open(self.msms_filepath) as infile:
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
                    logging.warning(
                        f"Could not add MS/MS spectrum with the feature ID "
                        f"'{spectrum.get('params').get('feature_id')}'. "
                        "This feature ID does not exist in peaktable or was filtered "
                        "out by 'rel_int_range' settings."
                    )
        logging.debug(f"Completed parsing of MS/MS '.mgf' file '{self.msms_filepath}'.")
        return feature_repo
