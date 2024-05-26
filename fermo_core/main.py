"""Main entry point to fermo_core.

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

import json
import logging
import platform
import sys
from argparse import Namespace
from datetime import datetime
from importlib import metadata
from pathlib import Path

import coloredlogs

from fermo_core.data_analysis.class_analysis_manager import AnalysisManager
from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_argparse_manager import ArgparseManager
from fermo_core.input_output.class_export_manager import ExportManager
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_validation_manager import ValidationManager


def main(params: ParameterManager, starttime: datetime, logger: logging.Logger):
    """Run fermo_core processing part on input data contained in params.

    Can be used as a module too.

    Args:
        params: Handling input file names and params
        starttime: start time
        logger: the 'fermo_core' logger
    """
    general_parser = GeneralParser()
    general_parser.parse_parameters(params)
    stats, features, samples = general_parser.return_attributes()

    analysis_manager = AnalysisManager(
        params=params, stats=stats, features=features, samples=samples
    )
    analysis_manager.analyze()
    stats, features, samples = analysis_manager.return_attributes()

    export_manager = ExportManager(
        params=params, stats=stats, features=features, samples=samples
    )
    export_manager.run(metadata.version("fermo_core"), starttime)

    logger.info("'main': completed all steps - DONE")


def configure_logger_results(args: Namespace) -> logging.Logger:
    """Set up logging parameters and create output dir to store log

    Arguments:
        args: the argparse object containing user params

    Raises:
        ValueError: verboseness parameter is not one of the allowed values
        KeyError: parameters file incorrectly formatted.
    """
    with open(Path(args.parameters)) as infile:
        json_dict = json.load(infile)
        file_dir = json_dict.get("files", {}).get("peaktable", {}).get("filepath")

    if file_dir is None:
        raise KeyError("'fermo_core': could not find 'peaktable' in parameters file.")
    else:
        Path(file_dir).parent.joinpath("results").mkdir(exist_ok=True)

    if args.verboseness not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError("'fermo_core': parameter 'verboseness' incorrect.")

    logger = logging.getLogger("fermo_core")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, args.verboseness))
    console_handler.setFormatter(
        coloredlogs.ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )

    file_handler = logging.FileHandler(
        Path(file_dir).parent.joinpath("results").joinpath("out.fermo.log"),
        mode="w",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def main_cli():
    """Interface for installer."""
    start_time = datetime.now()
    args = ArgparseManager().run_argparse(metadata.version("fermo_core"), sys.argv[1:])

    logger = configure_logger_results(args=args)
    logger.info(f"Started 'fermo_core' v'{metadata.version('fermo_core')}' as CLI.")
    logger.debug(
        f"Python version: {platform.python_version()}; "
        f"System: {platform.system()}; "
        f"System version: {platform.version()};"
        f"System architecture: {platform.python_version()}"
    )

    user_input = FileManager.load_json_file(args.parameters)
    ValidationManager().validate_file_vs_jsonschema(user_input, args.parameters)

    param_manager = ParameterManager()
    param_manager.assign_parameters_cli(user_input)
    main(params=param_manager, starttime=start_time, logger=logger)


if __name__ == "__main__":
    main_cli()
