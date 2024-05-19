"""Parses a spectral library file in mgf format.

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

import matchms
from pydantic import BaseModel

from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class SpecLibMgfParser(BaseModel):
    """Interface to parse a spectral library file in mgf format.

    Attributes:
        params: a ParameterManager instance managing the input parameters
        stats: a Stats object instance to store spectral library in
    """

    params: ParameterManager
    stats: Stats

    def return_stats(self: Self) -> Stats:
        """Returns modified stats objects

        Returns:
            The modified stats objects
        """
        return self.stats

    def modify_stats(self: Self):
        """Adds spectral library entries to Stats object."""
        spectra = list(
            matchms.importing.load_from_mgf(self.params.SpecLibParameters.filepath)
        )
        spectra = [matchms.filtering.add_precursor_mz(i) for i in spectra]
        spectra = [matchms.filtering.normalize_intensities(i) for i in spectra]
        self.stats.spectral_library = spectra

    def parse(self: Self):
        """Parses a spectral library file in mgf format.

        Returns:
            A (modified) Stats object
        """
        logger.info(
            f"'SpecLibMgfParser': started parsing of spectral library file "
            f"'{self.params.SpecLibParameters.filepath.name}'"
        )
        self.modify_stats()

        logger.info(
            f"'SpecLibMgfParser': completed parsing of spectral library file "
            f"'{self.params.SpecLibParameters.filepath.name}'"
        )
