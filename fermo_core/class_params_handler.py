"""Organize functions and parameters from both user interface and command line.

Contains the ParamsHandler class that stores run parameters (user input) and holds
methods regarding command line input.
"""

import argparse
from pathlib import Path
from typing import List, Self


class ParamsHandler:
    """Organize functions and parameters from both user interface and command line.

    Attributes:
        version (str): Current program version.
        root (Path): "Root" directory of program.
        session (Path | None): Path to fermo json session file.
        peaktable_mzmine3 (Path | None): Path to mzmine3-style peaktable or None.
        msms_mgf (Path | None): Path to mgf-style msms file or None.
        phenotype_fermo (Path | None): Path to fermo-style phenotypic data file or None.
        group_fermo (Path | None): Path to fermo-style group data file or None.
        speclib_mgf (Path | None): Path to mgf-style spectral library file or None.
        mass_dev_ppm (int): Expected mass deviation tolerance in ppm.
        msms_frag_min (int): Minimum tolerable number of msms fragments per spectrum.
        phenotype_fold (int): Fold-factor to retain features in sub-inhibitory conc.
        column_ret_fold (int): Fold-factor to retain features cross-bleeding in blanks.
        fragment_tol (float): Tolerance in m/z to connect features by spectral sim.
        spectral_sim_score_cutoff (float): Cutoff tolerance to connect features by
            spectra similarity.
        max_nr_links_spec_sim (int): Maximum tolerable nr of connections to other
            features per feature.
        min_nr_matched_peaks (int): Minimum tolerable nr of peaks for a match in
            spectral similarity matching.
        flag_ms2query (bool): Flag for annotation by ms2query.
        flag_ms2query_blank (bool): Flag for blank-associated feature annotation by
            ms2query.
        ms2query_filter_range (List): Restrict annotation by ms2query based on
            relative intensity
        spectral_sim_network_alg (str): Selected spectral similarity networking algorithm.
        rel_int_range (List): Restrict processing of features based on relative intensity.

    Methods:
        run_argparse():
            Run argparse comm line interface and assign params to attributes.

            Run the argparse object and assign the user-provided args to the
            ParamsHandler object attributes.

        define_argparse_args():
            Initialize argparse object and add arguments.

            Returns:
                argparse.ArgumentParser : argparse object

            Notes:
                MMZ 27.8.23
                Once multiple competing input files are supported, the argparse
                arguments can be put into multiple mutually exclusive groups

    Notes:
        MMZ 27.8.23
        Main point of entry for input data and parameters.
        Attributes can be expanded for additional compatibility and input formats.
        Further implementation into downstream reading and parsing modules necessary.
        Furthermore, compatibility with Feature and Sample objects and processing
        objects must be created and the Dashboard needs to be adjusted accordingly.
    """

    def __init__(self: Self, version: str, root: Path):
        self.version: str = version
        self.root: Path = root
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
        self.flag_ms2query: bool = False
        self.flag_ms2query_blank: bool = False
        self.ms2query_filter_range: List = [0, 1]
        self.spectral_sim_network_alg: str = "mod_cosine"
        self.rel_int_range: List = [0, 1]

    def define_argparse_args(self: Self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=(
                "#####################################################\n"
                f"fermo_core: command line interface of FERMO v{self.version}\n"
                "#####################################################\n"
                "The command line version of fermo focuses on large-scale processing.\n"
                "For a more user-friendly experience, see fermo.bioinformatics.nl\n"
                "More info on usage can be found in the README, Docs, or publication.\n"
                "#####################################################\n"
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "--peaktable_mzmine3",
            nargs=1,
            type=str,
            required=True,
            help="Provide a MZmine3 style peaktable in the .csv-format.",
        )

        parser.add_argument(
            "--msms_mgf",
            nargs=1,
            type=str,
            required=True,
            help="Provide a file with ms/ms information in the .mgf-format.",
        )

        parser.add_argument(
            "--phenotype_fermo",
            nargs=1,
            type=str,
            default=None,
            required=False,
            help="Provide a file with phenotype information in the .mgf-format.",
        )

        parser.add_argument(
            "--group_fermo",
            nargs=1,
            type=str,
            default=None,
            required=False,
            help="Provide a file with group information in the .mgf-format.",
        )

        parser.add_argument(
            "--speclib_mgf",
            nargs=1,
            type=str,
            default=None,
            required=False,
            help="Provide a spectral library file in the .mgf-format.",
        )

        parser.add_argument(
            "--mass_dev_ppm",
            nargs=1,
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
            nargs=1,
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
            nargs=1,
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
            nargs=1,
            type=int,
            default=self.column_ret_fold,
            required=False,
            help=(
                "Factor to retain metabolites that were detected in sample blanks \n"
                "due to corss-contamination.\n"
                f"(default: {self.column_ret_fold}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--fragment_tol",
            nargs=1,
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
            nargs=1,
            type=float,
            default=self.spectral_sim_score_cutoff,
            required=False,
            help=(
                "Tolerance when matching two MS/MS fragments in spectral similarity\n"
                "matching, in m/z units.\n"
                f"(default: {self.spectral_sim_score_cutoff}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--max_nr_links_spec_sim",
            nargs=1,
            type=int,
            default=self.max_nr_links_spec_sim,
            required=False,
            help=(
                "For spectral similarity/molecular network calculation, maximum number\n"
                "of links to other molecular features any molecular feature is allowed\n "
                "to have.\n"
                f"(default: {self.max_nr_links_spec_sim}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--min_nr_matched_peaks",
            nargs=1,
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
            "--flag_ms2query",
            nargs=1,
            type=bool,
            default=self.flag_ms2query,
            required=False,
            help=(
                "Flag to enable/disable annotation by MS2Query.\n"
                "Allowed values: 'True' (enabled); 'False' (disabled).\n"
                f"(default: {self.flag_ms2query}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--flag_ms2query_blank",
            nargs=1,
            type=bool,
            default=self.flag_ms2query_blank,
            required=False,
            help=(
                "Flag to enable/disable annotation of sample blank-associated molecular\n"
                "features by MS2Query. This increases calculation time.\n"
                "Allowed values: 'True' (enabled); 'False' (disabled).\n"
                f"(default: {self.flag_ms2query_blank}).\n"
                "For more information, see the docs.\n"
            ),
        )

        parser.add_argument(
            "--ms2query_filter_range",
            nargs="+",
            type=int,
            default=self.ms2query_filter_range,
            required=False,
            help=(
                "Restrict annotation by ms2query to a range based on relative\n"
                "intensity. This can be 0.1 to 1, which excludes all molecular features\n"
                "with a relative intensity of less than 0.1.\n"
                "Allowed values: 'n' (lower boundry); 'm' (upper boundry).\n"
                "Example input: 0 1; 0.1 1; 0 0.8 .\n"
                f"(default: {self.ms2query_filter_range}).\n"
                "For more information, see the docs.\n"
            ),
        )

        # self.ms2query_filter_range: List = [0, 1]
        # self.spectral_sim_network_alg: str = 'mod_cosine'
        # self.rel_int_range: List = [0, 1]

        return parser

    def run_argparse(self: Self) -> None:
        parser = self.define_argparse_args()
        args = parser.parse_args()
        print(args)
        #  TODO: "unpack" the args into the appropriate attributes
