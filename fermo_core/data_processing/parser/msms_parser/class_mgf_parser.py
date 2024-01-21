"""Parses msms information from a .mgf-file.

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

from pyteomics import mgf

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.parser.msms_parser.abc_msms_parser import MsmsParser
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class MgfParser(MsmsParser):
    """Interface to parse MS/MS files in mgf format based on abstract baseclass."""

    def parse(
        self: Self, feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Parse a mgf style MS/MS file.

        Arguments:
            feature_repo: Repository holding individual features
            params: instance of ParameterManager holding user input

        Returns:
            A Repository object with modified features
        """
        logger.info(
            f"'MgfParser': started parsing of MS/MS data-containing file "
            f"'{params.MsmsParameters.filepath.name}'"
        )

        feature_repo = self.modify_features(feature_repo, params)

        logger.info(
            f"'MgfParser': completed parsing of MS/MS data-containing file "
            f"'{params.MsmsParameters.filepath.name}'"
        )

        return feature_repo

    def modify_features(
        self: Self, feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Modifies Feature objects by adding MS/MS information.

        Arguments:
            feature_repo: Repository holding individual features
            params: instance of ParameterManager holding user input

        Returns:
            A Repository object with modified features
        """
        with open(params.MsmsParameters.filepath) as infile:
            for spectrum in mgf.read(infile, use_index=False):
                try:
                    data = {
                        "f_id": int(spectrum.get("params").get("feature_id")),
                        "mz": spectrum.get("m/z array"),
                        "intens": spectrum.get("intensity array"),
                        "precursor_mz": spectrum.get("params").get("pepmass")[0],
                    }
                    feature = feature_repo.get(data["f_id"])
                    feature.Spectrum = self.create_spectrum_object(data)
                    feature_repo.modify(data["f_id"], feature)

                except KeyError:
                    logger.warning(
                        f"Could not add MS/MS spectrum with the feature ID "
                        f"'{spectrum.get('params').get('feature_id')}'. "
                        "This feature ID does not exist in the provided peaktable"
                        " - SKIP"
                    )

        return feature_repo
