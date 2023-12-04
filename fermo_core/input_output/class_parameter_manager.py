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

import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Self, Optional

from fermo_core.input_output.class_validation_manager import ValidationManager

from fermo_core.input_output.input_file_parameter_managers import (
    PeaktableParameters,
    MsmsParameters,
    PhenotypeParameters,
    GroupMetadataParameters,
    SpecLibParameters,
)
from fermo_core.input_output.core_module_parameter_managers import (
    AdductAnnotationParameters,
    SpecSimNetworkCosineParameters,
    SpecSimNetworkDeepscoreParameters,
)
from fermo_core.input_output.additional_module_parameter_managers import (
    PeaktableFilteringParameters,
    BlankAssignmentParameters,
    PhenotypeAssignmentFoldParameters,
    SpectralLibMatchingCosineParameters,
    SpectralLibMatchingDeepscoreParameters,
    Ms2QueryAnnotationParameters,
)


class ParameterManager(BaseModel):
    """Handle parameters for processing by fermo_core.

    Handle input from both graphical user interface and command line,
    well as default values, for downstream processing. More information on default
    parameters and the properties of the dicts can be found in
    fermo_core/config/default_parameters.json

    Attributes:
        PeaktableParameters: instance of class handling peaktable parameters or None
        MsmsParameters: instance of class handling MS/MS parameters or None
        PhenotypeParameters: instance of class handling phenotype parameters or None
        GroupMetadataParameters: instance of class handling metadata parameters or None
        SpecLibParameters: instance of class handling spectra library parameters or Non
        AdductAnnotationParameters:
        SpecSimNetworkCosineParameters:
        SpecSimNetworkDeepscoreParameters:
        PeaktableFilteringParameters:
        BlankAssignmentParameters:
        PhenotypeAssignmentFoldParameters:
        SpectralLibMatchingCosineParameters:
        SpectralLibMatchingDeepscoreParameters:
        Ms2QueryAnnotationParameters:
        TODO(MMZ 04.12.23): complete docstring
    """

    PeaktableParameters: Optional[PeaktableParameters] = None
    MsmsParameters: Optional[MsmsParameters] = None
    PhenotypeParameters: Optional[PhenotypeParameters] = None
    GroupMetadataParameters: Optional[GroupMetadataParameters] = None
    SpecLibParameters: Optional[SpecLibParameters] = None
    AdductAnnotationParameters: AdductAnnotationParameters = (
        AdductAnnotationParameters()
    )
    SpecSimNetworkCosineParameters: SpecSimNetworkCosineParameters = (
        SpecSimNetworkCosineParameters()
    )
    SpecSimNetworkDeepscoreParameters: SpecSimNetworkDeepscoreParameters = (
        SpecSimNetworkDeepscoreParameters()
    )
    PeaktableFilteringParameters: PeaktableFilteringParameters = (
        PeaktableFilteringParameters()
    )
    BlankAssignmentParameters: BlankAssignmentParameters = BlankAssignmentParameters()
    PhenotypeAssignmentFoldParameters: PhenotypeAssignmentFoldParameters = (
        PhenotypeAssignmentFoldParameters()
    )
    SpectralLibMatchingCosineParameters: SpectralLibMatchingCosineParameters = (
        SpectralLibMatchingCosineParameters()
    )
    SpectralLibMatchingDeepscoreParameters: SpectralLibMatchingDeepscoreParameters = (
        SpectralLibMatchingDeepscoreParameters()
    )
    Ms2QueryAnnotationParameters: Ms2QueryAnnotationParameters = (
        Ms2QueryAnnotationParameters()
    )

    def assign_parameters(self: Self, user_params: dict):
        """Assigns user-input to different methods for attribute modification.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if (info := user_params.get("files").get("peaktable")) is not None:
            self.assign_peaktable(info)
        if (info := user_params.get("files").get("msms")) is not None:
            self.assign_peaktable(info)

    def assign_peaktable(self: Self, user_params: dict):
        """Assign peaktable params to self.PeaktableParameters

        Parameters:
            user_params: user-provided params, read from json file

        Raises:
            Exception: catch for specific exception by PeaktableParameters()
        """
        try:
            self.PeaktableParameters = PeaktableParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for 'peaktable'."
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
                f"Validated and assigned user-specified parameter 'MS/MS "
                f"information' "
                f"'{user_params['msms']['filename']}' in "
                f"'{user_params['msms']['format']}' format."
            )
        except Exception as e:
            logging.error(str(e))
            logging.warning("Could not detect MS/MS information file - SKIP.")
            self.msms = default_params.get("msms")

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
                f"Validated and assigned user-specified parameter "
                f"'phenotype/bioactivity "
                f"information' "
                f"'{user_params['phenotype']['filename']}' in "
                f"'{user_params['phenotype']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect phenotype file - SKIP.")
            self.phenotype = default_params.get("phenotype")

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
                f"Validated and assigned user-specified parameter 'group metadata "
                f"information' "
                f"'{user_params['group_metadata']['filename']}' in "
                f"'{user_params['group_metadata']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect group metadata file - SKIP.")
            self.group_metadata = default_params.get("group_metadata")

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

            self.spectral_library = user_params.get("spectral_library")
            logging.info(
                f"Validated and assigned user-specified parameter 'MS/MS spectral "
                f"library' "
                f"'{user_params['spectral_library']['filename']}' in "
                f"'{user_params['spectral_library']['format']}' format."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning("Could not detect spectral library file - SKIP.")
            self.spectral_library = default_params.get("spectral_library")

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
                        ValidationManager.validate_positive_number(
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
                "Validated and assigned user-specified parameter "
                "'phenotype_algorithm_settings'."
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
            ValidationManager.validate_positive_number(
                user_params["mass_dev_ppm"]["value"]
            )
            ValidationManager.validate_mass_deviation_ppm(
                user_params["mass_dev_ppm"]["value"]
            )

            self.mass_dev_ppm = int(user_params["mass_dev_ppm"]["value"])
            logging.info(
                f"Validated and assigned user-specified parameter to 'mass_dev_ppm': "
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
            ValidationManager.validate_positive_number(
                user_params["msms_frag_min"]["value"]
            )

            self.msms_frag_min = int(user_params["msms_frag_min"]["value"])
            logging.info(
                f"Validated and assigned user-specified parameter to 'msms_frag_min': "
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
            ValidationManager.validate_positive_number(
                user_params["column_ret_fold"]["value"]
            )

            self.column_ret_fold = int(user_params["column_ret_fold"]["value"])
            logging.info(
                f"Validated and assigned user-specified parameter to "
                f"'column_ret_fold': "
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
            ValidationManager.validate_positive_number(
                user_params["fragment_tol"]["value"]
            )

            self.fragment_tol = float(user_params["fragment_tol"]["value"])
            logging.info(
                f"Validated and assigned user-specified parameter to 'fragment_tol': "
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
            ValidationManager.validate_positive_number(
                user_params["spectral_sim_score_cutoff"]["value"]
            )

            self.spectral_sim_score_cutoff = float(
                user_params["spectral_sim_score_cutoff"]["value"]
            )
            logging.info(
                f"Validated and assigned user-specified parameter to "
                f"'spectral_sim_score_cutoff':"
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
            ValidationManager.validate_positive_number(
                user_params["max_nr_links_spec_sim"]["value"]
            )

            self.max_nr_links_spec_sim = int(
                user_params["max_nr_links_spec_sim"]["value"]
            )
            logging.info(
                f"Validated and assigned user-specified parameter to "
                f"'max_nr_links_spec_sim': "
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
            ValidationManager.validate_positive_number(
                user_params["min_nr_matched_peaks"]["value"]
            )

            self.min_nr_matched_peaks = int(
                user_params["min_nr_matched_peaks"]["value"]
            )
            logging.info(
                f"Validated and assigned user-specified parameter to "
                f"'min_nr_matched_peaks': "
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
                f"Validated and assigned user-specified parameter to "
                f"'spectral_sim_network_alg': "
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
            logging.info("Validated and assigned user-specified parameter 'ms2query'.")

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
                "Validated and assigned user-specified parameter to 'rel_int_range': "
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

    def assign_max_library_size(self: Self, user_params: dict, default_params: dict):
        """Validate and assign the maximum spectra library size setting to self.

        Parameters:
            user_params: user-provided params, read from json file
            default_params: default parameters read from json file, serves as fallback

        Notes:
            Optional parameter, raises no error.
        """
        try:
            ValidationManager.validate_keys(user_params, "max_library_size")
            ValidationManager.validate_keys(user_params["max_library_size"], "value")
            ValidationManager.validate_integer(user_params["max_library_size"]["value"])
            ValidationManager.validate_positive_number(
                user_params["max_library_size"]["value"]
            )

            self.max_library_size = int(user_params["max_library_size"]["value"])
            logging.info(
                f"Validated and assigned user-specified parameter to "
                f"'max_library_size': "
                f"'{user_params['max_library_size']['value']}'."
            )

        except Exception as e:
            logging.warning(str(e))
            logging.warning(
                "Could not detect/process parameter 'max_library_size'. "
                "Assigned the default value: "
                f"'{default_params['max_library_size']['value']}'."
            )
            self.max_library_size = default_params["max_library_size"]["value"]

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
                case "max_library_size":
                    self.assign_max_library_size(user_params, default_params)

        logging.info("Completed assignment of user-provided parameters.")
