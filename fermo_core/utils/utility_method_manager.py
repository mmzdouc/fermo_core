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
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Self
from urllib.parse import urlparse

import matchms
import pandas as pd
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
            RuntimeError(
                "'UtilityMethodManager': the MS2DeepScore algorithm currently only "
                "supports positive ionization mode mass spectrometry data - SKIP"
            )

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
            URLError: states the URL from where download failed

        Notes:
            `urlretrieve` considered legacy, therefore not used
        """
        logger.info(
            f"'UtilityMethodManager': attempt to download file from "
            f"'{url}' to location '{location}' with a timeout of '{timeout}' seconds."
        )
        try:
            with (
                urllib.request.urlopen(url=url, timeout=timeout) as response,
                open(location, "wb") as out,
            ):
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
        """Create matchms Spectrum, add neutral losses, normalize and filter intensity

        Arguments:
            data: a dict containing data to create a matchms Spectrum object.
            intensity_from: a float between 0 and 1 to filter for MS2 rel intensity

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
                f"MS2 fragments with relative intensity lower than '"
                f"{intensity_from}': {frag_diff}'. '{len(spectrum.peaks.mz)}' "
                f"fragments remaining (before: '{frag_before}')."
            )

        spectrum = matchms.filtering.add_losses(spectrum)

        return spectrum

    @staticmethod
    def mass_deviation(m1: float, m2: float, f_id_m2: int | str) -> float:
        """Calculate mass deviation in ppm between m1 and m2

        Arguments:
            m1: an m/z ratio
            m2: an m/z ratio
            f_id_m2: the (feature) id of m2 for error reporting

        Returns:
            The mass deviation in ppm

        Raises:
            ZeroDivisionError: m2 is zero

        Notes:
            Taken from publication doi.org/10.1016/j.jasms.2010.06.006
        """
        try:
            return abs(((m1 - m2) / m2) * 10**6)
        except ZeroDivisionError as e:
            logger.error(
                f"'UtilityMethodManager': Division through zero in mass deviation "
                f"calculation. Feature with id '{f_id_m2}' has a mass of '{m2}' - SKIP"
            )
            raise e

    @staticmethod
    def extract_as_kcb_results(as_results: Path, cutoff: float) -> dict:
        """Extract MIBiG IDs from antiSMASH full results folder

        Arguments:
            as_results: a path pointing towards the antiSMASH results folder
            cutoff: the coverage cutoff value to restrict spurious hits

        Returns:
            A dict of regions with detected MIBiG knownclusterblast matches

        Raises:
            NotADirectoryError: the knownclusterblast directory was not found
        """

        def _extract_bgcs(content) -> list:
            return re.findall(r"BGC\d{7}", content)

        df_cds = pd.read_csv(
            DefaultPaths().library_mibig_pos.parent.parent.joinpath(
                "mibig_cds_count.csv"
            )
        )

        if not as_results.joinpath("knownclusterblast").is_dir():
            raise NotADirectoryError(
                f"'UtilityMethodManager': could not find the directory "
                f"'knownclusterblast' in the antiSMASH result folder "
                f"'{as_results.resolve()}' - SKIP"
            )

        bgcs = {}
        for f_path in as_results.joinpath("knownclusterblast").iterdir():
            if f_path.is_file() and f_path.suffix == ".txt":
                with open(f_path) as f_handle:
                    data = f_handle.read()

                    if len(_extract_bgcs(data)) == 0:
                        logger.debug(
                            f"'UtilityMethodManager': no significant "
                            f"KnownClusterBlast matches for region '{f_path.stem}' - "
                            f"SKIP"
                        )
                        continue

                    entries = data.split(">>")[1:]
                    for entry in entries:
                        bgc_id = _extract_bgcs(entry)[0]
                        hits = entry.split(
                            "Table of Blast hits (query gene, subject gene, %identity,"
                            " blast score, %coverage, e-value):"
                        )[1:][0].split("\n")
                        nr_hits = len([item for item in hits if item != ""])
                        cds_bgc = df_cds.loc[
                            df_cds["mibig_id"] == bgc_id, "nr_cds"
                        ].values[0]
                        if (bgc_sim := round((nr_hits / cds_bgc), 2)) >= cutoff:
                            if bgc_sim > 1.0:
                                bgc_sim = 1.0
                            try:
                                if bgcs[bgc_id]["bgc_sim"] < bgc_sim:
                                    bgcs[bgc_id] = {
                                        "bgc_nr_cds": cds_bgc,
                                        "matched_cds": nr_hits,
                                        "bgc_sim": bgc_sim * 100,
                                        "region": f_path.stem,
                                    }
                            except KeyError:
                                bgcs[bgc_id] = {
                                    "bgc_nr_cds": cds_bgc,
                                    "matched_cds": nr_hits,
                                    "bgc_sim": bgc_sim * 100,
                                    "region": f_path.stem,
                                }

        if len(bgcs) != 0:
            return bgcs
        else:
            raise RuntimeError(
                "'UtilityMethodManager': could not find significant BGC matches in "
                "antiSMASH KnownClusterBlast results."
            )

    @staticmethod
    def create_mibig_spec_lib(mibig_ids: set) -> list[matchms.Spectrum]:
        """Load MIBiG-derived in silico spectral library.

        Attributes:
            mibig_ids: A set of MIBiG IDs to create a targeted spectral library

        Returns:
            The spectral library

        Raises:
            RuntimeError: empty spectral library
        """
        spectra = list(
            matchms.importing.load_from_mgf(DefaultPaths().library_mibig_pos)
        )
        spectra = [matchms.filtering.add_precursor_mz(i) for i in spectra]
        spectra = [matchms.filtering.normalize_intensities(i) for i in spectra]

        filtered_spectra = []
        for spectrum in spectra:
            ids = set(spectrum.metadata.get("mibigaccession").split(","))
            if not mibig_ids.isdisjoint(ids):
                filtered_spectra.append(spectrum)

        if len(filtered_spectra) != 0:
            return filtered_spectra
        else:
            raise RuntimeError(
                "'UtilityMethodManager': MIBiG spectral library construction: "
                "spectral library empty - SKIP."
            )
