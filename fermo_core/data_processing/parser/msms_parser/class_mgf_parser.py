"""Parses msms information from a .mgf-file.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

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

from pydantic import BaseModel
from pyteomics import mgf

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils

logger = logging.getLogger("fermo_core")


class MgfParser(BaseModel):
    """Pydantic-based class to parse MS/MS files in mgf format.

    Attributes:
        params: a ParameterManager object containing analysis parameters
        features: a Repository object containing feature objects
    """

    params: ParameterManager
    features: Repository

    def return_features(self: Self) -> Repository:
        """Returns modified feature objects

        Returns:
            The modified feature objects
        """
        return self.features

    def modify_features(self: Self):
        """Modifies Feature objects by adding MS/MS information.

        Data is read using pyteomics.mgf() and only then converted to
        matchms.Spectrum object to have better control over data import and filtering.
        """
        with open(self.params.MsmsParameters.filepath) as infile:
            for spectrum in mgf.read(infile, use_index=False):
                try:
                    data = {
                        "f_id": int(spectrum.get("params").get("feature_id")),
                        "mz": spectrum.get("m/z array"),
                        "intens": spectrum.get("intensity array"),
                        "precursor_mz": spectrum.get("params").get("pepmass")[0],
                    }
                    feature = self.features.get(data["f_id"])
                    feature.Spectrum = Utils.create_spectrum_object(
                        data, self.params.MsmsParameters.rel_int_from
                    )
                    self.features.modify(data["f_id"], feature)
                except KeyError:
                    logger.warning(
                        f"Could not add MS/MS spectrum with the feature ID "
                        f"'{spectrum.get('params').get('feature_id')}'. "
                        "This feature ID does not exist in the provided peaktable"
                        " - SKIP"
                    )

    def parse(self: Self):
        """Parse a mgf style MS/MS file."""
        logger.info(
            f"'MgfParser': started parsing of MS/MS data-containing file "
            f"'{self.params.MsmsParameters.filepath.name}'"
        )
        self.modify_features()
        logger.info(
            f"'MgfParser': completed parsing of MS/MS data-containing file "
            f"'{self.params.MsmsParameters.filepath.name}'"
        )
