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
from pydantic import BaseModel
from typing import Self, Optional

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
    as well as default values, for downstream processing. More information on default
    parameters and the properties of the dicts can be found in
    fermo_core/config/default_parameters.json

    Attributes:
        PeaktableParameters: class handling peaktable parameters or None
        MsmsParameters: class handling MS/MS parameters or None
        PhenotypeParameters: class handling phenotype parameters or None
        GroupMetadataParameters: class handling metadata parameters or None
        SpecLibParameters: class handling spectra library parameters or None
        AdductAnnotationParameters: class handling adduct annotation module parameter
        SpecSimNetworkCosineParameters: class handling cosine-based spectral
            similarity networking module parameter
        SpecSimNetworkDeepscoreParameters: class handling ms2deepscore-based spectral
            similarity networking module parameter
        PeaktableFilteringParameters: class handling peaktable filter module parameter
        BlankAssignmentParameters: class handling blank-assignment module parameter
        PhenotypeAssignmentFoldParameters: class handling phenotype-assignment module
            parameter
        SpectralLibMatchingCosineParameters: class handling cosine-based spectral
            library matching module parameter
        SpectralLibMatchingDeepscoreParameters: class handling ms2deepscore-based
            spectral library matching module parameter
        Ms2QueryAnnotationParameters: class handling ms2query annotation module params
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

        Raises:
            ValueError: could not find "peaktable" parameters in user input.
        """
        if (info := user_params.get("files", {}).get("peaktable")) is not None:
            self.assign_peaktable(info)
        else:
            self.log_skipped_modules("peaktable")
            logging.critical(
                "ParameterManager: no or malformed parameters for 'peaktable' - ABORT"
            )
            raise ValueError(
                "ParameterManager: could not find 'peaktable' parameters in user input."
            )

        if (info := user_params.get("files", {}).get("msms")) is not None:
            self.assign_msms(info)
        else:
            self.log_skipped_modules("msms")

        if (info := user_params.get("files", {}).get("phenotype")) is not None:
            self.assign_phenotype(info)
        else:
            self.log_skipped_modules("phenotype")

        if (info := user_params.get("files", {}).get("group_metadata")) is not None:
            self.assign_group_metadata(info)
        else:
            self.log_skipped_modules("group_metadata")

        if (info := user_params.get("files", {}).get("spectral_library")) is not None:
            self.assign_spectral_library(info)
        else:
            self.log_skipped_modules("spectral_library")

    def assign_core_modules_parameters(self: Self, user_params: dict):
        """Assigns user-input on core modules to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if (
            info := user_params.get("core_modules", {}).get("adduct_annotation")
        ) is not None:
            self.assign_adduct_annotation(info)
        else:
            self.log_default_values("adduct_annotation")

        if (
            info := user_params.get("core_modules", {})
            .get("spec_sim_networking", {})
            .get("modified_cosine")
        ) is not None:
            self.assign_spec_sim_networking_cosine(info)
        else:
            self.log_default_values("spec_sim_networking/modified_cosine")

        if (
            info := user_params.get("core_modules", {})
            .get("spec_sim_networking", {})
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
            info := user_params.get("additional_modules", {}).get("peaktable_filtering")
        ) is not None:
            self.assign_peaktable_filtering(info)
        else:
            self.log_default_values("peaktable_filtering")

        if (
            info := user_params.get("additional_modules", {}).get("blank_assignment")
        ) is not None:
            self.assign_blank_assignment(info)
        else:
            self.log_default_values("blank_assignment")

        if (
            info := user_params.get("additional_modules", {})
            .get("phenotype_assignment", {})
            .get("fold_difference")
        ) is not None:
            self.assign_phenotype_assignment_fold(info)
        else:
            self.log_default_values("phenotype_assignment/fold_difference")

        if (
            info := user_params.get("additional_modules", {})
            .get("spectral_library_matching", {})
            .get("modified_cosine")
        ) is not None:
            self.assign_spec_lib_matching_cosine(info)
        else:
            self.log_default_values("spectral_library_matching/modified_cosine")

        if (
            info := user_params.get("additional_modules", {})
            .get("spectral_library_matching", {})
            .get("ms2deepscore")
        ) is not None:
            self.assign_spec_lib_matching_ms2deepscore(info)
        else:
            self.log_default_values("spectral_library_matching/ms2deepscore")

        if (
            info := user_params.get("additional_modules", {}).get("ms2query_annotation")
        ) is not None:
            self.assign_ms2query(info)
        else:
            self.log_default_values("ms2query_annotation")

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
    def log_malformed_parameters_skip(module: str):
        """Write log for module for which missing/malformed parameters were found.

        Arguments:
            module: a str referencing the module for errors were detected.
        """
        logging.warning(
            f"ParameterManager: missing/malformed parameter values for module "
            f"'{module}' - SKIP."
        )

    @staticmethod
    def log_malformed_parameters_default(module: str):
        """Write log for module for which missing/malformed parameters were found.

        Arguments:
            module: a str referencing the module for errors were detected.
        """
        logging.warning(
            f"ParameterManager: missing/malformed parameter values for module "
            f"'{module}' - USED DEFAULT VALUES."
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
            self.log_malformed_parameters_skip("msms")
            self.MsmsParameters = None

    def assign_phenotype(self: Self, user_params: dict):
        """Assign phenotype file parameters to self.PhenotypeParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenotypeParameters = PhenotypeParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for 'phenotype'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_skip("phenotype")
            self.PhenotypeParameters = None

    def assign_group_metadata(self: Self, user_params: dict):
        """Assign group metadata file parameters to self.GroupMetadataParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupMetadataParameters = GroupMetadataParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for 'group_metadata'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_skip("group_metadata")
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
            self.log_malformed_parameters_skip("spectral_library")
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
            self.log_malformed_parameters_default("adduct_annotation")
            self.AdductAnnotationParameters = AdductAnnotationParameters()

    def assign_spec_sim_networking_cosine(self: Self, user_params: dict):
        """Assign spec_sim_networking/modified_cosine parameters to
            self.SpecSimNetworkCosineParameters.

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
            self.log_malformed_parameters_default("spec_sim_networking/modified_cosine")
            self.SpecSimNetworkCosineParameters = SpecSimNetworkCosineParameters()

    def assign_spec_sim_networking_ms2deepscore(self: Self, user_params: dict):
        """Assign spec_sim_networking/ms2deepscore parameters to
            self.SpecSimNetworkDeepscoreParameters.

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
            self.log_malformed_parameters_default("spec_sim_networking/ms2deepscore")
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
            self.log_malformed_parameters_default("peaktable_filtering")
            self.PeaktableFilteringParameters = PeaktableFilteringParameters()

    def assign_blank_assignment(self: Self, user_params: dict):
        """Assign blank_assignment parameters to self.BlankAssignmentParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.BlankAssignmentParameters = BlankAssignmentParameters(**user_params)
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'blank_assignment'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_default("blank_assignment")
            self.BlankAssignmentParameters = BlankAssignmentParameters()

    def assign_phenotype_assignment_fold(self: Self, user_params: dict):
        """Assign phenotype_assignment/fold_difference parameters to
            self.PhenotypeAssignmentFoldParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenotypeAssignmentFoldParameters = PhenotypeAssignmentFoldParameters(
                **user_params
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'phenotype_assignment/fold_difference'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_default(
                "phenotype_assignment/fold_difference"
            )
            self.PhenotypeAssignmentFoldParameters = PhenotypeAssignmentFoldParameters()

    def assign_spec_lib_matching_cosine(self: Self, user_params: dict):
        """Assign spectral_library_matching/modified_cosine parameters to
            self.SpectralLibMatchingCosineParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpectralLibMatchingCosineParameters = (
                SpectralLibMatchingCosineParameters(**user_params)
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'spectral_library_matching/modified_cosine'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_default(
                "spectral_library_matching/modified_cosine"
            )
            self.SpectralLibMatchingCosineParameters = (
                SpectralLibMatchingCosineParameters()
            )

    def assign_spec_lib_matching_ms2deepscore(self: Self, user_params: dict):
        """Assign spectral_library_matching/ms2deepscore parameters to
            self.SpectralLibMatchingDeepscoreParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpectralLibMatchingDeepscoreParameters = (
                SpectralLibMatchingDeepscoreParameters(**user_params)
            )
            logging.info(
                "Validated and assigned user-specified parameter for "
                "'spectral_library_matching/ms2deepscore'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_default(
                "spectral_library_matching/ms2deepscore"
            )
            self.SpectralLibMatchingDeepscoreParameters = (
                SpectralLibMatchingDeepscoreParameters()
            )

    def assign_ms2query(self: Self, user_params: dict):
        """Assign ms2query parameters to self.Ms2QueryAnnotationParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.Ms2QueryAnnotationParameters = Ms2QueryAnnotationParameters(
                **user_params
            )
            logging.info(
                "Validated and assigned user-specified parameter for 'ms2query'."
            )
        except Exception as e:
            logging.warning(str(e))
            self.log_malformed_parameters_default("ms2query")
            self.Ms2QueryAnnotationParameters = Ms2QueryAnnotationParameters()
