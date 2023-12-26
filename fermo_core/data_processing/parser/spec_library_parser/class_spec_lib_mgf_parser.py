"""Parses a spectral library file in mgf format.

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
from fermo_core.data_processing.parser.spec_library_parser.abc_spec_lib_parser import (
    SpecLibParser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager


class SpecLibMgfParser(SpecLibParser):
    """Interface to parse a spectral library file in mgf format."""

    def parse(self: Self, stats: Stats, params: ParameterManager) -> Stats:
        """Parses a spectral library file in mgf format.

        Arguments:
            stats: Stats object which handles the entries in the spectral library file
            params: Parameter Object holding user input information

        Returns:
            A (modified) Stats object

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling
        """
        logging.info(
            f"'SpecLibMgfParser': started parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )

        stats = self.modify_stats(stats, params)

        logging.info(
            f"'SpecLibMgfParser': completed parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )

        return stats

    @staticmethod
    def modify_stats(stats: Stats, params: ParameterManager) -> Stats:
        """Adds spectral library entries to Stats object.

        Arguments:
            stats: Stats object which handles the entries in the spectral library file
            params: Parameter Object holding user input information

        Returns:
            A (modified) Stats object

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling
        """
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
                        "detected. Missing 'NAME' or 'PEPMASS' or MS/MS information. "
                        "SKIP - continue with next entry."
                    )
                counter += 1

        return stats
