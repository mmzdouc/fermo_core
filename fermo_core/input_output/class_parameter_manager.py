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
from typing import Self, Optional

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
        self.rel_int_range: Optional[dict] = None

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
                "Provide a FERMO parameter .json file.\n"
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
            Mandatory parameter.
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
                        f"'{user_params['peaktable']['format']}' of file "
                        f"'{user_params['peaktable']['filename']}'."
                    )

            self.peaktable = user_params.get("peaktable")
            logging.info(
                f"Validated and assigned user-parameter peaktable "
                f"'{user_params['peaktable']['filename']}' in "
                f"'{user_params['peaktable']['format']}' format."
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
                        f"'{user_params['msms']['format']}' of file "
                        f"'{user_params['msms']['filename']}'."
                    )

            self.msms = user_params.get("msms")
            logging.info(
                f"Validated and assigned user-parameter MS/MS information "
                f"'{user_params['msms']['filename']}' in "
                f"'{user_params['msms']['format']}' format."
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
                        f"'{user_params['phenotype']['format']}' of file "
                        f"'{user_params['phenotype']['filename']}'."
                    )

            self.phenotype = user_params.get("phenotype")
            logging.info(
                f"Validated and assigned user-parameter phenotype/bioactivity "
                f"information "
                f"'{user_params['phenotype']['filename']}' in "
                f"'{user_params['phenotype']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect phenotype file - SKIP.")

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
                        f"Could not recognize group metadata format "
                        f"'{user_params['group_metadata']['format']}' of file "
                        f"'{user_params['group_metadata']['filename']}'."
                    )

            self.group_metadata = user_params.get("group_metadata")
            logging.info(
                f"Validated and assigned user-parameter group metadata information "
                f"'{user_params['group_metadata']['filename']}' in "
                f"'{user_params['group_metadata']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect group metadata file - SKIP.")

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
                        f"'{user_params['spectral_library']['format']}' of file "
                        f"'{user_params['spectral_library']['filename']}'."
                    )

            self.speclib_mgf = user_params.get("spectral_library")
            logging.info(
                f"Validated and assigned user-parameter MS/MS spectral library "
                f"'{user_params['spectral_library']['filename']}' in "
                f"'{user_params['spectral_library']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect spectral library file - SKIP.")

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

            self.phenotype_algorithm_settings = user_params.get(
                "phenotype_algorithm_settings"
            )
            logging.info(
                "Validated and assigned user-parameter 'phenotype_algorithm_settings'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'phenotype_algorithm_settings'. "
                "Continue with default values."
            )
            self.phenotype_algorithm_settings = default_params.get(
                "phenotype_algorithm_settings"
            )

    def assign_mass_dev_ppm(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the mass deviation setting to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "mass_dev_ppm")
            ValidationManager.validate_keys(user_params["mass_dev_ppm"], "value")
            ValidationManager.validate_integer(user_params["mass_dev_ppm"]["value"])

            self.mass_dev_ppm = int(user_params["mass_dev_ppm"]["value"])
            logging.info(
                f"Validated and assigned user-parameter to 'mass_dev_ppm': "
                f"'{user_params['mass_dev_ppm']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'mass_dev_ppm'. "
                "Assigned the default value: "
                f"'{default_params['mass_dev_ppm']['value']}'."
            )
            self.mass_dev_ppm = default_params["mass_dev_ppm"]["value"]

    def assign_msms_frag_min(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the minimum mass fragments per spectrum setting to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "msms_frag_min")
            ValidationManager.validate_keys(user_params["msms_frag_min"], "value")
            ValidationManager.validate_integer(user_params["msms_frag_min"]["value"])

            self.msms_frag_min = int(user_params["msms_frag_min"]["value"])
            logging.info(
                f"Validated and assigned user-parameter to 'msms_frag_min': "
                f"'{user_params['msms_frag_min']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'msms_frag_min'. "
                "Assigned the default value: "
                f"'{default_params['msms_frag_min']['value']}'."
            )
            self.msms_frag_min = default_params["msms_frag_min"]["value"]

    def assign_column_ret_fold(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the column retention factor setting to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "column_ret_fold")
            ValidationManager.validate_keys(user_params["column_ret_fold"], "value")
            ValidationManager.validate_integer(user_params["column_ret_fold"]["value"])

            self.column_ret_fold = int(user_params["column_ret_fold"]["value"])
            logging.info(
                f"Validated and assigned user-parameter to 'column_ret_fold': "
                f"'{user_params['column_ret_fold']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'column_ret_fold'. "
                "Assigned the default value: "
                f"'{default_params['column_ret_fold']['value']}'."
            )
            self.column_ret_fold = default_params["column_ret_fold"]["value"]

    def assign_fragment_tol(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the fragmentation tolerance setting to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "fragment_tol")
            ValidationManager.validate_keys(user_params["fragment_tol"], "value")
            ValidationManager.validate_float(user_params["fragment_tol"]["value"])

            self.fragment_tol = float(user_params["fragment_tol"]["value"])
            logging.info(
                f"Validated and assigned user-parameter to 'fragment_tol': "
                f"'{user_params['fragment_tol']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'fragment_tol'. "
                "Assigned the default value: "
                f"'{default_params['fragment_tol']['value']}'."
            )
            self.fragment_tol = default_params["fragment_tol"]["value"]

    def assign_spectral_sim_score_cutoff(
        self: Self, user_params: dict, default_params: dict
    ):
        """Validate and assign the spectral similarity score cutoff to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "spectral_sim_score_cutoff")
            ValidationManager.validate_keys(
                user_params["spectral_sim_score_cutoff"], "value"
            )
            ValidationManager.validate_float(
                user_params["spectral_sim_score_cutoff"]["value"]
            )

            self.spectral_sim_score_cutoff = float(
                user_params["spectral_sim_score_cutoff"]["value"]
            )
            logging.info(
                f"Validated and assigned user-parameter to 'spectral_sim_score_cutoff':"
                f" '{user_params['spectral_sim_score_cutoff']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'spectral_sim_score_cutoff'. "
                "Assigned the default value: "
                f"'{default_params['spectral_sim_score_cutoff']['value']}'."
            )
            self.spectral_sim_score_cutoff = default_params[
                "spectral_sim_score_cutoff"
            ]["value"]

    def assign_max_nr_links_spec_sim(
        self: Self, user_params: dict, default_params: dict
    ):
        """Validate and assign the max nr of neighbours in spec sim network param.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "max_nr_links_spec_sim")
            ValidationManager.validate_keys(
                user_params["max_nr_links_spec_sim"], "value"
            )
            ValidationManager.validate_integer(
                user_params["max_nr_links_spec_sim"]["value"]
            )

            self.max_nr_links_spec_sim = int(
                user_params["max_nr_links_spec_sim"]["value"]
            )
            logging.info(
                f"Validated and assigned user-parameter to 'max_nr_links_spec_sim': "
                f"'{user_params['max_nr_links_spec_sim']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'max_nr_links_spec_sim'. "
                "Assigned the default value: "
                f"'{default_params['max_nr_links_spec_sim']['value']}'."
            )
            self.max_nr_links_spec_sim = default_params["max_nr_links_spec_sim"][
                "value"
            ]

    def assign_min_nr_matched_peaks(
        self: Self, user_params: dict, default_params: dict
    ):
        """Validate and assign the min number of corresponding peaks for match param.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "min_nr_matched_peaks")
            ValidationManager.validate_keys(
                user_params["min_nr_matched_peaks"], "value"
            )
            ValidationManager.validate_integer(
                user_params["min_nr_matched_peaks"]["value"]
            )

            self.min_nr_matched_peaks = int(
                user_params["min_nr_matched_peaks"]["value"]
            )
            logging.info(
                f"Validated and assigned user-parameter to 'min_nr_matched_peaks': "
                f"'{user_params['min_nr_matched_peaks']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'min_nr_matched_peaks'. "
                "Assigned the default value: "
                f"'{default_params['min_nr_matched_peaks']['value']}'."
            )
            self.min_nr_matched_peaks = default_params["min_nr_matched_peaks"]["value"]

    def assign_spectral_sim_network_alg(
        self: Self, user_params: dict, default_params: dict
    ):
        """Validate and assign the spectral similarity network algorithm param.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "spectral_sim_network_alg")
            ValidationManager.validate_keys(
                user_params["spectral_sim_network_alg"], "format"
            )
            ValidationManager.validate_value_in_list(
                default_params["spectral_sim_network_alg"]["allowed_formats"],
                user_params["spectral_sim_network_alg"]["format"],
            )

            self.spectral_sim_network_alg = user_params["spectral_sim_network_alg"][
                "format"
            ]
            logging.info(
                f"Validated and assigned user-parameter to 'spectral_sim_network_alg': "
                f"'{user_params['spectral_sim_network_alg']['format']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'spectral_sim_network_alg'. "
                "Assigned the default value: "
                f"'{default_params['spectral_sim_network_alg']['format']}'."
            )
            self.spectral_sim_network_alg = default_params["spectral_sim_network_alg"][
                "format"
            ]

    def assign_ms2query(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the ms2query parameter settings.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "ms2query")
            ValidationManager.validate_keys(
                user_params["ms2query"], "mode", "annot_features_from_blanks", "range"
            )
            ValidationManager.validate_value_in_list(
                default_params["ms2query"]["allowed_modes"],
                user_params["ms2query"]["mode"],
            )
            ValidationManager.validate_value_in_list(
                default_params["ms2query"]["allowed_modes_annot_features_from_blanks"],
                user_params["ms2query"]["annot_features_from_blanks"],
            )
            ValidationManager.validate_range_zero_one(user_params["ms2query"]["range"])

            self.ms2query = user_params["ms2query"]
            logging.info("Validated and assigned user-parameter 'ms2query'.")

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect/process parameter 'ms2query' - SKIP.")
            self.ms2query = default_params["ms2query"]

    def assign_rel_int_range(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the relative intensity range parameter settings.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "rel_int_range")
            ValidationManager.validate_keys(
                user_params["rel_int_range"],
                "range",
            )
            ValidationManager.validate_range_zero_one(
                user_params["rel_int_range"]["range"]
            )

            self.rel_int_range = (
                user_params["rel_int_range"]["range"][0],
                user_params["rel_int_range"]["range"][1],
            )
            logging.info(
                "Validated and assigned user-parameter to 'rel_int_range': "
                f"'{user_params['rel_int_range']['range']}'"
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'rel_int_range'. "
                "Assigned the default value: "
                f"'{default_params['rel_int_range']['range']}'."
            )
            self.rel_int_range = (
                default_params["rel_int_range"]["range"][0],
                default_params["rel_int_range"]["range"][1],
            )

    def parse_parameters(self: Self, user_params: dict, default_params: dict):
        """Validate an assign user-provided parameters.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback
        """
        logging.info("Started assignment of user-provided parameters.")
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
                case "mass_dev_ppm":
                    self.assign_mass_dev_ppm(user_params, default_params)
                case "msms_frag_min":
                    self.assign_msms_frag_min(user_params, default_params)
                case "column_ret_fold":
                    self.assign_column_ret_fold(user_params, default_params)
                case "fragment_tol":
                    self.assign_fragment_tol(user_params, default_params)
                case "spectral_sim_score_cutoff":
                    self.assign_spectral_sim_score_cutoff(user_params, default_params)
                case "max_nr_links_spec_sim":
                    self.assign_max_nr_links_spec_sim(user_params, default_params)
                case "min_nr_matched_peaks":
                    self.assign_min_nr_matched_peaks(user_params, default_params)
                case "spectral_sim_network_alg":
                    self.assign_spectral_sim_network_alg(user_params, default_params)
                case "ms2query":
                    self.assign_ms2query(user_params, default_params)
                case "rel_int_range":
                    self.assign_rel_int_range(user_params, default_params)
        logging.info("Completed assignment of user-provided parameters.")
