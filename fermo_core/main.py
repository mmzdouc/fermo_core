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
from fermo_core.input_output.dataclass_params_handler import ParamsHandler
from fermo_core.input_output.class_comm_line_handler import CommLineHandler
from fermo_core.data_processing.class_parser import Parser


VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent

logging.basicConfig(
    # TODO(MMZ): Uncomment before release to allow reading of log from file.
    # filename="fermo_core.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w",
)


def main(params: ParamsHandler) -> None:
    """Run fermo core processing part on input data contained in params.

    Args:
        params: Handling input file names and params

    Returns:
        A data object with methods to export data to a JSON file.

    Notes:
        MMZ 28.08.23
        Should return a session object for use in the dashboard or for file export once
        this part is done.
    """
    logging.info("Start of peaktable parsing.")
    stats, features, samples = Parser().parse_peaktable(params)

    features = Parser().parse_msms(params, features)

    # TODO(MMZ): parse the msms info in separate Parser class

    # TODO(MMZ): Cover parser class with tests

    # TODO(MMZ): proceed with annotations, bioactivity etc.


if __name__ == "__main__":
    comm_line_handler = CommLineHandler()
    params_handler = comm_line_handler.run_argparse(ParamsHandler(VERSION, ROOT))
    logging.info("Completed command line parameter parsing.")
    main(params_handler)
