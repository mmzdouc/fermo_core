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
        """Modifies attributes by calling methods that take user input.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        logging.info("Started assignment of user-provided parameters.")

        self.assign_files_parameters(user_params)
        self.assign_core_modules_parameters(user_params)
        self.assign_additional_modules_parameters(user_params)

        logging.info("Completed assignment of user-provided parameters.")

    def assign_files_parameters(self: Self, user_params: dict):
        """Assigns user-input on files to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if (info := user_params.get("files").get("peaktable")) is not None:
            self.assign_peaktable(info)

        if (info := user_params.get("files").get("msms")) is not None:
            self.assign_msms(info)
        else:
            self.log_skipped_modules("msms")

        if (info := user_params.get("files").get("phenotype")) is not None:
            self.assign_phenotype(info)
        else:
            self.log_skipped_modules("phenotype")

        if (info := user_params.get("files").get("group_metadata")) is not None:
            self.assign_group_metadata(info)
        else:
            self.log_skipped_modules("group_metadata")

        if (info := user_params.get("files").get("spectral_library")) is not None:
            self.assign_spectral_library(info)
        else:
            self.log_skipped_modules("spectral_library")

    def assign_core_modules_parameters(self: Self, user_params: dict):
        """Assigns user-input on core modules to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if (
            info := user_params.get("core_modules").get("adduct_annotation")
        ) is not None:
            self.assign_adduct_annotation(info)
        else:
            self.log_default_values("adduct_annotation")

        if (
            info := user_params.get("core_modules")
            .get("spec_sim_networking")
            .get("modified_cosine")
        ) is not None:
            self.assign_spec_sim_networking_cosine(info)
        else:
            self.log_default_values("spec_sim_networking/modified_cosine")

        if (
            info := user_params.get("core_modules")
            .get("spec_sim_networking")
            .get("ms2deepscore")
        ) is not None:
            self.assign_spec_sim_networking_ms2deepscore(info)
        else:
            self.log_default_values("spec_sim_networking/ms2deepscore")

    def assign_additional_modules_parameters(self: Self, user_params: dict):
        """Assigns user-input on additional modules to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if (
            info := user_params.get("additional_modules").get("peaktable_filtering")
        ) is not None:
            self.assign_peaktable_filtering(info)
        else:
            self.log_default_values("peaktable_filtering")

        # TODO(MMZ 05.12.23): continue with core modules assignment

    # function assign_additional_modules_parameters()

    @staticmethod
    def log_skipped_modules(module: str):
        """Write log of skipped module assignment.

        Arguments:
            module: a str referencing the module that was skipped.
        """
        logging.info(f"ParameterManager: no parameters for module '{module}' - SKIP.")

    @staticmethod
    def log_default_values(module: str):
        """Write log for module for which defaults are used.

        Arguments:
            module: a str referencing the module for which default params are used.
        """
        logging.info(
            f"ParameterManager: no parameters for module '{module}' "
            f"- USED DEFAULT VALUES."
        )

    @staticmethod
    def log_malformed_parameters(module: str):
        """Write log for module for which missing/malformed parameters were found.

        Arguments:
            module: a str referencing the module for errors were detected.
        """
        logging.warning(
            f"ParameterManager: found missing/malformed parameter values for module "
            f"'{module}' - SKIP."
        )

    def assign_peaktable(self: Self, user_params: dict):
        """Assign peaktable file parameters to self.PeaktableParameters

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
            logging.warning(str(e))
            logging.critical(
                "ParameterManager: no or malformed parameters for "
                "'peaktable' - ABORT"
            )
            raise e

    def assign_msms(self: Self, user_params: dict):
        """Assign msms file parameters to self.MsmsParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.MsmsParameters = MsmsParameters(**user_params)
            logging.info("Validated and assigned user-specified parameter for 'msms'.")
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("msms")
            self.MsmsParameters = None

    def assign_phenotype(self: Self, user_params: dict):
        """Assign phenotype file parameters to self.PhenotypeParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenotypeParameters = PhenotypeParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for " "'phenotype'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("phenotype")
            self.PhenotypeParameters = None

    def assign_group_metadata(self: Self, user_params: dict):
        """Assign group metadata file parameters to self.GroupMetadataParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupMetadataParameters = GroupMetadataParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'group_metadata'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("group_metadata")
            self.GroupMetadataParameters = None

    def assign_spectral_library(self: Self, user_params: dict):
        """Assign spectral library file parameters to self.SpecLibParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpecLibParameters = SpecLibParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'spectral_library'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("spectral_library")
            self.SpecLibParameters = None

    def assign_adduct_annotation(self: Self, user_params: dict):
        """Assign adduct_annotation parameters to self.AdductAnnotationParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AdductAnnotationParameters = AdductAnnotationParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'adduct_annotation'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("adduct_annotation")
            self.AdductAnnotationParameters = AdductAnnotationParameters()

    def assign_spec_sim_networking_cosine(self: Self, user_params: dict):
        """Assign spec_sim_networking/modified_cosine parameters to self.SpecSimNetworkCosineParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpecSimNetworkCosineParameters = SpecSimNetworkCosineParameters(
                **user_params
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'spec_sim_networking/modified_cosine'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("spec_sim_networking/modified_cosine")
            self.SpecSimNetworkCosineParameters = SpecSimNetworkCosineParameters()

    def assign_spec_sim_networking_ms2deepscore(self: Self, user_params: dict):
        """Assign spec_sim_networking/ms2deepscore parameters to self.SpecSimNetworkDeepscoreParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpecSimNetworkDeepscoreParameters = SpecSimNetworkDeepscoreParameters(
                **user_params
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'spec_sim_networking/ms2deepscore'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("spec_sim_networking/ms2deepscore")
            self.SpecSimNetworkDeepscoreParameters = SpecSimNetworkDeepscoreParameters()

    def assign_peaktable_filtering(self: Self, user_params: dict):
        """Assign peaktable_filtering parameters to self.PeaktableFilteringParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PeaktableFilteringParameters = PeaktableFilteringParameters(
                **user_params
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'peaktable_filtering'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters("spec_sim_networking/ms2deepscore")
            self.SpecSimNetworkDeepscoreParameters = SpecSimNetworkDeepscoreParameters()

    # TODO(MMZ 05.12.23): continue here with functions; all below will be deleted later

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
