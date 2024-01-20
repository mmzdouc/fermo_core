"""Abstract base class for MS/MS file parser.

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

from abc import ABC, abstractmethod
from typing import Self

import matchms

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import ParameterManager


class MsmsParser(ABC):
    """Abstract base class for all MS/MS parsers."""

    @abstractmethod
    def parse(
        self: Self, feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Interface for class calling and point of entry. Calls static methods.

        Arguments:
            feature_repo: An instance of Repository class w Feature objects
            params: An instance of the ParameterManager class

        Returns:
            Repository object w modified Feature objects
        """
        pass

    @abstractmethod
    def modify_features(
        self: Self, feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Method to modify Feature objects by adding MS/MS info. Called by 'parse'.

        Arguments:
            feature_repo: An instance of Repository class w Feature objects
            params: An instance of the ParameterManager class

        Returns:
            Repository object w modified Feature objects
        """
        pass

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

        return spectrum
