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
from typing import Self
import urllib.request
import urllib.error

import matchms
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths

logger = logging.getLogger("fermo_core")


class UtilityMethodManager(BaseModel):
    """Pydantic-based base class to organize general utility methods for subclasses."""

    @staticmethod
    def check_ms2deepscore_req() -> bool:
        """Checks and logs if file required for MS2DeepScore functionality are present

        Returns:
            True - file present; False - file not present
        """
        if (
            not DefaultPaths()
            .dirpath_ms2deepscore.joinpath(DefaultPaths().filename_ms2deepscore)
            .exists()
        ):
            logger.warning(
                f"'MS2DeepScore embedding file "
                f"'{DefaultPaths().filename_ms2deepscore}' not found. "
                f"Attempting to download file to default directory"
                f"{DefaultPaths().dirpath_ms2deepscore.resolve()}'. This may take "
                f"some time."
            )
            return False
        else:
            return True

    def download_ms2deepscore_req(self: Self, max_runtime: int):
        """Download ms2deepscore required files as specified in DefaultSettings class

        Arguments:
            max_runtime: maximum time to download in seconds

        """
        if max_runtime != 0:
            self.download_file(
                url=DefaultPaths().url_ms2deepscore,
                location=DefaultPaths().dirpath_ms2deepscore.joinpath(
                    DefaultPaths().filename_ms2deepscore
                ),
                timeout=max_runtime,
            )
        else:
            self.download_file(
                url=DefaultPaths().url_ms2deepscore,
                location=DefaultPaths().dirpath_ms2deepscore.joinpath(
                    DefaultPaths().filename_ms2deepscore
                ),
                timeout=3600,
            )

    @staticmethod
    def download_file(url: str, location: Path, timeout: int):
        """Downloads from given URL into the designated location.

        Arguments:
            url: A URL string to download from
            location: A Path pointing towards the designated file location
            timeout: A timeout for the download

        Raises:
            URLError

        Notes:
            `urlretrieve` considered legacy, therefore not used
        """
        try:
            with urllib.request.urlopen(url=url, timeout=timeout) as response, open(
                location, "wb"
            ) as out:
                data = response.read()
                out.write(data)
            logger.info(
                f"'UtilityMethodManager': successfully downloaded file from "
                f"'{url}' to location '{location}'."
            )
        except urllib.error.URLError as e:
            logger.error(
                f"'UtilityMethodManager': could not download from url '{url}' - SKIP"
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

    @staticmethod
    def mass_deviation(m1: float, m2: float, f_id_m2: int | str) -> float:
        """Calculate mass deviation in ppm between m1 and m2

        Arguments:
            m1: an m/z ratio
            m2: an m/z ratio
            f_id_m2: the (feature) id of m2

        Returns:
            The mass deviation in ppm

        Raises:
            ZeroDivisionError

        Notes:
            Taken from publication doi.org/10.1016/j.jasms.2010.06.006
        """
        try:
            return round(abs(((m1 - m2) / m2) * (10**6)), 2)
        except ZeroDivisionError as e:
            logger.error(
                f"'AnnotationManager/AdductAnnotator': Division through zero. "
                f"Feature with id '{f_id_m2}' has a mass of '{m2}'. This is illegal - "
                f"SKIP"
            )
            raise e
