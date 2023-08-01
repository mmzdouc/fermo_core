"""Handle and validate command line input.

Interface to collect user input/parameters via argparse module. Input is validated
using methods from the ParamsHandler class and eventually assigned to an instance of
ParamsHandler class.

Note:
    To transfer parameters/user input from argparse to ParamsHandler, they need to
    be added to the create_input_validation_dict() method.

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
from pathlib import Path
from typing import Self, Any, Callable, Dict
from fermo_core.input_output.class_params_handler import ParamsHandler


class CommLineHandler:
    """Call argparse and validate user input."""

    @staticmethod
    def define_argparse_args(
        params: ParamsHandler,
    ) -> argparse.ArgumentParser:
        """Define command line options.

        Args:
            params: Holds default values of input arguments.

        Returns:
            argparse object containing command line options.

        Notes:
            MMZ 27.8.23
            Once multiple competing input files are supported, the argparse
            arguments can be put into multiple mutually exclusive groups.

            To transfer parameters/user input from argparse to ParamsHandler, they need to
            be added to the create_input_validation_dict() method.
        """
        parser = argparse.ArgumentParser(
            description=(
                "#####################################################\n"
                f"fermo_core v{params.version}: command line interface of "
                f"FERMO\n"
                "#####################################################\n"
                "Focused on large-scale data processing by advanced users.\n"
                "For a more user-friendly experience, see fermo.bioinformatics.nl\n"
                "More info on usage can be found in the README, Docs, or publication.\n"
                "#####################################################\n"
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "--peaktable_mzmine3",
            type=str,
            required=True,
            help=(
                "Provide a peaktable in the MZmine3 'quant_full' .csv-format.\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--msms_mgf",
            type=str,
            required=True,
            help=(
                "Provide a file with molecular feature MS/MS information in the\n"
                ".mgf-format.\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--phenotype_fermo",
            type=str,
            default=None,
            required=False,
            help=(
                "Provide a file with phenotype information in the fermo-format.\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--group_fermo",
            type=str,
            default=None,
            required=False,
            help=(
                "Provide a file with group information in the fermo-format.\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--speclib_mgf",
            type=str,
            default=None,
            required=False,
            help=(
                "Provide a spectral library file in the .mgf-format.\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--mass_dev_ppm",
            type=int,
            choices=range(1, 101),
            metavar="[1-100]",
            default=params.mass_dev_ppm,
            required=False,
            help=(
                "Expected mass deviation tolerance in ppm.\n"
                f"(default: {params.mass_dev_ppm}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--msms_frag_min",
            type=int,
            default=params.msms_frag_min,
            required=False,
            help=(
                "Minimum number of fragments per MS/MS spectrum.\n"
                f"(default: {params.msms_frag_min}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--phenotype_fold",
            type=int,
            default=params.phenotype_fold,
            required=False,
            help=(
                "Factor to retain metabolites present in samples with sub-inhibitory\n"
                "concentrations.\n"
                f"(default: {params.phenotype_fold}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--column_ret_fold",
            type=int,
            default=params.column_ret_fold,
            required=False,
            help=(
                "Factor to retain metabolites that were detected in sample blanks \n"
                "due to cross-contamination.\n"
                f"(default: {params.column_ret_fold}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--fragment_tol",
            type=float,
            default=params.fragment_tol,
            required=False,
            help=(
                "Tolerance when matching two MS/MS fragments in spectral similarity\n"
                "matching, in m/z units.\n"
                f"(default: {params.fragment_tol}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--spectral_sim_score_cutoff",
            type=float,
            default=params.spectral_sim_score_cutoff,
            required=False,
            help=(
                "Similarity score cutoff to determine relatedness of two MS/MS spectra.\n"
                f"(default: {params.spectral_sim_score_cutoff}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--max_nr_links_spec_sim",
            type=int,
            default=params.max_nr_links_spec_sim,
            required=False,
            help=(
                "In spectral similarity/molecular network calculations, maximum number\n"
                "of links to other molecular features any molecular feature is allowed\n"
                "to have.\n"
                f"(default: {params.max_nr_links_spec_sim}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--min_nr_matched_peaks",
            type=int,
            default=params.min_nr_matched_peaks,
            required=False,
            help=(
                "For spectral similarity matching, minimum number of fragments\n"
                "two MS/MS spectra need to share to be considered related.\n"
                f"(default: {params.min_nr_matched_peaks}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--spectral_sim_network_alg",
            type=str,
            default=params.spectral_sim_network_alg,
            required=False,
            choices=["all", "modified_cosine", "ms2deepscore"],
            help=(
                "For spectral similarity matching, spectral similarity/molecular\n"
                "networking algorithm to use.\n"
                f"(default: {params.spectral_sim_network_alg}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--flag_ms2query",
            type=bool,
            choices=[True, False],
            default=params.flag_ms2query,
            required=False,
            help=(
                "Flag to enable/disable annotation by MS2Query.\n"
                "This can increase calculation time.\n"
                f"(default: {params.flag_ms2query}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--flag_ms2query_blank",
            type=bool,
            choices=[True, False],
            default=params.flag_ms2query_blank,
            required=False,
            help=(
                "Flag to enable/disable annotation of sample blank-associated molecular\n"
                "features by MS2Query. This can increase calculation time.\n"
                f"(default: {params.flag_ms2query_blank}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--ms2query_filter_range",
            nargs="+",
            type=float,
            default=params.ms2query_filter_range,
            required=False,
            help=(
                "Restrict annotation by ms2query to a range based on relative\n"
                "intensity (e.g. 0.1 to 1.0, excluding molecular features\n"
                "with a relative intensity of less than 0.1.)\n"
                "Expected input: 'n' 'm' (lower and upper boundary, max. 2 values).\n"
                "Example input: '0.1 1.0'\n"
                f"(default: {params.ms2query_filter_range}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--rel_int_range",
            nargs="+",
            type=float,
            default=params.rel_int_range,
            required=False,
            help=(
                "Restrict processing of molecular features by fermo to a range based\n"
                "on relative intensity (e.g. 0.1 to 1.0, excluding molecular features\n"
                "with a relative intensity of less than 0.1.)\n"
                "Expected input: 'n' 'm' (lower and upper boundary, max. 2 values).\n"
                "Example input: '0.1 1.0'\n"
                f"(default: {params.rel_int_range}).\n"
                "For more information, see the docs.\n"
            ),
        )
        return parser

    @staticmethod
    def raise_value_error(param: str, val: Any, message: str) -> None:
        """Raise value error for given value and message

        Args:
            param: The name of the input value
            val: The invalid input value for which the error is raised
            message: The reason why input value is invalid

        Raises:
            ValueError: Invalid command line input received.
        """
        raise ValueError(f"Parameter {param}: {val} is invalid. Reason: {message}")

    def validate_input_arg(
        self: Self,
        func: Callable,
        user_input: Any,
        param_name: str,
    ) -> bool:
        """Validate input value and return it

        func: Function required to test the input value.
        user_input: The user input
        param_name: Name of the parameter in case an error is raised.

        Returns:
            A bool indicating success or failure
        """
        if (response := func(user_input))[0]:
            return True
        else:
            self.raise_value_error(f"--{param_name}", user_input, response[1])
            return False

    @staticmethod
    def create_input_validation_dict(
        params: ParamsHandler,
        args: argparse.Namespace,
    ) -> Dict:
        """Create dict for command line argument validation.

        Create a dict that delivers arguments to check in validate_input_arg().

        Args:
            params: object instance, provides methods for validation
            args: object instance holding user input/command line args and parameters

        Returns:
            A dict of tuples: For each entry, [0] is always the method to validate with,
            [1] is always the value to test for.

        Notes:
            Additional command line parameter need to be introduced here, else they
            will not be added to the ParamsHandler instance.
        """
        output = dict()

        argument_validation_files = {
            "peaktable_mzmine3": "validate_peaktable_mzmine3",
            "msms_mgf": "validate_mgf",
            "phenotype_fermo": "validate_phenotype_fermo",
            "group_fermo": "validate_group_fermo",
            "speclib_mgf": "validate_mgf",
        }

        for val in argument_validation_files:
            if getattr(args, val) is not None:
                output[val] = (
                    getattr(params, argument_validation_files[val]),
                    Path(
                        getattr(args, val)
                    ),  # Prevent Error when casting None with Path.
                )

        argument_validation_generics = {
            "mass_dev_ppm": "validate_mass_dev_ppm",
            "msms_frag_min": "validate_pos_int",
            "phenotype_fold": "validate_pos_int",
            "column_ret_fold": "validate_pos_int",
            "fragment_tol": "validate_float_zero_one",
            "spectral_sim_score_cutoff": "validate_float_zero_one",
            "max_nr_links_spec_sim": "validate_pos_int",
            "min_nr_matched_peaks": "validate_pos_int",
            "spectral_sim_network_alg": "validate_spectral_sim_network_alg",
            "flag_ms2query": "validate_bool",
            "flag_ms2query_blank": "validate_bool",
        }

        for val in argument_validation_generics:
            if getattr(args, val) is not None:
                output[val] = (
                    getattr(params, argument_validation_generics[val]),
                    getattr(args, val),  # Does not need to be cast.
                )

        argument_validation_ranges = {
            "ms2query_filter_range": "validate_range_zero_one",
            "rel_int_range": "validate_range_zero_one",
        }

        for val in argument_validation_ranges:
            if getattr(args, val) is not None:
                output[val] = (
                    getattr(params, argument_validation_ranges[val]),
                    tuple(getattr(args, val)),  # Prevent Error when List instead Tuple.
                )

        return output

    def run_argparse(self: Self, params: ParamsHandler) -> ParamsHandler:
        """Run argparse comm line interface and assign input to ParamsHandler attributes.

        Args:
            params: ParamsHandler instance to which command line input is assigned.

        Returns:
            Modified ParamsHandler instance.

        Notes:
            To transfer parameters/user input from argparse to ParamsHandler, they need to
            be added to the create_input_validation_dict() method.
        """
        parser = self.define_argparse_args(params)
        args = parser.parse_args()

        arg_validation = self.create_input_validation_dict(params, args)

        for arg in arg_validation:
            if self.validate_input_arg(
                arg_validation[arg][0], arg_validation[arg][1], arg
            ):
                setattr(params, arg, arg_validation[arg][1])

        return params
