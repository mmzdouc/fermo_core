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
from urllib.parse import urlparse
import urllib.request
import urllib.error

import matchms
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths

logger = logging.getLogger("fermo_core")


class UtilityMethodManager(BaseModel):
    """Pydantic-based base class to organize general utility methods for subclasses."""

    def check_ms2deepscore_req(self: Self, polarity: str):
        """Checks if files required for ms2query functionality are present

        Attributes:
            polarity: the mass spectrometry data polarity

        Raises:
            RuntimeError: unexpected polarity (currently only positive mode supported)
        """
        if polarity == "positive":
            file = urlparse(DefaultPaths().url_ms2deepscore_pos).path.split("/")[-1]
            if not DefaultPaths().dirpath_ms2deepscore_pos.joinpath(file).exists():
                self.download_file(
                    url=DefaultPaths().url_ms2deepscore_pos,
                    location=DefaultPaths().dirpath_ms2deepscore_pos.joinpath(file),
                    timeout=600,
                )
        else:
            logger.warning(
                "'UtilityMethodManager': the MS2DeepScore algorithm currently only "
                "supports positive ionization mode mass spectrometry data - SKIP"
            )
            raise RuntimeError

    def check_ms2query_req(self: Self, polarity: str):
        """Checks if files required for ms2query functionality are present

        Attributes:
            polarity: the mass spectrometry data polarity
        """
        if polarity == "positive":
            for url in DefaultPaths().url_ms2query_pos:
                file = urlparse(url).path.split("/")[-1]
                if not DefaultPaths().dirpath_ms2query_pos.joinpath(file).exists():
                    self.download_file(
                        url=url,
                        location=DefaultPaths().dirpath_ms2query_pos.joinpath(file),
                        timeout=600,
                    )
        else:
            for url in DefaultPaths().url_ms2query_neg:
                file = urlparse(url).path.split("/")[-1]
                if not DefaultPaths().dirpath_ms2query_neg.joinpath(file).exists():
                    self.download_file(
                        url=url,
                        location=DefaultPaths().dirpath_ms2query_neg.joinpath(file),
                        timeout=600,
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
        logger.info(
            f"'UtilityMethodManager': attempt to download file from "
            f"'{url}' to location '{location}' with a timeout of '{timeout}' seconds."
        )
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
    def create_spectrum_object(data: dict, intensity_from: float) -> matchms.Spectrum:
        """Create matchms Spectrum instance, add neutral losses and normalize intensity

        Arguments:
            data: a dict containing data to create a matchms Spectrum object.
            intensity_from: a float between 0 and 1 to filter for intensity

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

        frag_before = len(spectrum.peaks.mz)
        spectrum = matchms.filtering.remove_peaks_around_precursor_mz(
            spectrum_in=spectrum, mz_tolerance=10
        )
        logger.debug(
            f"'UtilityMethodManager': feature id '{data['f_id']}': removed MS2 "
            f"fragments 10 Da around precursor m/z. '{len(spectrum.peaks.mz)}' "
            f"fragments remaining (before: '{frag_before}')."
        )

        spectrum = matchms.filtering.normalize_intensities(spectrum)
        if intensity_from > 0.0:
            frag_before = len(spectrum.peaks.mz)
            spectrum = matchms.filtering.select_by_relative_intensity(
                spectrum, intensity_from=intensity_from
            )
            frag_diff = frag_before - len(spectrum.peaks.mz)
            logger.debug(
                f"'UtilityMethodManager': feature id '{data['f_id']}': removed '"
                f"{frag_diff}' MS2 fragments with relative intensity lower than '"
                f"{intensity_from}'. '{len(spectrum.peaks.mz)}' fragments remaining ("
                f"before: '{frag_before}')."
            )

        spectrum = matchms.filtering.add_losses(spectrum)

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
            return abs(((m1 - m2) / m2) * 10**6)
        except ZeroDivisionError as e:
            logger.error(
                f"'AnnotationManager/AdductAnnotator': Division through zero. "
                f"Feature with id '{f_id_m2}' has a mass of '{m2}'. This is illegal - "
                f"SKIP"
            )
            raise e
