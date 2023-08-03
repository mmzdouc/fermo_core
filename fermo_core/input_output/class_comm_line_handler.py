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
from typing import Self, Any, Tuple, List
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

        # group_peaktable = parser.add_mutually_exclusive_group(required=True)

        parser.add_argument(
            "--peaktable_mzmine3",
            type=str,
            help=(
                "Provide a peaktable in the MZmine3 'quant_full' .csv-format.\n"
                "For more information, see the docs.\n"
            ),
        )
        # group_peaktable.add_argument(
        #     "--peaktable_fermo",
        #     type=str,
        #     help=(
        #         "Provide a peaktable in the FERMO .csv-format.\n"
        #         "For more information, see the docs.\n"
        #     ),
        # )

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
                "In this case, the parameter '--phenotype_fermo_mode must also be \n"
                "given.'\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--phenotype_fermo_mode",
            type=str,
            default=params.phenotype_fermo_mode,
            required=False,
            choices=["percentage", "concentration"],
            help=(
                "Specifies the data mode of the phenotype information.\n"
                "All data must be of the same type of experiment (e.g. MIC).\n"
                f"(default: {params.spectral_sim_network_alg}).\n"
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

    def assign_peaktable_mzmine3(
        self: Self, name: str, peaktable: str, ref: ParamsHandler
    ) -> Path | None:
        """Validate peaktable and prepare for assignment.

        Args:
            name: A command line parameter name
            peaktable: A string pointing toward a mzmine3 style peaktable
            ref: Instance of ParamsHandler

        Returns:
            A Path instance or None.
        """
        if peaktable is not None:
            if not (response := ref.validate_path(peaktable))[0]:
                self.raise_value_error(f"--{name}", peaktable, response[1])
            elif not (response := ref.validate_peaktable_mzmine3(Path(peaktable)))[0]:
                self.raise_value_error(f"--{name}", peaktable, response[1])
            else:
                return Path(peaktable)
        else:
            return None

    def assign_mgf(self: Self, name: str, mgf: str, ref: ParamsHandler) -> Path | None:
        """Validate mgf file and prepare for assignment.

        Args:
            name: A command line parameter name
            mgf: A string pointing toward an MS/MS mgf file
            ref: Instance of ParamsHandler

        Returns:
            A Path instance or None.
        """
        if mgf is not None:
            if not (response := ref.validate_path(mgf))[0]:
                self.raise_value_error(f"--{name}", mgf, response[1])
            elif not (response := ref.validate_mgf(Path(mgf)))[0]:
                self.raise_value_error(f"--{name}", mgf, response[1])
            else:
                return Path(mgf)
        else:
            return None

    def assign_phenotype_fermo(
        self: Self, name: str, table: str, mode: str, ref: ParamsHandler
    ) -> Path | None:
        """Validate phenotype_fermo file and prepare for assignment.

        Args:
            name: A command line parameter name.
            table: A string pointing toward a phenotype fermo type file.
            mode: A string describing the formatting mode
            ref: Instance of ParamsHandler

        Returns:
            A Path instance or None.
        """
        if table is not None:
            if not (response := ref.validate_path(table))[0]:
                self.raise_value_error(f"--{name}", table, response[1])
            elif not (response := ref.validate_phenotype_fermo(Path(table), mode))[0]:
                self.raise_value_error(f"--{name}", table, response[1])
            else:
                return Path(table)
        else:
            return None

    def assign_group_fermo(
        self: Self, name: str, table: str, ref: ParamsHandler
    ) -> Path | None:
        """Validate group_fermo file and prepare for assignment.

        Args:
            name: A command line parameter name.
            table: A string pointing toward a fermo-style group file.
            ref: Instance of ParamsHandler

        Returns:
            A Path instance or None.
        """
        if table is not None:
            if not (response := ref.validate_path(table))[0]:
                self.raise_value_error(f"--{name}", table, response[1])
            elif not (response := ref.validate_group_fermo(Path(table)))[0]:
                self.raise_value_error(f"--{name}", table, response[1])
            else:
                return Path(table)
        else:
            return None

    def assign_mass_dev_ppm(self: Self, name: str, ppm: int, ref: ParamsHandler) -> int:
        """Validate mass_dev_ppm and prepare for assignment.

        Args:
            name: The command line parameter name.
            ppm: The expected mass deviation in ppm.
            ref: Instance of ParamsHandler

        Returns:
            An integer.
        """
        if not (response := ref.validate_mass_dev_ppm(ppm))[0]:
            self.raise_value_error(f"--{name}", ppm, response[1])
        else:
            return ppm

    def assign_pos_int(self: Self, name: str, in_val: int, ref: ParamsHandler) -> int:
        """Validate a positive integer and prepare for assignment.

        Args:
            name: The command line parameter name.
            in_val: The integer value
            ref: Instance of ParamsHandler

        Returns:
            An integer.
        """
        if not (response := ref.validate_pos_int(in_val))[0]:
            self.raise_value_error(f"--{name}", in_val, response[1])
        else:
            return in_val

    def assign_float_zero_one(
        self: Self, name: str, fl_val: float, ref: ParamsHandler
    ) -> float:
        """Validate a positive float between 0 and 1 and prepare for assignment.

        Args:
            name: The command line parameter name.
            fl_val: The float value
            ref: Instance of ParamsHandler

        Returns:
            An integer.
        """
        if not (response := ref.validate_float_zero_one(fl_val))[0]:
            self.raise_value_error(f"--{name}", fl_val, response[1])
        else:
            return fl_val

    def assign_bool(self: Self, name: str, b: bool, ref: ParamsHandler) -> bool:
        """Validate a bool value and prepare for assignment.

        Args:
            name: The command line parameter name.
            b: The bool value
            ref: Instance of ParamsHandler

        Returns:
            A bool indicating a flag.
        """
        if not (response := ref.validate_bool(b))[0]:
            self.raise_value_error(f"--{name}", b, response[1])
        else:
            return b

    def assign_range_zero_one(
        self: Self, name: str, r: List[float], ref: ParamsHandler
    ) -> Tuple[float]:
        """Validate a range, cast into tuple, and prepare for assignment.

        Args:
            name: The command line parameter name.
            r: The range, a list of two values (or more, depending on user input).
            ref: Instance of ParamsHandler.

        Returns:
            A tuple indicating a range between 0 and 1.
        """
        if not (response := ref.validate_range_zero_one(tuple(r)))[0]:
            self.raise_value_error(f"--{name}", r, response[1])
        else:
            return tuple(r)

    def assign_network_alg(self: Self, name: str, alg: str, ref: ParamsHandler) -> str:
        """Validate the validity of the chosen network algorithm, prepare for assignment.

        Args:
            name: The command line parameter name.
            alg: The chosen network algorithm.
            ref: Instance of ParamsHandler.

        Returns:
            A str indicating the network algorithm.
        """
        if not (response := ref.validate_spectral_sim_network_alg(alg))[0]:
            self.raise_value_error(f"--{name}", alg, response[1])
        else:
            return alg

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

        for arg in vars(args):
            if arg == "peaktable_mzmine3":
                setattr(
                    params,
                    arg,
                    self.assign_peaktable_mzmine3(arg, getattr(args, arg), params),
                )
            elif arg == "msms_mgf":
                setattr(params, arg, self.assign_mgf(arg, getattr(args, arg), params))
            elif arg == "phenotype_fermo":
                setattr(
                    params,
                    arg,
                    self.assign_phenotype_fermo(
                        arg,
                        getattr(args, arg),
                        getattr(args, "phenotype_fermo_mode"),
                        params,
                    ),
                ),
                setattr(
                    params,
                    "phenotype_fermo_mode",
                    getattr(args, "phenotype_fermo_mode"),
                )
            elif arg == "group_fermo":
                setattr(
                    params,
                    arg,
                    self.assign_group_fermo(arg, getattr(args, arg), params),
                )
            elif arg == "speclib_mgf":
                setattr(params, arg, self.assign_mgf(arg, getattr(args, arg), params))
            elif arg == "mass_dev_ppm":
                setattr(
                    params,
                    arg,
                    self.assign_mass_dev_ppm(arg, getattr(args, arg), params),
                )
            elif any(
                arg == i
                for i in [
                    "phenotype_fold",
                    "column_ret_fold",
                    "max_nr_links_spec_sim",
                    "min_nr_matched_peaks",
                ]
            ):
                setattr(
                    params, arg, self.assign_pos_int(arg, getattr(args, arg), params)
                )
            elif any(arg == i for i in ["fragment_tol", "spectral_sim_score_cutoff"]):
                setattr(
                    params,
                    arg,
                    self.assign_float_zero_one(arg, getattr(args, arg), params),
                )
            elif any(arg == i for i in ["flag_ms2query", "flag_ms2query_blank"]):
                setattr(
                    params,
                    arg,
                    self.assign_bool(arg, getattr(args, arg, params), params),
                )
            elif any(arg == i for i in ["rel_int_range", "ms2query_filter_range"]):
                setattr(
                    params,
                    arg,
                    self.assign_range_zero_one(
                        arg,
                        getattr(
                            args,
                            arg,
                        ),
                        params,
                    ),
                )
            elif arg == "spectral_sim_network_alg":
                setattr(
                    params,
                    arg,
                    self.assign_network_alg(arg, getattr(args, arg), params),
                )

        return params
