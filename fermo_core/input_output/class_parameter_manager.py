"""Hold parameters for downstream data processing and analysis.

Interface to collect and hold user input from both command line and GUI.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

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
from typing import Any, Optional, Self

from pydantic import BaseModel

from fermo_core.input_output.param_handlers import (
    AdductAnnotationParameters,
    AsKcbCosineMatchingParams,
    AsKcbDeepscoreMatchingParams,
    AsResultsParameters,
    BlankAssignmentParameters,
    FeatureFilteringParameters,
    FragmentAnnParameters,
    GroupFactAssignmentParameters,
    GroupMetadataParameters,
    MS2QueryResultsParameters,
    MsmsParameters,
    NeutralLossParameters,
    OutputParameters,
    PeaktableParameters,
    PhenoQualAssgnParams,
    PhenoQuantConcAssgnParams,
    PhenoQuantPercentAssgnParams,
    PhenotypeParameters,
    SpecLibParameters,
    SpecSimNetworkCosineParameters,
    SpecSimNetworkDeepscoreParameters,
    SpectralLibMatchingCosineParameters,
    SpectralLibMatchingDeepscoreParameters,
)

logger = logging.getLogger("fermo_core")


class ParameterManager(BaseModel):
    """Handle parameters for processing by fermo_core."""

    PeaktableParameters: Any | None = None
    MsmsParameters: Any | None = None
    PhenotypeParameters: Any | None = None
    GroupMetadataParameters: Any | None = None
    SpecLibParameters: Any | None = None
    MS2QueryResultsParameters: Any | None = None
    AsResultsParameters: Any | None = None
    OutputParameters: Any | None = None
    AdductAnnotationParameters: Any | None = None
    NeutralLossParameters: Any | None = None
    FragmentAnnParameters: Any | None = None
    SpecSimNetworkCosineParameters: Any | None = None
    SpecSimNetworkDeepscoreParameters: Any | None = None
    FeatureFilteringParameters: Any | None = None
    BlankAssignmentParameters: Any | None = None
    GroupFactAssignmentParameters: Any | None = None
    PhenoQualAssgnParams: Any | None = None
    PhenoQuantPercentAssgnParams: Any | None = None
    PhenoQuantConcAssgnParams: Any | None = None
    SpectralLibMatchingCosineParameters: Any | None = None
    SpectralLibMatchingDeepscoreParameters: Any | None = None
    AsKcbCosineMatchingParams: Any | None = None
    AsKcbDeepscoreMatchingParams: Any | None = None

    def to_json(self: Self) -> dict:
        """Export class attributes to json-dump compatible dict.

        Returns:
            A dictionary with class attributes as keys
        """
        attributes = (
            (self.PeaktableParameters, "PeaktableParameters"),
            (self.MsmsParameters, "MsmsParameters"),
            (self.PhenotypeParameters, "PhenotypeParameters"),
            (self.GroupMetadataParameters, "GroupMetadataParameters"),
            (self.SpecLibParameters, "SpecLibParameters"),
            (self.MS2QueryResultsParameters, "MS2QueryResultsParameters"),
            (self.OutputParameters, "OutputParameters"),
            (self.AdductAnnotationParameters, "AdductAnnotationParameters"),
            (self.NeutralLossParameters, "NeutralLossParameters"),
            (self.FragmentAnnParameters, "FragmentAnnParameters"),
            (self.SpecSimNetworkCosineParameters, "SpecSimNetworkCosineParameters"),
            (
                self.SpecSimNetworkDeepscoreParameters,
                "SpecSimNetworkDeepscoreParameters",
            ),
            (self.FeatureFilteringParameters, "FeatureFilteringParameters"),
            (self.BlankAssignmentParameters, "BlankAssignmentParameters"),
            (self.GroupFactAssignmentParameters, "GroupFactAssignmentParameters"),
            (self.PhenoQualAssgnParams, "PhenoQualAssgnParameters"),
            (self.PhenoQuantPercentAssgnParams, "PhenoQuantPercentAssgnParameters"),
            (self.PhenoQuantConcAssgnParams, "PhenoQuantConcAssgnParameters"),
            (
                self.SpectralLibMatchingCosineParameters,
                "SpectralLibMatchingCosineParameters",
            ),
            (
                self.SpectralLibMatchingDeepscoreParameters,
                "SpectralLibMatchingDeepscoreParameters",
            ),
            (self.AsKcbCosineMatchingParams, "AsKcbCosineMatchingParameters"),
            (self.AsKcbDeepscoreMatchingParams, "AsKcbDeepscoreMatchingParameters"),
        )

        json_dict = {}
        for file in attributes:
            if file[0] is not None:
                json_dict[file[1]] = file[0].to_json()
            else:
                json_dict[file[1]] = {"activate_module": False}

        return json_dict

    @staticmethod
    def log_skipped_modules(module: str):
        """Write log of skipped module assignment.

        Arguments:
            module: a str referencing the module that was skipped.
        """
        logger.info(f"'ParameterManager': no parameters for module '{module}' - SKIP.")

    @staticmethod
    def log_passed_modules(module: str):
        """Write log of passed module assignment.

        Arguments:
            module: a str referencing the module that was skipped.
        """
        logger.info(f"'{module}': params validated and assigned.")

    @staticmethod
    def log_malformed_parameters_skip(module: str):
        """Write log for module for which missing/malformed parameters were found.

        Arguments:
            module: a str referencing the module for errors were detected.
        """
        logger.warning(
            f"'ParameterManager': missing/malformed parameter values for module "
            f"'{module}' - SKIP."
        )

    def assign_parameters_cli(self: Self, user_params: dict):
        """Modifies attributes by calling methods that take user input from CLI.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        logger.info(
            "'ParameterManager': started assignment of user-provided parameters."
        )
        self.assign_params(user_params)
        logger.info(
            "'ParameterManager': completed assignment of user-provided parameters."
        )

    def assign_params(self, user_params: dict) -> None:
        """Assigns user-input on files to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.

        Raises:
            KeyError: could not find "peaktable" parameters in user input.
        """
        try:
            user_params["PeaktableParameters"]
        except KeyError as e:
            logger.fatal("ParameterManager: did not find 'PeaktableParameters' - ABORT")
            raise e

        modules = (
            (
                user_params.get("PeaktableParameters"),
                self.assign_peaktable,
                "PeaktableParams",
            ),
            (user_params.get("MsmsParameters"), self.assign_msms, "MsmsParameters"),
            (
                user_params.get("PhenotypeParameters"),
                self.assign_phenotype,
                "PhenotypeParameters",
            ),
            (
                user_params.get("GroupMetadataParameters"),
                self.assign_group_metadata,
                "GroupMetadataParameters",
            ),
            (
                user_params.get("SpecLibParameters"),
                self.assign_spectral_library,
                "SpecLibParameters",
            ),
            (
                user_params.get("MS2QueryResultsParameters"),
                self.assign_ms2query_results,
                "MS2QueryResultsParameters",
            ),
            (
                user_params.get("AsResultsParameters"),
                self.assign_as_results,
                "AsResultsParameters",
            ),
            (
                user_params.get("AdductAnnotationParameters"),
                self.assign_adduct_annotation,
                "AdductAnnotationParameters",
            ),
            (
                user_params.get("NeutralLossParameters"),
                self.assign_neutral_loss_annotation,
                "NeutralLossParameters",
            ),
            (
                user_params.get("FragmentAnnParameters"),
                self.assign_fragment_annotation,
                "FragmentAnnParameters",
            ),
            (
                user_params.get("SpecSimNetworkCosineParameters"),
                self.assign_spec_sim_networking_cosine,
                "SpecSimNetworkCosineParameters",
            ),
            (
                user_params.get("SpecSimNetworkDeepscoreParameters"),
                self.assign_spec_sim_networking_ms2deepscore,
                "SpecSimNetworkDeepscoreParameters",
            ),
            (
                user_params.get("FeatureFilteringParameters"),
                self.assign_feature_filtering,
                "FeatureFilteringParameters",
            ),
            (
                user_params.get("BlankAssignmentParameters"),
                self.assign_blank_assignment,
                "BlankAssignmentParameters",
            ),
            (
                user_params.get("GroupFactAssignmentParameters"),
                self.assign_group_factor_assignment,
                "GroupFactAssignmentParameters",
            ),
            (
                user_params.get("PhenoQualAssgnParameters"),
                self.assign_phenotype_qualitative,
                "PhenoQualAssgnParameters",
            ),
            (
                user_params.get("PhenoQuantPercentAssgnParameters"),
                self.assign_phenotype_quant_percent,
                "PhenoQuantPercentAssgnParameters",
            ),
            (
                user_params.get("PhenoQuantConcAssgnParameters"),
                self.assign_phenotype_quant_concentration,
                "PhenoQuantConcAssgnParameters",
            ),
            (
                user_params.get("SpectralLibMatchingCosineParameters"),
                self.assign_spec_lib_matching_cosine,
                "SpectralLibMatchingCosineParameters",
            ),
            (
                user_params.get("SpectralLibMatchingDeepscoreParameters"),
                self.assign_spec_lib_matching_ms2deepscore,
                "SpectralLibMatchingDeepscoreParameters",
            ),
            (
                user_params.get("AsKcbCosineMatchingParameters"),
                self.assign_as_kcb_matching_cosine,
                "AsKcbCosineMatchingParameters",
            ),
            (
                user_params.get("AsKcbDeepscoreMatchingParameters"),
                self.assign_as_kcb_matching_deepscore,
                "AsKcbDeepscoreMatchingParameters",
            ),
        )

        for module in modules:
            if (data := module[0]) is not None:
                module[1](data)
            else:
                self.log_skipped_modules(module[2])

        self.OutputParameters = OutputParameters(
            directory_path=Path(
                user_params.get("PeaktableParameters").get("filepath")
            ).parent
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
            self.log_passed_modules("PeaktableParameters")
        except Exception as e:
            logger.fatal(str(e))
            logger.fatal("'PeaktableParameters': param assignment failed - ABORT")
            raise e

    def assign_msms(self: Self, user_params: dict):
        """Assign msms file parameters to self.MsmsParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.MsmsParameters = MsmsParameters(**user_params)
            self.log_passed_modules("MsmsParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("MsmsParameters")
            self.MsmsParameters = None

    def assign_phenotype(self: Self, user_params: dict):
        """Assign phenotype file parameters to self.PhenotypeParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenotypeParameters = PhenotypeParameters(**user_params)
            self.log_passed_modules("PhenotypeParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("PhenotypeParameters")
            self.PhenotypeParameters = None

    def assign_group_metadata(self: Self, user_params: dict):
        """Assign group metadata file parameters to self.GroupMetadataParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupMetadataParameters = GroupMetadataParameters(**user_params)
            self.log_passed_modules("GroupMetadataParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("GroupMetadataParameters")
            self.GroupMetadataParameters = None

    def assign_spectral_library(self: Self, user_params: dict):
        """Assign spectral library file parameters to self.SpecLibParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpecLibParameters = SpecLibParameters(**user_params)
            self.log_passed_modules("SpecLibParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("SpecLibParameters")
            self.SpecLibParameters = None

    def assign_ms2query_results(self: Self, user_params: dict):
        """Assign ms2query_results parameters to self.MS2QueryResultsParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.MS2QueryResultsParameters = MS2QueryResultsParameters(**user_params)
            self.log_passed_modules("MS2QueryResultsParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("MS2QueryResultsParameters")
            self.MS2QueryResultsParameters = None

    def assign_as_results(self: Self, user_params: dict):
        """Assign antiSMASH results parameters to self.AsResultsParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AsResultsParameters = AsResultsParameters(**user_params)
            self.log_passed_modules("AsResultsParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("AsResultsParameters")
            self.AsResultsParameters = None

    def assign_adduct_annotation(self: Self, user_params: dict):
        """Assign adduct_annotation parameters to self.AdductAnnotationParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AdductAnnotationParameters = AdductAnnotationParameters(**user_params)
            self.log_passed_modules("AdductAnnotationParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("AdductAnnotationParameters")
            self.AdductAnnotationParameters = None

    def assign_fragment_annotation(self: Self, user_params: dict):
        """Assign fragment_annotation parameters to self.FragmentAnnParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.FragmentAnnParameters = FragmentAnnParameters(**user_params)
            self.log_passed_modules("FragmentAnnParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("FragmentAnnParameters")
            self.FragmentAnnParameters = None

    def assign_neutral_loss_annotation(self: Self, user_params: dict):
        """Assign neutral_loss_annotation parameters to self.NeutralLossParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.NeutralLossParameters = NeutralLossParameters(**user_params)
            self.log_passed_modules("NeutralLossParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("NeutralLossParameters")
            self.NeutralLossParameters = None

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
            self.log_passed_modules("SpecSimNetworkCosineParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("SpecSimNetworkCosineParameters")
            self.SpecSimNetworkCosineParameters = None

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
            self.log_passed_modules("SpecSimNetworkDeepscoreParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("SpecSimNetworkDeepscoreParameters")
            self.SpecSimNetworkDeepscoreParameters = None

    def assign_feature_filtering(self: Self, user_params: dict):
        """Assign feature_filtering parameters to self.FeatureFilteringParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.FeatureFilteringParameters = FeatureFilteringParameters(**user_params)
            self.log_passed_modules("FeatureFilteringParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("FeatureFilteringParameters")
            self.FeatureFilteringParameters = None

    def assign_blank_assignment(self: Self, user_params: dict):
        """Assign blank_assignment parameters to self.BlankAssignmentParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.BlankAssignmentParameters = BlankAssignmentParameters(**user_params)
            self.log_passed_modules("BlankAssignmentParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("BlankAssignmentParameters")
            self.BlankAssignmentParameters = None

    def assign_group_factor_assignment(self: Self, user_params: dict):
        """Assign parameters to self.GroupFactAssignmentParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupFactAssignmentParameters = GroupFactAssignmentParameters(
                **user_params
            )
            self.log_passed_modules("GroupFactAssignmentParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("GroupFactAssignmentParameters")
            self.GroupFactAssignmentParameters = None

    def assign_phenotype_qualitative(self: Self, user_params: dict):
        """Assign phenotype_assignment/qualitative parameters to
            self.PhenoQualAssgnParams.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenoQualAssgnParams = PhenoQualAssgnParams(**user_params)
            self.log_passed_modules("PhenoQualAssgnParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("PhenoQualAssgnParameters")
            self.PhenoQualAssgnParams = None

    def assign_phenotype_quant_percent(self: Self, user_params: dict):
        """Assign phenotype_assignment/quantitative-percentage parameters to
            self.PhenoQuantPercentAssgnParams.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenoQuantPercentAssgnParams = PhenoQuantPercentAssgnParams(
                **user_params
            )
            self.log_passed_modules("PhenoQuantPercentAssgnParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("PhenoQuantPercentAssgnParameters")
            self.PhenoQuantPercentAssgnParams = None

    def assign_phenotype_quant_concentration(self: Self, user_params: dict):
        """Assign phenotype_assignment/quantitative-concentration parameters to
            self.PhenoQuantConcAssgnParams.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenoQuantConcAssgnParams = PhenoQuantConcAssgnParams(**user_params)
            self.log_passed_modules("PhenoQuantConcAssgnParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("PhenoQuantConcAssgnParameters")
            self.PhenoQuantConcAssgnParams = None

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
            self.log_passed_modules("SpectralLibMatchingCosineParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("SpectralLibMatchingCosineParameters")
            self.SpectralLibMatchingCosineParameters = None

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
            self.log_passed_modules("SpectralLibMatchingDeepscoreParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("SpectralLibMatchingDeepscoreParameters")
            self.SpectralLibMatchingDeepscoreParameters = None

    def assign_as_kcb_matching_cosine(self: Self, user_params: dict):
        """Assign antismash kcb results parameters to self.AsKcbCosineMatchingParams.

        Uses modified cosine algorithm

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AsKcbCosineMatchingParams = AsKcbCosineMatchingParams(**user_params)
            self.log_passed_modules("AsKcbCosineMatchingParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("AsKcbCosineMatchingParameters")
            self.AsKcbCosineMatchingParams = None

    def assign_as_kcb_matching_deepscore(self: Self, user_params: dict):
        """Assign antismash kcb results parameters to self.AsKcbDeepscoreMatchingParams.

        Uses MS2DeepScore algorithm

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AsKcbDeepscoreMatchingParams = AsKcbDeepscoreMatchingParams(
                **user_params
            )
            self.log_passed_modules("AsKcbDeepscoreMatchingParameters")
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("AsKcbDeepscoreMatchingParameters")
            self.AsKcbDeepscoreMatchingParams = None
