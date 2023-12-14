from abc import ABC, abstractmethod
from typing import Self

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

    @staticmethod
    @abstractmethod
    def modify_features(
        feature_repo: Repository, params: ParameterManager
    ) -> Repository:
        """Method to modify Feature objects by adding MS/MS info. Called by 'parse'.

        Arguments:
            feature_repo: An instance of Repository class w Feature objects
            params: An instance of the ParameterManager class

        Returns:
            Repository object w modified Feature objects
        """
        pass
