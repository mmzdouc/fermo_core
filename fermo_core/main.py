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

#  Internal
from fermo_core.input_output.class_params_handler import ParamsHandler
from fermo_core.input_output.class_comm_line_handler import CommLineHandler

VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent


def main(params: ParamsHandler) -> None:
    """Run fermo core processing part on input data contained in params.

    Args:
        params (ParamsHandler) : Handling input file names and params

    Returns:
        A data object with methods to export data to a JSON file.

    Notes:
        MMZ 28.08.23
        Should return a session object for use in the dashboard or for file export once
        this part is done.
    """

    #  define abstractbaseclass for input file types (csv
    #  define implementations of mzmine

    print("Arrives at end.")
    print(params)
    pass


if __name__ == "__main__":
    params_handler = ParamsHandler(VERSION, ROOT)
    comm_line_handler = CommLineHandler()
    params_handler = comm_line_handler.run_argparse(params_handler)
    main(params_handler)
