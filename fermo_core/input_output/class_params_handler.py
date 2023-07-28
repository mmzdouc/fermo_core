"""Organize, handle, and validate input from graphical user interface and command line.

TBA # TODO(MMZ)
"""

import argparse
import pandas as pd
from pathlib import Path
from typing import Self, Tuple, Any, Type

from pandas.errors import ParserError


class ParamsHandler:
    """Organize user input for processing by fermo_core.

    Interface for user input from both graphical user interface and command line.
    Receives input, tests for validity, holds parameter as attributes.

    Attributes:
        version: Current program version.
        root: "Root" directory of program.
        flag_comm_line: Indicates command line mode or GUI
        session: Fermo json session file.
        peaktable_mzmine3: Mzmine3-style peaktable.
        msms_mgf: Mgf-style msms file.
        phenotype_fermo: Fermo-style phenotypic data file.
        group_fermo: Fermo-style group data file.
        speclib_mgf: Mgf-style spectral library file.
        mass_dev_ppm: Expected mass deviation tolerance in ppm.
        msms_frag_min: Minimum tolerable number of msms fragments per spectrum.
        phenotype_fold: Fold-factor to retain features in sub-inhibitory
            concentration.
        column_ret_fold: Fold-factor to retain features cross-bleeding in blanks.
        fragment_tol: Tolerance in m/z to connect features by spectral sim.
        spectral_sim_score_cutoff: Cutoff tolerance to connect features by
            spectra similarity.
        max_nr_links_spec_sim: Maximum tolerable nr of connections to other
            features per feature.
        min_nr_matched_peaks: Minimum tolerable nr of peaks for a match in
            spectral similarity matching.
        spectral_sim_network_alg: Selected spectral similarity networking algorithm.
        flag_ms2query: Flag for annotation by ms2query.
        flag_ms2query_blank: Flag for blank-associated feature annotation by
            ms2query.
        ms2query_filter_range: Restrict annotation by ms2query based on
            relative intensity.
        rel_int_range: Restrict processing of features based on relative
            intensity.
    """

    def __init__(self: Self, version: str, root: Path, flag_comm_line: bool):
        self.version: str = version
        self.root: Path = root
        self.flag_comm_line: bool = flag_comm_line
        self.session: Path | None = None
        self.peaktable_mzmine3: Path | None = None
        self.msms_mgf: Path | None = None
        self.phenotype_fermo: Path | None = None
        self.group_fermo: Path | None = None
        self.speclib_mgf: Path | None = None
        self.mass_dev_ppm: int = 20
        self.msms_frag_min: int = 5
        self.phenotype_fold: int = 10
        self.column_ret_fold: int = 10
        self.fragment_tol: float = 0.1
        self.spectral_sim_score_cutoff: float = 0.7
        self.max_nr_links_spec_sim: int = 10
        self.min_nr_matched_peaks: int = 5
        self.spectral_sim_network_alg: str = "modified_cosine"
        self.flag_ms2query: bool = False
        self.flag_ms2query_blank: bool = False
        self.ms2query_filter_range: Tuple[float, float] = (0.0, 1.0)
        self.rel_int_range: Tuple[float, float] = (0.0, 1.0)

    def define_argparse_args(self: Self) -> argparse.ArgumentParser:
        """Define command line options and default values.

        Returns:
            argparse.ArgumentParser:
                argparse object containing command line options

        Notes:
            MMZ 27.8.23
            Once multiple competing input files are supported, the argparse
            arguments can be put into multiple mutually exclusive groups
        """
        parser = argparse.ArgumentParser(
            description=(
                "#####################################################\n"
                f"fermo_core v{self.version}: command line interface of "
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
            default=self.mass_dev_ppm,
            required=False,
            help=(
                "Expected mass deviation tolerance in ppm.\n"
                f"(default: {self.mass_dev_ppm}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--msms_frag_min",
            type=int,
            default=self.msms_frag_min,
            required=False,
            help=(
                "Minimum number of fragments per MS/MS spectrum.\n"
                f"(default: {self.msms_frag_min}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--phenotype_fold",
            type=int,
            default=self.phenotype_fold,
            required=False,
            help=(
                "Factor to retain metabolites present in samples with sub-inhibitory\n"
                "concentrations.\n"
                f"(default: {self.phenotype_fold}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--column_ret_fold",
            type=int,
            default=self.column_ret_fold,
            required=False,
            help=(
                "Factor to retain metabolites that were detected in sample blanks \n"
                "due to cross-contamination.\n"
                f"(default: {self.column_ret_fold}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--fragment_tol",
            type=float,
            default=self.fragment_tol,
            required=False,
            help=(
                "Tolerance when matching two MS/MS fragments in spectral similarity\n"
                "matching, in m/z units.\n"
                f"(default: {self.fragment_tol}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--spectral_sim_score_cutoff",
            type=float,
            default=self.spectral_sim_score_cutoff,
            required=False,
            help=(
                "Similarity score cutoff to determine relatedness of two MS/MS spectra.\n"
                f"(default: {self.spectral_sim_score_cutoff}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--max_nr_links_spec_sim",
            type=int,
            default=self.max_nr_links_spec_sim,
            required=False,
            help=(
                "In spectral similarity/molecular network calculations, maximum number\n"
                "of links to other molecular features any molecular feature is allowed\n"
                "to have.\n"
                f"(default: {self.max_nr_links_spec_sim}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--min_nr_matched_peaks",
            type=int,
            default=self.min_nr_matched_peaks,
            required=False,
            help=(
                "For spectral similarity matching, minimum number of fragments\n"
                "two MS/MS spectra need to share to be considered related.\n"
                f"(default: {self.min_nr_matched_peaks}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--spectral_sim_network_alg",
            type=str,
            default=self.spectral_sim_network_alg,
            required=False,
            choices=["all", "modified_cosine", "ms2deepscore"],
            help=(
                "For spectral similarity matching, spectral similarity/molecular\n"
                "networking algorithm to use.\n"
                f"(default: {self.spectral_sim_network_alg}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--flag_ms2query",
            type=bool,
            choices=[True, False],
            default=self.flag_ms2query,
            required=False,
            help=(
                "Flag to enable/disable annotation by MS2Query.\n"
                "This can increase calculation time.\n"
                f"(default: {self.flag_ms2query}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--flag_ms2query_blank",
            type=bool,
            choices=[True, False],
            default=self.flag_ms2query_blank,
            required=False,
            help=(
                "Flag to enable/disable annotation of sample blank-associated molecular\n"
                "features by MS2Query. This can increase calculation time.\n"
                f"(default: {self.flag_ms2query_blank}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--ms2query_filter_range",
            nargs="+",
            type=float,
            default=self.ms2query_filter_range,
            required=False,
            help=(
                "Restrict annotation by ms2query to a range based on relative\n"
                "intensity (e.g. 0.1 to 1.0, excluding molecular features\n"
                "with a relative intensity of less than 0.1.)\n"
                "Expected input: 'n' 'm' (lower and upper boundary, max. 2 values).\n"
                "Example input: '0.1 1.0'\n"
                f"(default: {self.ms2query_filter_range}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--rel_int_range",
            nargs="+",
            type=float,
            default=self.rel_int_range,
            required=False,
            help=(
                "Restrict processing of molecular features by fermo to a range based\n"
                "on relative intensity (e.g. 0.1 to 1.0, excluding molecular features\n"
                "with a relative intensity of less than 0.1.)\n"
                "Expected input: 'n' 'm' (lower and upper boundary, max. 2 values).\n"
                "Example input: '0.1 1.0'\n"
                f"(default: {self.rel_int_range}).\n"
                "For more information, see the docs.\n"
            ),
        )
        return parser

    def run_argparse(self: Self) -> None:
        """Run argparse comm line interface and assign input to object attributes."""
        parser = self.define_argparse_args()
        args = parser.parse_args()

        self.valid_mass_dev_ppm(args.mass_dev_ppm)

        #  Placeholder for increase of compatibility to other peaktable styles
        if args.peaktable_mzmine3 is not None:
            self.valid_file_exists(args.peaktable_mzmine3)
            self.valid_csv_file(args.peaktable_mzmine3)
            self.valid_peaktable_mzmine3(args.peaktable_mzmine3)
        else:
            raise ValueError("No peaktable provided")

    def valid_mass_dev_ppm(self: Self, in_value: int) -> None | str:
        """Validate mass_dev_ppm for type and plausibility.

        Args:
            in_value: mass deviation in ppm. Measure for mass accuracy.

        Returns:
            Positive validation assigns in_value to attribute and returns None as signal.
            Negative outcome raises Error when in command line mode and returns a
            message in GUI mode.
        """
        if not isinstance(in_value, int):
            message = "Mass deviation is not an integer value!"
        elif in_value > 100:
            message = "Mass deviation is unreasonably high (>100). Set a lower value."
        elif in_value <= 0:
            message = "Mass deviation is unreasonably low (<= 0). Set a higher value."
        else:
            self.mass_dev_ppm = in_value
            return None

        if self.flag_comm_line:
            raise ValueError(message)
        else:
            return message

    def valid_file_exists(self: Self, in_value: str) -> None | str:
        """Validate if file exists

        Returns:
            If file exists, returns None.
            If file does not exist, raises error if in command line mode and returns
            message if in GUI mode
        """
        if not Path.exists(Path(in_value)):
            message = f"File '{in_value}' does not exist!"
        else:
            return None

        if self.flag_comm_line:
            raise ValueError(message)
        else:
            return message

    def valid_csv_file(self: Self, in_value: str) -> None | str:
        """Validate if file is a csv file

        Returns:
            If file exists, returns None.
            If file does not exist, raises error if in command line mode and returns
            message if in GUI mode
        """
        try:
            pd.read_csv(in_value)
            return None
        except ParserError:
            message = f"File {in_value} is not a .csv-file."

        if self.flag_comm_line:
            raise ValueError(message)
        else:
            return message

    def valid_peaktable_mzmine3(self: Self, in_value: str) -> None | str:
        """Validate format of mzmine3 style peaktable

        Args:
            in_value: str of filename of mzmine3 style peaktable

        Returns:
            Positive validation assigns in_value to attribute and returns None as signal.
            Negative outcome raises Error when in command line mode and returns a
            message in GUI mode.
        """
        df = pd.read_csv(in_value)

        if df.filter(regex="^id$").columns.empty:
            message = f"File {in_value} is missing columns titled 'id'"
        # expand TODO(MMZ)
        else:
            self.peaktable_mzmine3 = Path(in_value)
            return None

        if self.flag_comm_line:
            raise ValueError(message)
        else:
            return message

    # def val_user_inp_type(self: Self, user_inp: Any, ipt_type: Type) -> Any | None:
    #     """Validate user input to recognize wrong input format.
    #
    #     Args:
    #         user_inp: User input to be validated.
    #         ipt_type: Format to validate for.
    #
    #     Returns:
    #         Input filename string or None to inform calling function.
    #     """
    #     if user_inp is not None and isinstance(user_inp, ipt_type):
    #         return user_inp
    #     else:
    #         return None

    # def run_argparse(self: Self) -> None:
    #     """Run argparse comm line interface and assign input to object attributes.
    #
    #     TODO(MMZ) - expand description
    #     """
    #
    #
    #     if self.val_user_inp_type(args.peaktable_mzmine3, list) is not None:
    #         self.peaktable_mzmine3 = args.peaktable_mzmine3[0]
    #
    #     if self.val_user_inp_type(args.msms_mgf, list) is not None:
    #         self.msms_mgf = args.msms_mgf[0]
    #
    #     if self.val_user_inp_type(args.phenotype_fermo, list) is not None:
    #         self.phenotype_fermo = args.phenotype_fermo[0]
    #
    #     if self.val_user_inp_type(args.group_fermo, list) is not None:
    #         self.group_fermo = args.group_fermo[0]
    #
    #     if self.val_user_inp_type(args.speclib_mgf, list) is not None:
    #         self.speclib_mgf = args.speclib_mgf[0]
    #
    #     self.mass_dev_ppm = self.val_user_inp_type(args.mass_dev_ppm, int)
    #     self.msms_frag_min = self.val_user_inp_type(args.msms_frag_min, int)
    #     self.phenotype_fold = self.val_user_inp_type(args.phenotype_fold, int)
    #     self.column_ret_fold = self.val_user_inp_type(args.column_ret_fold, int)
    #     self.fragment_tol = self.val_user_inp_type(args.fragment_tol, float)
    #     self.spectral_sim_score_cutoff = self.val_user_inp_type(
    #         args.spectral_sim_score_cutoff, float
    #     )
    #     self.max_nr_links_spec_sim = self.val_user_inp_type(
    #         args.max_nr_links_spec_sim, int
    #     )
    #     self.min_nr_matched_peaks = self.val_user_inp_type(
    #         args.min_nr_matched_peaks, int
    #     )
    #     self.spectral_sim_network_alg = self.val_user_inp_type(
    #         args.spectral_sim_network_alg, str
    #     )
    #     self.flag_ms2query = self.val_user_inp_type(
    #         args.flag_ms2query, bool
    #     )
    #     self.flag_ms2query_blank = self.val_user_inp_type(
    #         args.flag_ms2query_blank, bool
    #     )
    #
    #     if self.val_user_inp_type(args.ms2query_filter_range, list) is not None:
    #         self.ms2query_filter_range = (
    #             args.ms2query_filter_range[0], args.ms2query_filter_range[1]
    #         )
    #
    #     if self.val_user_inp_type(args.rel_int_range, list) is not None:
    #         self.rel_int_range = (args.rel_int_range[0], args.rel_int_range[1])
    #
    #
    #     return None
    #
