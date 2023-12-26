"""Manages methods related to argparse-based command line argument parsing.

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

import argparse
from typing import Self


class ArgparseManager:
    """Manages methods related to argparse command line parsing."""

    def run_argparse(self: Self, version: str, args: list) -> argparse.Namespace:
        """Run argparse comm line interface, main method of this class.

        Arguments:
            version: Indicates the version of fermo.
            args: a list of arguments specified by the user.

        Returns:
            Namespace containing the command line params.
        """
        parser = self.define_argparse_args(version)
        return parser.parse_args(args)

    @staticmethod
    def define_argparse_args(version: str) -> argparse.ArgumentParser:
        """Define command line options for fermo_core.

        Returns:
            argparse object containing command line options.
        """
        parser = argparse.ArgumentParser(
            description=(
                "#####################################################\n"
                f"fermo_core v{version}: command line interface of FERMO.\n"
                "#####################################################\n"
                "Focused on large-scale data processing by advanced users.\n"
                "For a more user-friendly experience, see fermo.bioinformatics.nl.\n"
                "More info on usage can be found in the README, docs, or publication.\n"
                "#####################################################\n"
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "-p",
            "--parameters",
            type=str,
            required=True,
            help=(
                "Provide a FERMO parameter .json file.\n"
                "See 'example_data/case_study_parameters.json' for an example or "
                "consult the documentation.\n"
            ),
        )
        return parser
