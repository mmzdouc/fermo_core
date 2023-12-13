"""Parses spectral library files depending on file format.

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

from fermo_core.data_processing.class_stats import Stats, SpecLibEntry
from fermo_core.input_output.class_parameter_manager import ParameterManager


class SpectralLibraryParser:
    """Interface to parse different spectral library file formats."""

    def parse(self: Self, stats: Stats, params: ParameterManager) -> Stats:
        """Parses a spectral library file based on file format.

        Arguments:
            stats: Stats object handling spectral library information
            params: Parameter Object holding user input information

        Returns:
            (Modified) Stats object.

        Notes:
            Adjust here for additional spectral library file formats.

        # TODO(MMZ 13.12.23): Cover with tests
        """
        match params.SpecLibParameters.format:
            case "mgf":
                return self.parse_mgf(stats, params)
            case _:
                return stats

    @staticmethod
    def parse_mgf(stats: Stats, params: ParameterManager) -> Stats:
        """Parses a spectral library file in mgf format, attributes to Stats.

        Arguments:
            stats: Stats object which handles the entries in the spectral library file
            params: Parameter Object holding user input information

        Returns:
            A (modified) Stats object

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling

        # TODO(MMZ 13.12.23): Cover with tests
        """
        logging.info(
            f"'SpectralLibraryParser': started parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )

        with open(params.SpecLibParameters.filepath) as infile:
            counter = 1
            stats.spectral_library = dict()
            for spectrum in mgf.read(infile, use_index=False):
                try:
                    stats.spectral_library[counter] = SpecLibEntry(
                        spectrum["params"]["name"],
                        spectrum["params"]["pepmass"][0],
                        (
                            tuple(spectrum["m/z array"].tolist()),
                            tuple(spectrum["intensity array"].tolist()),
                        ),
                    )
                except KeyError:
                    logging.warning(
                        f"Malformed entry (count: '{counter}') in file"
                        f"'{params.SpecLibParameters.filepath.name}'"
                        "detected. Missing 'NAME', 'PEPMASS', or MS/MS information. "
                        "Entry skipped, continue with next entry."
                    )
                counter += 1

        logging.info(
            f"'SpectralLibraryParser': completed parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )
        return stats
