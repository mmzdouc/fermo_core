"""Organize general utility functions that are not specific for any other classes.

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
from pathlib import Path
from typing import Union
import urllib.request
import urllib.error

import matchms
from pydantic import BaseModel

logger = logging.getLogger("fermo_core")


class UtilityMethodManager(BaseModel):
    """Pydantic-based base class to organize general utility methods for subclasses."""

    @staticmethod
    def download_file(url: str, file: Union[Path, str]):
        """Downloads from given URL into the designated filename/path.

        Arguments:
            url: A URL string to download from
            file: A string or Path pointing towards the designated file location

        Raises:
            urllib.error.URLError: cannot resolve the URL

        Notes:
            `urlretrieve` considered legacy, therefore not used
        """
        try:
            with urllib.request.urlopen(url) as response, open(file, "wb") as out_file:
                data = response.read()
                out_file.write(data)
        except urllib.error.URLError as e:
            logging.error(
                f"'UtilityMethodManager': could not download from url 'f{url}' - SKIP"
            )
            raise e

    @staticmethod
    def create_spectrum_object(data: dict) -> matchms.Spectrum:
        """Create matchms Spectrum instance, add neutral losses and normalize intensity

        Arguments:
            data: a dict containing data to create a matchms Spectrum object.

        Returns:
            A matchms Spectrum object
        """
        spectrum = matchms.Spectrum(
            mz=data["mz"],
            intensities=data["intens"],
            metadata={"precursor_mz": data["precursor_mz"], "id": data["f_id"]},
            metadata_harmonization=False,
        )
        spectrum = matchms.filtering.add_precursor_mz(spectrum)
        spectrum = matchms.filtering.add_losses(spectrum)
        spectrum = matchms.filtering.normalize_intensities(spectrum)

        return spectrum

        # TODO (MMZ 13.03.24): remove this utility function
