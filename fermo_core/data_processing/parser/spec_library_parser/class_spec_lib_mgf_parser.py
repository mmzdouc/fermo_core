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
from typing import Self

import matchms

from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.parser.spec_library_parser.abc_spec_lib_parser import (
    SpecLibParser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


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
        logger.info(
            f"'SpecLibMgfParser': started parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )

        stats = self.modify_stats(stats, params)

        logger.info(
            f"'SpecLibMgfParser': completed parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'"
        )

        return stats

    @staticmethod
    def modify_stats(stats: Stats, params: ParameterManager) -> Stats:
        """Adds spectral library entries to Stats object.

        Data is read using pyteomics.mgf() and only then converted to
        matchms.Spectrum object to have better control over data import and filtering.

        Arguments:
            stats: Stats object which handles the entries in the spectral library file
            params: Parameter Object holding user input information

        Returns:
            A (modified) Stats object

        Notes:
            mgf.read() returns a Numpy array - turned to list for easier handling
        """
        spectra = list(
            matchms.importing.load_from_mgf(params.SpecLibParameters.filepath)
        )
        spectra = [matchms.filtering.add_precursor_mz(i) for i in spectra]
        spectra = [matchms.filtering.normalize_intensities(i) for i in spectra]
        stats.spectral_library = {num: value for num, value in enumerate(spectra)}
        return stats
