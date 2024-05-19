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
from typing import Optional, Self

import pandas as pd
from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.parser.group_metadata_parser.class_fermo_metadata_parser import (
    MetadataFermoParser,
)
from fermo_core.data_processing.parser.msms_parser.class_mgf_parser import MgfParser
from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.data_processing.parser.phenotype_parser.class_phenotype_parser import (
    PhenotypeParser,
)
from fermo_core.data_processing.parser.spec_library_parser.class_spec_lib_mgf_parser import (
    SpecLibMgfParser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class GeneralParser(BaseModel):
    """Pydantic-based class to organize calling of specific parser classes + logger

    Attributes:
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
    """

    stats: Optional[Stats] = None
    features: Optional[Repository] = None
    samples: Optional[Repository] = None

    def return_attributes(self: Self) -> tuple[Stats, Repository, Repository]:
        """Returns created attributes to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def parse_parameters(self: Self, params: ParameterManager):
        """Organize calling of specific parser classes.

        Arguments:
            params: ParameterManager holding validated user input
        """
        logger.info("'GeneralParser': started file parsing.")

        self.parse_peaktable(params)
        self.parse_msms(params)
        self.parse_group_metadata(params)
        self.parse_phenotype(params)
        self.parse_spectral_library(params)

        logger.info("'GeneralParser': completed file parsing.")

    def parse_peaktable(self: Self, params: ParameterManager):
        """Parses user-provided peaktable file.

        Arguments:
            params: ParameterManager holding validated user input

        Raises:
            RuntimeError: unsupported peaktable data format
        """
        match params.PeaktableParameters.format:
            case "mzmine3":
                self.stats, self.features, self.samples = PeakMzmine3Parser().parse(
                    params
                )
            case _:
                raise RuntimeError(
                    f"'GeneralParser': detected unsupported format "
                    f"'{params.PeaktableParameters.format}' for 'peaktable'."
                )

    def parse_msms(self: Self, params: ParameterManager):
        """Parses user-provided msms file.

        Arguments:
            params: ParameterManager holding validated user input

        Raises:
            RuntimeError: unsupported msms data format
        """
        if params.MsmsParameters is None:
            logger.info(
                "'GeneralParser': parameters for module 'msms' not specified - SKIP"
            )
            return

        match params.MsmsParameters.format:
            case "mgf":
                mgf_parser = MgfParser(params=params, features=self.features)
                mgf_parser.parse()
                self.features = mgf_parser.return_features()
            case _:
                raise RuntimeError(
                    f"'GeneralParser': detected unsupported format "
                    f"'{params.MsmsParameters.format}' for 'msms'."
                )

    def parse_group_metadata(self: Self, params: ParameterManager):
        """Parses user-provided group metadata file.

        Arguments:
            params: ParameterManager holding validated user input

        Raises:
            RuntimeError: unsupported group metadata format
        """
        if params.GroupMetadataParameters is None:
            logger.info(
                "'GeneralParser': parameters for module 'group_metadata' not specified"
                " - SKIP"
            )
            return

        match params.GroupMetadataParameters.format:
            case "fermo":
                metadata_parser = MetadataFermoParser(
                    stats=self.stats,
                    df=pd.read_csv(params.GroupMetadataParameters.filepath),
                )
                metadata_parser.run_parser()
                self.stats = metadata_parser.return_stats()
            case _:
                raise RuntimeError(
                    f"'GeneralParser': detected unsupported format "
                    f"'{params.GroupMetadataParameters.format}' for 'group_metadata'."
                )

    def parse_phenotype(self: Self, params: ParameterManager):
        """Parses user-provided phenotype/bioactivity data file.

        Arguments:
            params: ParameterManager holding validated user input

        Raises:
            RuntimeError: unsupported group metadata format
        """
        if params.PhenotypeParameters is None:
            logger.info(
                "'GeneralParser': parameters for module 'phenotype' not specified"
                " - SKIP"
            )
            return

        phenotype_parser = PhenotypeParser(
            stats=self.stats,
            df=pd.read_csv(params.PhenotypeParameters.filepath),
        )
        phenotype_parser.message("started")
        phenotype_parser.validate_sample_names()

        match params.PhenotypeParameters.format:
            case "qualitative":
                phenotype_parser.parse_qualitative()
                self.stats = phenotype_parser.return_stats()
            case "quantitative-percentage":
                phenotype_parser.parse_quantitative_percentage(
                    params.PhenoQuantPercentAssgnParams.sample_avg
                )
                self.stats = phenotype_parser.return_stats()
            case "quantitative-concentration":
                phenotype_parser.parse_quantitative_concentration(
                    params.PhenoQuantConcAssgnParams.sample_avg
                )
                self.stats = phenotype_parser.return_stats()
            case _:
                raise RuntimeError(
                    f"'GeneralParser': detected unsupported format "
                    f"'{params.PhenotypeParameters.format}' for 'phenotype'."
                )

        phenotype_parser.message("completed")

    def parse_spectral_library(self: Self, params: ParameterManager):
        """Parses user-provided spectral_library file.

        Arguments:
            params: ParameterManager holding validated user input

        Raises:
            RuntimeError: unsupported spectral library format
        """
        if params.SpecLibParameters is None:
            logger.info(
                "'GeneralParser': parameters for module 'spectral_library' not "
                "specified - SKIP"
            )
            return

        match params.SpecLibParameters.format:
            case "mgf":
                parser = SpecLibMgfParser(params=params, stats=self.stats)
                parser.parse()
                self.stats = parser.return_stats()
            case _:
                raise RuntimeError(
                    f"'GeneralParser': detected unsupported format "
                    f"'{params.SpecLibParameters.format}' for 'spectral_library'."
                )
