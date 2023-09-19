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
from typing import Tuple

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.parser.class_peaktable_parser import PeaktableParser
from fermo_core.data_processing.parser.class_msms_parser import MsmsParser
from fermo_core.data_processing.parser.class_group_metadata_parser import (
    GroupMetadataParser,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


class GeneralParser:
    """Interface to organize calling of specific parser classes"""

    @staticmethod
    def parse(params: ParameterManager) -> Tuple[Stats, Repository, Repository]:
        """Organize calling of specific parser classes (e.g. PeaktableParser).

        Arguments:
            params: Stats object holding various information of overall data

        Returns:
            Tuple containing Stats object, Feature and Sample Repository objects.

        Notes:
            Adjust here for additional input file types.
        """
        peaktable_parser = PeaktableParser(
            params.peaktable.get("filename"),
            params.peaktable.get("format"),
            params.rel_int_range,
            (params.ms2query.get("range")[0], params.ms2query.get("range")[1]),
            params.peaktable.get("polarity"),
        )
        stats, features, samples = peaktable_parser.parse()

        if params.msms.get("filename") is not None:
            msms_parser = MsmsParser(
                params.msms.get("filename"), params.msms.get("format")
            )
            features = msms_parser.parse(features)
        else:
            logging.warning(
                "No MS/MS file provided - functionality of FERMO is limited. "
                "For more information, consult the documentation."
            )

        if params.group_metadata.get("filename") is not None:
            group_metadata_parser = GroupMetadataParser(
                params.group_metadata.get("filename"),
                params.group_metadata.get("format"),
            )
            stats, samples = group_metadata_parser.parse(stats, samples)
        else:
            logging.warning(
                "No group metadata provided - functionality of FERMO is limited. "
                "For more information, consult the documentation."
            )

        # TODO(MMZ): Add bioactivity file parser

        # TODO(MMZ): Add library file parser

        return stats, features, samples
