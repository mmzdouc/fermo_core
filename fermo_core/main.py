#!/usr/bin/env python3

#  External
from importlib import metadata
from pathlib import Path

#  Internal
from fermo_core.input_output.class_params_handler import ParamsHandler

VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent


def main(params: ParamsHandler) -> None:
    """Run fermo core processing part on input data

    Args:
        params (ParamsHandler) : Handling input file names and params

    Notes:
        MMZ 28.08.23
        Should return a session object for use in the dashboard or for file export once
        this part is done.
    """
    print("Arrives to the end of script.")
    print(params.peaktable_mzmine3)
    pass


if __name__ == "__main__":
    params_handler = ParamsHandler(VERSION, ROOT, True)
    params_handler.run_argparse()

    main(params_handler)
