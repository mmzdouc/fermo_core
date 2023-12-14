"""Organizes calling of specific parsers.

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
from typing import Tuple, Self, Optional

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)

from fermo_core.data_processing.parser.msms_parser.class_mgf_parser import MgfParser
from fermo_core.data_processing.parser.group_metadata_parser.class_fermo_metadata_parser import (
    MetadataFermoParser,
)
from fermo_core.data_processing.parser.class_spectral_library_parser import (
    SpectralLibraryParser,
)
from fermo_core.data_processing.parser.phenotype_parser.class_fermo_phenotype_parser import (
    PhenotypeFermoParser,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


class GeneralParser:
    """Interface to organize calling of specific parser classes and their logging

    Attributes:
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
    """

    def __init__(self):
        self.stats: Optional[Stats] = None
        self.features: Optional[Repository] = None
        self.samples: Optional[Repository] = None

    def return_attributes(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Returns created attributes to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def parse_parameters(self: Self, params: ParameterManager):
        """Organize calling of specific parser classes.

        Arguments:
            params: ParameterManager holding validated user input

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        logging.info("'GeneralParser': started file parsing.")

        self.parse_peaktable(params)
        self.parse_msms(params)
        self.parse_group_metadata(params)
        self.parse_phenotype(params)
        self.parse_spectral_library(params)

        logging.info("'GeneralParser': completed file parsing.")

    def parse_peaktable(self: Self, params: ParameterManager):
        """Parses user-provided peaktable file.

        Arguments:
            params: ParameterManager holding validated user input

        # TODO(MMZ 11.12.23): Cover with tests
        """
        match params.PeaktableParameters.format:
            case "mzmine3":
                self.stats, self.features, self.samples = PeakMzmine3Parser().parse(
                    params
                )

    def parse_msms(self: Self, params: ParameterManager):
        """Parses user-provided msms file.

        Arguments:
            params: ParameterManager holding validated user input

        # TODO(MMZ 11.12.23): Cover with tests
        """
        if params.MsmsParameters is None:
            logging.info(
                "'GeneralParser': parameters for module 'msms' not specified - SKIP"
            )
            return

        match params.MsmsParameters.format:
            case "mgf":
                self.features = MgfParser().parse(self.features, params)

    def parse_group_metadata(self: Self, params: ParameterManager):
        """Parses user-provided group metadata file.

        Arguments:
            params: ParameterManager holding validated user input

        # TODO(MMZ 11.12.23): Cover with tests
        """
        if params.GroupMetadataParameters is None:
            logging.info(
                "'GeneralParser': parameters for module 'group_metadata' not specified"
                " - SKIP"
            )
            return

        match params.GroupMetadataParameters.format:
            case "fermo":
                self.stats, self.samples = MetadataFermoParser().parse(
                    self.stats, self.samples, params
                )

    def parse_phenotype(self: Self, params: ParameterManager):
        """Parses user-provided phenotype/bioactivity data file.

        Arguments:
            params: ParameterManager holding validated user input

        # TODO(MMZ 11.12.23): Cover with tests
        """
        if params.PhenotypeParameters is None:
            logging.info(
                "'GeneralParser': parameters for module 'phenotype' not specified"
                " - SKIP"
            )
            return

        match params.PhenotypeParameters.format:
            case "fermo":
                self.stats, self.samples = PhenotypeFermoParser().parse(
                    self.stats, self.samples, params
                )

    def parse_spectral_library(self: Self, params: ParameterManager):
        """Parses user-provided spectral_library file.

        Arguments:
            params: ParameterManager holding validated user input

        # TODO(MMZ 11.12.23): Cover with tests
        """
        if params.SpecLibParameters is None:
            logging.info(
                "'GeneralParser': parameters for module 'spectral_library' not "
                "specified - SKIP"
            )
            return

        logging.info(
            "'GeneralParser': started parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'."
        )

        self.stats = SpectralLibraryParser().parse(self.stats, params)

        logging.info(
            "'GeneralParser': started parsing of spectral library file "
            f"'{params.SpecLibParameters.filepath.name}'."
        )
