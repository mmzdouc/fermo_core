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
from fermo_core.input_output.class_parameter_manager import ParameterManager


class MsmsParser:
    """Interface to parse different input msms files."""

    def parse(
        self: Self, feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Parses the msms information based on format.

        Arguments:
            feature_repo: Repository holding individual features
            params: instance of ParameterManager holding user input

        Returns:
            A Repository object with modified features
        TODO(MMZ 13.12.23): Cover with tests
        """
        match params.MsmsParameters.format:
            case "mgf":
                return self.parse_mgf(feature_repo, params)
            case _:
                return feature_repo

    @staticmethod
    def parse_mgf(feature_repo: Repository, params: ParameterManager) -> Repository:
        """Parses a mgf file for MS/MS information and adds info to molecular features.

        Arguments:
            feature_repo: Repository holding individual features
            params: instance of ParameterManager holding user input

        Returns:
            A Repository object with modified features
        TODO(MMZ 13.12.23): Cover with tests
        """
        logging.info(
            f"'MsmsParser': started parsing MS/MS-data containing .mgf-file "
            f"'{params.MsmsParameters.filepath.name}'"
        )

        with open(params.MsmsParameters.filepath) as infile:
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

        logging.info(
            f"'MsmsParser': completed parsing MS/MS-data containing .mgf-file "
            f"'{params.MsmsParameters.filepath.name}'"
        )

        return feature_repo
