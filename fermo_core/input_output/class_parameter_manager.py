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
from typing import Optional, Self

from pydantic import BaseModel

from fermo_core.input_output.additional_module_parameter_managers import (
    AsKcbCosineMatchingParams,
    AsKcbDeepscoreMatchingParams,
    BlankAssignmentParameters,
    FeatureFilteringParameters,
    GroupFactAssignmentParameters,
    Ms2QueryAnnotationParameters,
    PhenoQualAssgnParams,
    PhenoQuantConcAssgnParams,
    PhenoQuantPercentAssgnParams,
    SpectralLibMatchingCosineParameters,
    SpectralLibMatchingDeepscoreParameters,
)
from fermo_core.input_output.core_module_parameter_managers import (
    AdductAnnotationParameters,
    FragmentAnnParameters,
    NeutralLossParameters,
    SpecSimNetworkCosineParameters,
    SpecSimNetworkDeepscoreParameters,
)
from fermo_core.input_output.input_file_parameter_managers import (
    AsResultsParameters,
    GroupMetadataParameters,
    MS2QueryResultsParameters,
    MsmsParameters,
    PeaktableParameters,
    PhenotypeParameters,
    SpecLibParameters,
)
from fermo_core.input_output.output_file_parameter_managers import OutputParameters

logger = logging.getLogger("fermo_core")


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
        MS2QueryResultsParameters: class handling ms2query results or None
        AsResultsParameters: class handling antiSMASH results or None
        OutputParameters: class handling output file parameters
        AdductAnnotationParameters: class handling adduct annotation module parameter
        NeutralLossParameters: class handling neutral loss annotation module parameters
        FragmentAnnParameters: class handling fragment annotation module parameters
        SpecSimNetworkCosineParameters: class handling cosine-based spectral
            similarity networking module parameter
        SpecSimNetworkDeepscoreParameters: class handling ms2deepscore-based spectral
            similarity networking module parameter
        FeatureFilteringParameters: class handling feature filter module parameter
        BlankAssignmentParameters: class handling blank-assignment module parameter
        GroupFactAssignmentParameters: class handling group factor assignment mod params
        PhenoQualAssgnParams: class handling phenotype qual assignment parameter
        PhenoQuantPercentAssgnParams: phenotype quantitative percentage assignment param
        PhenoQuantConcAssgnParams: phenotype quantitative concentration assignment param
        SpectralLibMatchingCosineParameters: class handling cosine-based spectral
            library matching module parameter
        SpectralLibMatchingDeepscoreParameters: class handling ms2deepscore-based
            spectral library matching module parameter
        Ms2QueryAnnotationParameters: class handling ms2query annotation module params
        AsKcbCosineMatchingParams: class handling antiSMASH KCB cosine module params
        AsKcbDeepscoreMatchingParams: class handling antiSMASH KCB DS module params
    """

    PeaktableParameters: Optional[PeaktableParameters] = None
    MsmsParameters: Optional[MsmsParameters] = None
    PhenotypeParameters: Optional[PhenotypeParameters] = None
    GroupMetadataParameters: Optional[GroupMetadataParameters] = None
    SpecLibParameters: Optional[SpecLibParameters] = None
    MS2QueryResultsParameters: Optional[MS2QueryResultsParameters] = None
    AsResultsParameters: Optional[AsResultsParameters] = None
    OutputParameters: OutputParameters = OutputParameters()
    AdductAnnotationParameters: AdductAnnotationParameters = (
        AdductAnnotationParameters()
    )
    NeutralLossParameters: NeutralLossParameters = NeutralLossParameters()
    FragmentAnnParameters: FragmentAnnParameters = FragmentAnnParameters()
    SpecSimNetworkCosineParameters: SpecSimNetworkCosineParameters = (
        SpecSimNetworkCosineParameters()
    )
    SpecSimNetworkDeepscoreParameters: SpecSimNetworkDeepscoreParameters = (
        SpecSimNetworkDeepscoreParameters()
    )
    FeatureFilteringParameters: FeatureFilteringParameters = (
        FeatureFilteringParameters()
    )
    BlankAssignmentParameters: BlankAssignmentParameters = BlankAssignmentParameters()
    GroupFactAssignmentParameters: GroupFactAssignmentParameters = (
        GroupFactAssignmentParameters()
    )
    PhenoQualAssgnParams: PhenoQualAssgnParams = PhenoQualAssgnParams()
    PhenoQuantPercentAssgnParams: PhenoQuantPercentAssgnParams = (
        PhenoQuantPercentAssgnParams()
    )
    PhenoQuantConcAssgnParams: PhenoQuantConcAssgnParams = PhenoQuantConcAssgnParams()
    SpectralLibMatchingCosineParameters: SpectralLibMatchingCosineParameters = (
        SpectralLibMatchingCosineParameters()
    )
    SpectralLibMatchingDeepscoreParameters: SpectralLibMatchingDeepscoreParameters = (
        SpectralLibMatchingDeepscoreParameters()
    )
    Ms2QueryAnnotationParameters: Ms2QueryAnnotationParameters = (
        Ms2QueryAnnotationParameters()
    )
    AsKcbCosineMatchingParams: AsKcbCosineMatchingParams = AsKcbCosineMatchingParams()
    AsKcbDeepscoreMatchingParams: AsKcbDeepscoreMatchingParams = (
        AsKcbDeepscoreMatchingParams()
    )

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
            (self.AsResultsParameters, "AsResultsParameters"),
        )

        json_dict = {}
        for file in attributes:
            if file[0] is not None:
                json_dict[file[1]] = file[0].to_json()
            else:
                json_dict[file[1]] = {"filepath": "No file provided."}

        json_dict["OutputParameters"] = self.OutputParameters.to_json()
        json_dict["AdductAnnotationParameters"] = (
            self.AdductAnnotationParameters.to_json()
        )
        json_dict["NeutralLossParameters"] = self.NeutralLossParameters.to_json()
        json_dict["FragmentAnnParameters"] = self.FragmentAnnParameters.to_json()
        json_dict["SpecSimNetworkCosineParameters"] = (
            self.SpecSimNetworkCosineParameters.to_json()
        )
        json_dict["SpecSimNetworkDeepscoreParameters"] = (
            self.SpecSimNetworkDeepscoreParameters.to_json()
        )
        json_dict["FeatureFilteringParameters"] = (
            self.FeatureFilteringParameters.to_json()
        )
        json_dict["BlankAssignmentParameters"] = (
            self.BlankAssignmentParameters.to_json()
        )
        json_dict["GroupFactAssignmentParameters"] = (
            self.GroupFactAssignmentParameters.to_json()
        )
        json_dict["PhenoQualAssgnParams"] = self.PhenoQualAssgnParams.to_json()
        json_dict["PhenoQuantPercentAssgnParams"] = (
            self.PhenoQuantPercentAssgnParams.to_json()
        )
        json_dict["PhenoQuantConcAssgnParams"] = (
            self.PhenoQuantConcAssgnParams.to_json()
        )
        json_dict["SpectralLibMatchingCosineParameters"] = (
            self.SpectralLibMatchingCosineParameters.to_json()
        )
        json_dict["SpectralLibMatchingDeepscoreParameters"] = (
            self.SpectralLibMatchingDeepscoreParameters.to_json()
        )
        json_dict["Ms2QueryAnnotationParameters"] = (
            self.Ms2QueryAnnotationParameters.to_json()
        )
        json_dict["AsKcbCosineMatchingParams"] = (
            self.AsKcbCosineMatchingParams.to_json()
        )
        json_dict["AsKcbDeepscoreMatchingParams"] = (
            self.AsKcbDeepscoreMatchingParams.to_json()
        )

        return json_dict

    def assign_parameters_cli(self: Self, user_params: dict):
        """Modifies attributes by calling methods that take user input from CLI.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        logger.info(
            "'ParameterManager': started assignment of user-provided parameters."
        )

        self.assign_files_parameters(user_params)
        self.assign_core_modules_parameters(user_params)
        self.assign_additional_modules_parameters(user_params)

        logger.info(
            "'ParameterManager': completed assignment of user-provided parameters."
        )

    def assign_files_parameters(self: Self, user_params: dict):
        """Assigns user-input on files to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.

        Raises:
            KeyError: could not find "peaktable" parameters in user input.
        """
        if user_params.get("files") is not None:
            user_params = user_params.get("files")
        else:
            logger.critical("ParameterManager: found no parameters for 'files' - ABORT")
            raise KeyError("ParameterManager: found no parameters for 'files' - ABORT")

        modules = (
            (user_params.get("peaktable"), self.assign_peaktable, "peaktable"),
            (user_params.get("msms"), self.assign_msms, "msms"),
            (user_params.get("phenotype"), self.assign_phenotype, "phenotype"),
            (
                user_params.get("group_metadata"),
                self.assign_group_metadata,
                "group_metadata",
            ),
            (
                user_params.get("spectral_library"),
                self.assign_spectral_library,
                "spectral_library",
            ),
            (
                user_params.get("ms2query_results"),
                self.assign_ms2query_results,
                "ms2query_results",
            ),
            (user_params.get("as_results"), self.assign_as_results, "as_results"),
        )

        for module in modules:
            if (data := module[0]) is not None:
                module[1](data)
            else:
                self.log_skipped_modules(module[2])

        self.OutputParameters.validate_output_dir(
            peaktable_dir=self.PeaktableParameters.filepath.parent
        )

    def assign_core_modules_parameters(self: Self, user_params: dict):
        """Assigns user-input on core modules to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if user_params.get("core_modules") is not None:
            user_params = user_params.get("core_modules")
        else:
            self.log_default_values("core_modules")
            return

        modules = (
            (
                user_params.get("adduct_annotation"),
                self.assign_adduct_annotation,
                "adduct_annotation",
            ),
            (
                user_params.get("neutral_loss_annotation"),
                self.assign_neutral_loss_annotation,
                "neutral_loss_annotation",
            ),
            (
                user_params.get("fragment_annotation"),
                self.assign_fragment_annotation,
                "fragment_annotation",
            ),
            (
                user_params.get("spec_sim_networking", {}).get("modified_cosine"),
                self.assign_spec_sim_networking_cosine,
                "spec_sim_networking/modified_cosine",
            ),
            (
                user_params.get("spec_sim_networking", {}).get("ms2deepscore"),
                self.assign_spec_sim_networking_ms2deepscore,
                "spec_sim_networking/ms2deepscore",
            ),
        )

        for module in modules:
            if (data := module[0]) is not None:
                module[1](data)
            else:
                self.log_default_values(module[2])

    def assign_additional_modules_parameters(self: Self, user_params: dict):
        """Assigns user-input on additional modules to ParameterManager.

        Arguments:
            user_params: a json-derived dict with user input; jsonschema-controlled.
        """
        if user_params.get("additional_modules") is not None:
            user_params = user_params.get("additional_modules")
        else:
            self.log_default_values("additional_modules")
            return

        modules = (
            (
                user_params.get("feature_filtering"),
                self.assign_feature_filtering,
                "feature_filtering",
            ),
            (
                user_params.get("blank_assignment"),
                self.assign_blank_assignment,
                "blank_assignment",
            ),
            (
                user_params.get("group_factor_assignment"),
                self.assign_group_factor_assignment,
                "group_factor_assignment",
            ),
            (
                user_params.get("phenotype_assignment", {}).get("qualitative"),
                self.assign_phenotype_qualitative,
                "phenotype_assignment/qualitative",
            ),
            (
                user_params.get("phenotype_assignment", {}).get(
                    "quantitative-percentage"
                ),
                self.assign_phenotype_quant_percent,
                "phenotype_assignment/quantitative-percentage",
            ),
            (
                user_params.get("phenotype_assignment", {}).get(
                    "quantitative-concentration"
                ),
                self.assign_phenotype_quant_concentration,
                "phenotype_assignment/quantitative-concentration",
            ),
            (
                user_params.get("spectral_library_matching", {}).get("modified_cosine"),
                self.assign_spec_lib_matching_cosine,
                "spectral_library_matching/modified_cosine",
            ),
            (
                user_params.get("spectral_library_matching", {}).get("ms2deepscore"),
                self.assign_spec_lib_matching_ms2deepscore,
                "spectral_library_matching/ms2deepscore",
            ),
            (
                user_params.get("ms2query_annotation"),
                self.assign_ms2query,
                "ms2query_annotation",
            ),
            (
                user_params.get("as_kcb_matching", {}).get("modified_cosine"),
                self.assign_as_kcb_matching_cosine,
                "as_kcb_matching/modified_cosine",
            ),
            (
                user_params.get("as_kcb_matching", {}).get("ms2deepscore"),
                self.assign_as_kcb_matching_deepscore,
                "as_kcb_matching/ms2deepscore",
            ),
        )

        for module in modules:
            if (data := module[0]) is not None:
                module[1](data)
            else:
                self.log_default_values(module[2])

    @staticmethod
    def log_skipped_modules(module: str):
        """Write log of skipped module assignment.

        Arguments:
            module: a str referencing the module that was skipped.
        """
        logger.info(f"'ParameterManager': no parameters for module '{module}' - SKIP.")

    @staticmethod
    def log_default_values(module: str):
        """Write log for module for which defaults are used.

        Arguments:
            module: a str referencing the module for which default params are used.
        """
        logger.info(
            f"'ParameterManager': no parameters for module '{module}' "
            f"- USED DEFAULT VALUES."
        )

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

    @staticmethod
    def log_malformed_parameters_default(module: str):
        """Write log for module for which missing/malformed parameters were found.

        Arguments:
            module: a str referencing the module for errors were detected.
        """
        logger.warning(
            f"'ParameterManager': missing/malformed parameter values for module "
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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'peaktable'."
            )
        except Exception as e:
            logger.warning(str(e))
            logger.critical(
                "'ParameterManager': no or malformed parameters for "
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
            logger.info(
                "'ParameterManager': validated and assigned parameters for 'msms'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("msms")
            self.MsmsParameters = None

    def assign_phenotype(self: Self, user_params: dict):
        """Assign phenotype file parameters to self.PhenotypeParameters

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenotypeParameters = PhenotypeParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'phenotype'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("phenotype")
            self.PhenotypeParameters = None

    def assign_group_metadata(self: Self, user_params: dict):
        """Assign group metadata file parameters to self.GroupMetadataParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupMetadataParameters = GroupMetadataParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'group_metadata'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("group_metadata")
            self.GroupMetadataParameters = None

    def assign_spectral_library(self: Self, user_params: dict):
        """Assign spectral library file parameters to self.SpecLibParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.SpecLibParameters = SpecLibParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'spectral_library'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("spectral_library")
            self.SpecLibParameters = None

    def assign_ms2query_results(self: Self, user_params: dict):
        """Assign ms2query_results parameters to self.MS2QueryResultsParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.MS2QueryResultsParameters = MS2QueryResultsParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'ms2query_results'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("ms2query_results")
            self.MS2QueryResultsParameters = None

    def assign_as_results(self: Self, user_params: dict):
        """Assign antiSMASH results parameters to self.AsResultsParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AsResultsParameters = AsResultsParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'as_results'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_skip("as_results")
            self.AsResultsParameters = None

    def assign_adduct_annotation(self: Self, user_params: dict):
        """Assign adduct_annotation parameters to self.AdductAnnotationParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AdductAnnotationParameters = AdductAnnotationParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'adduct_annotation'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("adduct_annotation")
            self.AdductAnnotationParameters = AdductAnnotationParameters()

    def assign_fragment_annotation(self: Self, user_params: dict):
        """Assign fragment_annotation parameters to self.FragmentAnnParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.FragmentAnnParameters = FragmentAnnParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'fragment_annotation'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("adduct_annotation")
            self.FragmentAnnParameters = FragmentAnnParameters()

    def assign_neutral_loss_annotation(self: Self, user_params: dict):
        """Assign neutral_loss_annotation parameters to self.NeutralLossParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.NeutralLossParameters = NeutralLossParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'neutral_loss_annotation'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("neutral_loss_annotation")
            self.NeutralLossParameters = NeutralLossParameters()

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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'spec_sim_networking/modified_cosine'."
            )
        except Exception as e:
            logger.warning(str(e))
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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'spec_sim_networking/ms2deepscore'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("spec_sim_networking/ms2deepscore")
            self.SpecSimNetworkDeepscoreParameters = SpecSimNetworkDeepscoreParameters()

    def assign_feature_filtering(self: Self, user_params: dict):
        """Assign feature_filtering parameters to self.FeatureFilteringParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.FeatureFilteringParameters = FeatureFilteringParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'feature_filtering'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("feature_filtering")
            self.FeatureFilteringParameters = FeatureFilteringParameters()

    def assign_blank_assignment(self: Self, user_params: dict):
        """Assign blank_assignment parameters to self.BlankAssignmentParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.BlankAssignmentParameters = BlankAssignmentParameters(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'blank_assignment'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("blank_assignment")
            self.BlankAssignmentParameters = BlankAssignmentParameters()

    def assign_group_factor_assignment(self: Self, user_params: dict):
        """Assign parameters to self.GroupFactAssignmentParameters.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.GroupFactAssignmentParameters = GroupFactAssignmentParameters(
                **user_params
            )
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'group_factor_assignment'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("group_factor_assignment")
            self.GroupFactAssignmentParameters = GroupFactAssignmentParameters()

    def assign_phenotype_qualitative(self: Self, user_params: dict):
        """Assign phenotype_assignment/qualitative parameters to
            self.PhenoQualAssgnParams.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenoQualAssgnParams = PhenoQualAssgnParams(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'phenotype_assignment/qualitative'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("phenotype_assignment/qualitative")
            self.PhenoQualAssgnParams = PhenoQualAssgnParams()

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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'phenotype_assignment/quantitative-percentage'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default(
                "phenotype_assignment/quantitative-percentage"
            )
            self.PhenoQuantPercentAssgnParams = PhenoQuantPercentAssgnParams()

    def assign_phenotype_quant_concentration(self: Self, user_params: dict):
        """Assign phenotype_assignment/quantitative-concentration parameters to
            self.PhenoQuantConcAssgnParams.

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.PhenoQuantConcAssgnParams = PhenoQuantConcAssgnParams(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'phenotype_assignment/quantitative-concentration'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default(
                "phenotype_assignment/quantitative-concentration"
            )
            self.PhenoQuantConcAssgnParams = PhenoQuantConcAssgnParams()

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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'spectral_library_matching/modified_cosine'."
            )
        except Exception as e:
            logger.warning(str(e))
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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'spectral_library_matching/ms2deepscore'."
            )
        except Exception as e:
            logger.warning(str(e))
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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'ms2query'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("ms2query")
            self.Ms2QueryAnnotationParameters = Ms2QueryAnnotationParameters()

    def assign_as_kcb_matching_cosine(self: Self, user_params: dict):
        """Assign antismash kcb results parameters to self.AsKcbCosineMatchingParams.

        Uses modified cosine algorithm

        Parameters:
            user_params: user-provided params, read from json file
        """
        try:
            self.AsKcbCosineMatchingParams = AsKcbCosineMatchingParams(**user_params)
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'as_kcb_matching/modified_cosine'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("as_kcb_matching/modified_cosine")
            self.AsKcbCosineMatchingParams = AsKcbCosineMatchingParams()

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
            logger.info(
                "'ParameterManager': validated and assigned parameters "
                "for 'as_kcb_matching/ms2deepscore'."
            )
        except Exception as e:
            logger.warning(str(e))
            self.log_malformed_parameters_default("as_kcb_matching/ms2deepscore")
            self.AsKcbDeepscoreMatchingParams = AsKcbDeepscoreMatchingParams()
