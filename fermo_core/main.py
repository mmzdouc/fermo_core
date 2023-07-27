#!/usr/bin/env python3

#  External
from importlib import metadata
from pathlib import Path

#  Internal
from fermo_core.class_params_handler import ParamsHandler

VERSION = metadata.version("fermo_core")
ROOT = Path(__file__).resolve().parent


def main():
    """Main entry point into script"""
    pass


if __name__ == "__main__":
    params_handler = ParamsHandler(VERSION, ROOT)
    params_handler.run_argparse()

    main()
