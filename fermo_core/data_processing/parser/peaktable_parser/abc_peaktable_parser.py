from abc import ABC, abstractmethod
from typing import Tuple

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


class PeaktableParser(ABC):
    """Abstract base class for all peaktable parsers."""

    @abstractmethod
    def parse(self, params: ParameterManager) -> Tuple[Stats, Repository, Repository]:
        """Interface for class calling and point of entry. Calls class methods.

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
