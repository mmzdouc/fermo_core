"""Abstract base class for MS1 peaktable file parser.

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

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


class PeaktableParser(ABC):
    """Abstract base class for all peaktable parsers."""

    @abstractmethod
    def parse(
        self: Self, params: ParameterManager
    ) -> tuple[Stats, Repository, Repository]:
        """Interface for class calling and point of entry. Calls static methods.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            Tuple of objects: Stats, Repository w Features, Repository w Samples
        """
        pass

    @staticmethod
    @abstractmethod
    def extract_stats(params: ParameterManager) -> Stats:
        """Method to create a Stats object from peaktable. Called by 'parse' method.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            A Stats object summarizing general information about peaktable.
        """
        pass

    @staticmethod
    @abstractmethod
    def extract_features(params: ParameterManager) -> Repository:
        """Method to create a Repository of Features. Called by 'parse' method.

        Arguments:
            params: An instance of the ParameterManager class

        Returns:
            A Repository object containing Feature objects
        """
        pass

    @staticmethod
    @abstractmethod
    def extract_samples(stats: Stats, params: ParameterManager) -> Repository:
        """Method to create a Repository of Samples. Called by 'parse' method.

        Arguments:
            stats: An instance of the Stats class
            params: An instance of the ParameterManager class

        Returns:
            A Repository object containing Sample objects
        """
        pass
