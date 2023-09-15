"""Hold parameters for downstream data processing and analysis.

Interface to collect and hold user input from both command line and GUI.

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
import logging
import json
from pathlib import Path
from typing import Self, Tuple, Optional

from fermo_core.input_output.class_validation_manager import ValidationManager


class ParameterManager:
    """Handle parameters for processing by fermo_core.

    Handle input from both graphical user interface and command line,
    well as default values, for downstream processing.

    More information on default parameters and the properties of the dicts can be
    found in fermo_core/config/default_parameters.json

    Attributes:
        version: Current program version.
        root: "Root" directory of program.
        session: Fermo json session file.
        ---files---
        peaktable: Sample/feature information.
        msms: MS/MS information on molecular features.
        phenotype: phenotype/bioactivity information.
        group_metadata: sample grouping info.
        speclib_mgf: Annotated MS/MS spectra.
        ---parameters---
        phenotype_algorithm_settings: setting for phenotype algorithms
        mass_dev_ppm: Expected mass deviation tolerance in ppm.
        msms_frag_min: Minimum tolerable number of msms fragments per spectrum.
        column_ret_fold: Fold-factor to determine blank-associated features.
        fragment_tol: Tolerance in m/z to connect features by spectral sim.
        spectral_sim_score_cutoff: Cutoff tolerance spectra similarity.
        max_nr_links_spec_sim: Maximum tolerable nr of connections.
        min_nr_matched_peaks: Minimum tolerable nr of peaks for a spec sim match.
        spectral_sim_network_alg: Selected spectral similarity networking algorithm.
        ms2query: Info on running MS2Query annotation.
        rel_int_range: Restrict processing of features based on relative intensity.
    """

    def __init__(self: Self, version: str, root: Path):
        self.version: str = version
        self.root: Path = root
        self.session: Optional[dict] = None
        self.peaktable: Optional[dict] = None
        self.msms: Optional[dict] = None
        self.phenotype: Optional[dict] = None
        self.group_metadata: Optional[dict] = None
        self.speclib_mgf: Optional[dict] = None
        self.phenotype_algorithm_settings: Optional[dict] = None
        self.mass_dev_ppm: Optional[int] = None
        self.msms_frag_min: Optional[int] = None
        self.column_ret_fold: Optional[int] = None
        self.fragment_tol: Optional[float] = None
        self.spectral_sim_score_cutoff: Optional[float] = None
        self.max_nr_links_spec_sim: Optional[int] = None
        self.min_nr_matched_peaks: Optional[int] = None
        self.spectral_sim_network_alg: Optional[str] = None
        self.ms2query: Optional[dict] = None
        self.rel_int_range: Optional[Tuple[float, float]] = None

    def define_argparse_args(self: Self) -> argparse.ArgumentParser:
        """Define command line options.

        Returns:
            argparse object containing command line options.

        """
        parser = argparse.ArgumentParser(
            description=(
                "#####################################################\n"
                f"fermo_core v{self.version}: command line interface of FERMO.\n"
                "#####################################################\n"
                "Focused on large-scale data processing by advanced users.\n"
                "For a more user-friendly experience, see fermo.bioinformatics.nl\n"
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
                "Provide a .json file containing parameters.\n"
                "See 'parameters.json' for an example or consult the documentation.\n"
            ),
        )
        return parser

    def run_argparse(self: Self) -> argparse.Namespace:
        """Run argparse comm line interface.

        Returns:
            Namespace containing the command line params.
        """
        parser = self.define_argparse_args()
        return parser.parse_args()

    @staticmethod
    def load_json_file(json_file: str) -> dict:
        """Validates json file and attempts to load it.

        Parameters:
            json_file: a filepath to a json file

        Returns:
            The loaded file as a dict.
        """
        try:
            ValidationManager.validate_string(json_file)
            ValidationManager.validate_file_exists(json_file)
            ValidationManager.validate_file_extension(json_file, ".json")

            with open(Path(json_file)) as infile:
                return json.load(infile)

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file '{json_file}': wrong format.")
            raise e
        except Exception as e:
            logging.error(str(e))
            raise e

    def assign_peaktable(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the peaktable information to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Raises:
            Exception: catch for more specific exception raised by methods in
            ValidationManager.

        Notes:
            Expand here for other file formats.
        """
        try:
            ValidationManager.validate_keys(user_params, "peaktable")
            ValidationManager.validate_keys(
                user_params.get("peaktable"),
                "filename",
                "format",
            )
            ValidationManager.validate_string(user_params["peaktable"]["filename"])
            ValidationManager.validate_file_exists(user_params["peaktable"]["filename"])
            ValidationManager.validate_value_in_list(
                default_params["peaktable"]["allowed_formats"],
                user_params["peaktable"]["format"],
            )
            match user_params["peaktable"]["format"]:
                case "mzmine3":
                    ValidationManager.validate_file_extension(
                        user_params["peaktable"]["filename"], ".csv"
                    )
                    ValidationManager.validate_csv_file(
                        user_params["peaktable"]["filename"]
                    )
                    ValidationManager.validate_peaktable_mzmine3(
                        user_params["peaktable"]["filename"]
                    )
                    ValidationManager.validate_no_duplicate_entries_csv_column(
                        user_params["peaktable"]["filename"], "id"
                    )
                case _:
                    raise ValueError(
                        f"Could not recognize peaktable format "
                        f"'{user_params['peaktable']['format']}'."
                    )

            self.peaktable = user_params.get("peaktable")
            logging.info(
                f"Validated and assigned MZmine3-style peaktable "
                f"'{user_params['peaktable']['filename']}'."
            )
        except Exception as e:
            logging.error(str(e))
            raise e

    def assign_msms(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the msms information to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Raises:
            Exception: catch for more specific exception raised by methods in
            ValidationManager.

        Notes:
            Expand here for other file formats.
        """
        try:
            ValidationManager.validate_keys(user_params, "msms")
            ValidationManager.validate_keys(
                user_params.get("msms"),
                "filename",
                "format",
            )
            ValidationManager.validate_string(user_params["msms"]["filename"])
            ValidationManager.validate_file_exists(user_params["msms"]["filename"])
            ValidationManager.validate_value_in_list(
                default_params["msms"]["allowed_formats"], user_params["msms"]["format"]
            )

            match user_params["msms"]["format"]:
                case "mgf":
                    ValidationManager.validate_file_extension(
                        user_params["msms"]["filename"], ".mgf"
                    )
                    ValidationManager.validate_mgf_file(user_params["msms"]["filename"])
                case _:
                    raise ValueError(
                        f"Could not recognize MS/MS format "
                        f"'{user_params['msms']['format']}'."
                    )

            self.msms = user_params.get("msms")
            logging.info(
                f"Validated and assigned mgf-style MS/MS information "
                f"'{user_params['msms']['filename']}'."
            )
        except Exception as e:
            logging.error(str(e))
            raise e

    def assign_phenotype(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the phenotype information to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
            Expand here for other file formats.

            A fermo-style phenotype data file is a .csv-file with the layout:

            sample_name,phenotype_col_1,phenotype_col_2,...,phenotype_col_n \n
            sample1,1,0.1 \n
            sample2,10,0.01 \n
            sample3,100,0.001 \n

            Ad columns: "sample_name" mandatory, one or more additional columns
            Ad values: One experiment per column. All experiments must be of the
            same type (e.g. concentration, percentage inhibition).
            This is indicated by the "mode" of the file:
            -> percentage-like (the higher the better),
            -> concentration-like (the lower the better)
        """
        try:
            ValidationManager.validate_keys(user_params, "phenotype")
            ValidationManager.validate_keys(
                user_params.get("phenotype"), "filename", "format", "mode", "algorithm"
            )
            ValidationManager.validate_string(user_params["phenotype"]["filename"])
            ValidationManager.validate_file_exists(user_params["phenotype"]["filename"])
            ValidationManager.validate_value_in_list(
                default_params["phenotype"]["allowed_formats"],
                user_params["phenotype"]["format"],
            )
            ValidationManager.validate_value_in_list(
                default_params["phenotype"]["allowed_modes"],
                user_params["phenotype"]["mode"],
            )
            ValidationManager.validate_value_in_list(
                default_params["phenotype"]["allowed_algorithms"],
                user_params["phenotype"]["algorithm"],
            )

            match user_params["phenotype"]["format"]:
                case "fermo":
                    ValidationManager.validate_file_extension(
                        user_params["phenotype"]["filename"], ".csv"
                    )
                    ValidationManager.validate_csv_file(
                        user_params["phenotype"]["filename"]
                    )
                    ValidationManager.validate_phenotype_fermo(
                        user_params["phenotype"]["filename"]
                    )
                    ValidationManager.validate_no_duplicate_entries_csv_column(
                        user_params["phenotype"]["filename"], "sample_name"
                    )
                case _:
                    raise ValueError(
                        f"Could not recognize phenotype format "
                        f"'{user_params['phenotype']['format']}'."
                    )

            self.phenotype = user_params.get("phenotype")
            logging.info(
                f"Validated and assigned FERMO-style phenotype/bioactivity "
                f"table '{user_params['phenotype']['filename']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.info("Could not recognize phenotype file - SKIP.")

    def assign_group_metadata(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the group metadata information to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
            Expand here for other file formats.

            A fermo-style group data file is a .csv-file with the layout:

            sample_name,group_col_1,group_col_2,...,group_col_n \n
            sample1,medium_A,condition_A \n
            sample2,medium_B,condition_A\n
            sample3,medium_C,condition_A \n

            Ad values: The only prohibited value is 'DEFAULT' which is reserved for
            internal use. 'BLANK' os a special value that indicates the sample/medium
            blank for automated subtraction.
        """
        try:
            ValidationManager.validate_keys(user_params, "group_metadata")
            ValidationManager.validate_keys(
                user_params.get("group_metadata"), "filename", "format"
            )
            ValidationManager.validate_string(user_params["group_metadata"]["filename"])
            ValidationManager.validate_file_exists(
                user_params["group_metadata"]["filename"]
            )
            ValidationManager.validate_value_in_list(
                default_params["group_metadata"]["allowed_formats"],
                user_params["group_metadata"]["format"],
            )
            match user_params["group_metadata"]["format"]:
                case "fermo":
                    ValidationManager.validate_file_extension(
                        user_params["group_metadata"]["filename"], ".csv"
                    )
                    ValidationManager.validate_csv_file(
                        user_params["group_metadata"]["filename"]
                    )
                    ValidationManager.validate_group_metadata_fermo(
                        user_params["group_metadata"]["filename"]
                    )
                    ValidationManager.validate_no_duplicate_entries_csv_column(
                        user_params["group_metadata"]["filename"], "sample_name"
                    )
                case _:
                    raise ValueError(
                        f"Could not recognize group metadata file format "
                        f"'{user_params['group_metadata']['format']}'."
                    )

            self.group_metadata = user_params.get("group_metadata")
            logging.info(
                f"Validated and assigned FERMO-style group metadata "
                f"table '{user_params['group_metadata']['filename']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.info("Could not process group metadata file - SKIP.")

    def assign_spectral_library(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the spectral library information to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
            Expand here for other file formats.
        """
        try:
            ValidationManager.validate_keys(user_params, "spectral_library")
            ValidationManager.validate_keys(
                user_params.get("spectral_library"), "filename", "format"
            )
            ValidationManager.validate_string(
                user_params["spectral_library"]["filename"]
            )
            ValidationManager.validate_file_exists(
                user_params["spectral_library"]["filename"]
            )
            ValidationManager.validate_value_in_list(
                default_params["spectral_library"]["allowed_formats"],
                user_params["spectral_library"]["format"],
            )
            match user_params["spectral_library"]["format"]:
                case "mgf":
                    ValidationManager.validate_file_extension(
                        user_params["spectral_library"]["filename"], ".mgf"
                    )
                    ValidationManager.validate_mgf_file(
                        user_params["spectral_library"]["filename"]
                    )
                case _:
                    raise ValueError(
                        f"Could not recognize spectral library MS/MS format "
                        f"'{user_params['spectral_library']['format']}'."
                    )

            self.speclib_mgf = user_params.get("spectral_library")
            logging.info(
                f"Validated and assigned mgf-style MS/MS spectral library "
                f"'{user_params['spectral_library']['filename']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.info("Could not process spectral library file - SKIP.")

    def assign_phenotype_algorithm_settings(
        self: Self, user_params: dict, default_params: dict
    ):
        """Validate and assign the phenotype algorithm settings to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
            Expand here for other file formats.
        """
        try:
            ValidationManager.validate_keys(user_params, "phenotype_algorithm_settings")
            for param in user_params["phenotype_algorithm_settings"].keys():
                match param:
                    case "fold_difference":
                        ValidationManager.validate_integer(
                            user_params["phenotype_algorithm_settings"][
                                "fold_difference"
                            ]["value"]
                        )
                    case _:
                        raise ValueError(
                            f"Could not recognize phenotype algorithm setting '"
                            f"{param}'."
                        )

            self.phenotype_algorithm_settings = user_params[
                "phenotype_algorithm_settings"
            ]
            logging.info("Validated and assigned phenotype_algorithm_settings.")
        except Exception as e:
            logging.warning(str(e))
            logging.info(
                "Could not process phenotype algorithm settings - fallback to "
                "default values."
            )
            self.phenotype_algorithm_settings = default_params[
                "phenotype_algorithm_settings"
            ]

    def parse_parameters(self: Self, user_params: dict, default_params: dict):
        """Parses user-provided parameters based on expected params in default_params.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback
        """
        for param in default_params.keys():
            match param:
                case "peaktable":
                    self.assign_peaktable(user_params, default_params)
                case "msms":
                    self.assign_msms(user_params, default_params)
                case "phenotype":
                    self.assign_phenotype(user_params, default_params)
                case "group_metadata":
                    self.assign_group_metadata(user_params, default_params)
                case "spectral_library":
                    self.assign_spectral_library(user_params, default_params)
                case "phenotype_algorithm_settings":
                    self.assign_phenotype_algorithm_settings(
                        user_params, default_params
                    )
                # TODO(MMZ): continue adding parameters

        # load the default params
        # assign the default params one by one to self
        # assign keys to self

    # function: parse  user parameters by comparing the expected params against what
    # the user provided; makes it more flexible/robust and allows to abort early
    # here, a case statement can be user
    # dont forget to use get to prevent keyerrors if they are not here.


# call argparse to get input file parameters json
# call function to load default_parameter file json
