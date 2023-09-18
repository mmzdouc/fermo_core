#!/usr/bin/env python3

"""Main entry point to fermo_core.

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

#  External
from importlib import metadata
from pathlib import Path
import logging

#  Internal
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.parser.class_peaktable_parser import PeaktableParser
from fermo_core.data_processing.parser.class_msms_parser import MsmsParser
from fermo_core.data_processing.parser.class_group_metadata_parser import (
    GroupMetadataParser,
)


VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent

logging.basicConfig(
    # TODO(MMZ): Uncomment before release to allow reading of log from file.
    # filename="fermo_core.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w",
)


def main(params: ParameterManager) -> None:
    """Run fermo_core processing part on input data contained in params.

    Args:
        params: Handling input file names and params

    Returns:
        A data object with methods to export data to a JSON file.

    Notes:
        TODO(MMZ): 28.08.23
        Should return a session object for use in the dashboard or for file export
    """
    peaktable_parser = PeaktableParser(
        params.peaktable.get("filename"),
        params.peaktable.get("format"),
        params.rel_int_range,
        (params.ms2query.get("range")[0], params.ms2query.get("range")[1]),
    )
    stats, features, samples = peaktable_parser.parse()

    msms_parser = MsmsParser(params.msms.get("filename"), params.msms.get("format"))
    features = msms_parser.parse(features)

    group_metadata_parser = GroupMetadataParser(
        params.group_metadata.get("filename"),
        params.group_metadata.get("format"),
    )
    stats, samples = group_metadata_parser.parse(stats, samples)

    # TODO(MMZ): revise code to make msms optional -> do not raise the error in the
    #  assign function?

    # TODO(MMZ): add polarity (positive/negative) + add protocol for adding/changing
    #  parameters

    # TODO(MMZ): cover new classes with tests
    #

    # features = Parser().parse_msms(params, features)
    # stats, samples = Parser().parse_group_metadata(params, stats, samples)

    # TODO(MMZ): Add phenotype/bioactivity parser file

    # TODO(MMZ): proceed with annotations, bioactivity etc.

    # TODO(MMZ): when calculating fold changes, also add group info to features


if __name__ == "__main__":
    logging.info(f"Started 'fermo_core' version '{VERSION}' in command line mode.")
    params_manager = ParameterManager(VERSION, ROOT)
    args = params_manager.run_argparse()
    default_params = params_manager.load_json_file(
        str(ROOT.joinpath("config", "default_parameters.json"))
    )
    user_params = params_manager.load_json_file(args.parameters)
    params_manager.parse_parameters(user_params, default_params)
    main(params_manager)
