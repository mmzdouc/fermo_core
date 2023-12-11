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
from sys import argv
import logging

#  Internal
from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.data_analysis.class_analysis_manager import AnalysisManager

from fermo_core.input_output.class_argparse_manager import ArgparseManager
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_validation_manager import ValidationManager

VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent

logging.basicConfig(
    # TODO(MMZ): Uncomment before release to allow reading of log from file.
    # filename="fermo_core.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w",
)


def main(params: ParameterManager):
    """Run fermo_core processing part on input data contained in params.

    Args:
        params: Handling input file names and params
    """
    pass
    # stats, features, samples = GeneralParser.parse(params)
    # stats, features, samples = AnalysisManager.analyze(params, stats, features, samples)

    # TODO(MMZ): Create a class that exports the processed data (with switch to
    #  return either a fermo_gui compatible JSON or a table).


if __name__ == "__main__":
    logging.info(f"Started 'fermo_core' version '{VERSION}' as CLI.")

    args = ArgparseManager().run_argparse(VERSION, argv[1:])

    user_input = FileManager.load_json_file(args.parameters)
    ValidationManager().validate_file_vs_jsonschema(user_input, args.parameters)

    param_manager = ParameterManager()
    param_manager.assign_parameters_cli(user_input)

    main(param_manager)
