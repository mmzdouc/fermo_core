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


class SpectralLibraryParser:
    """Interface to parse different spectral library file formats.

    Attributes:
        spectral_library_filepath: a filepath string
        spectral_library_format: a peaktable format string
        max_library_size: a cutoff limiting the number of spectral entries
    """

    def __init__(
        self: Self,
        filepath: str,
        file_format: str,
        max_library_size: int,
    ):
        self.spectral_library_filepath = filepath
        self.spectral_library_format = file_format
        self.max_library_size = max_library_size

    def parse(self: Self, stats: Stats) -> Stats:
        """Parses a spectral library file based on file format.

        Arguments:
            stats: Stats object - can hold information on spectral library

        Returns:
            (Modified) Stats object.

        Notes:
            Adjust here for additional spectral library file formats.
        """
        match self.spectral_library_format:
            case "mgf":
                return self.parse_mgf(stats)
            case _:
                logging.warning(
                    "Could not recognize spectral library data file format - SKIP."
                )
                return stats

    def parse_mgf(self: Self, stats: Stats) -> Stats:
        """Parses a spectral library file in mgf format, attributes to Stats.

        Arguments:
            stats: Stats object which handles the entries in the spectral library file

        Returns:
            A (modified) Stats object

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling
        """
        logging.debug(
            f"Started parsing spectral library file '{self.spectral_library_filepath}'."
        )

        with open(self.spectral_library_filepath) as infile:
            counter = 1
            stats.spectral_library = dict()
            for spectrum in mgf.read(infile, use_index=False):
                if counter > self.max_library_size:
                    logging.warning(
                        "Spectral library entry exceeds the maximum permitted number "
                        f"of '{self.max_library_size}'. All remaining entries will "
                        "be skipped. To override this number, specify a higher number "
                        "for 'max_library_size' in the parameter settings"
                    )
                    break
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
                        f"Malformed entry (number '{counter}') in file"
                        f"'{self.spectral_library_filepath}'"
                        "detected. Missing 'NAME', 'PEPMASS', or MS/MS information. "
                        "Entry skipped, continue with next entry."
                    )
                counter += 1

        logging.debug(
            f"Completed parsing spectral library file "
            f"'{self.spectral_library_filepath}'."
        )
        return stats
