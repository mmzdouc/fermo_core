from pathlib import Path

import pytest
from pydantic import ValidationError

from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
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


def test_init_parameter_manager_valid():
    assert isinstance(ParameterManager(), ParameterManager)


def test_parameter_manager_properties_valid():
    params = ParameterManager()
    assert params.PeaktableParameters is None


def test_assign_peaktable_valid():
    params = ParameterManager()
    params.assign_peaktable(
        {
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    assert isinstance(params.PeaktableParameters, PeaktableParameters)


def test_assign_peaktable_invalid():
    params = ParameterManager()
    with pytest.raises(ValidationError):
        params.assign_peaktable(
            {
                "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            }
        )


def test_assign_msms_valid():
    params = ParameterManager()
    params.assign_msms(
        {
            "filepath": "tests/test_data/test.msms.mgf",
            "format": "mgf",
            "rel_int_from": 0.05,
        }
    )
    assert isinstance(params.MsmsParameters, MsmsParameters)


def test_assign_msms_invalid():
    params = ParameterManager()
    params.assign_msms(
        {
            "filepath": "tests/test_data/test.msms.mgf",
        }
    )
    assert params.MsmsParameters is None


def test_assign_phenotype_valid():
    params = ParameterManager()
    params.assign_phenotype(
        {
            "filepath": "tests/test_data/test.bioactivity.qualitative.csv",
            "format": "qualitative",
        }
    )
    assert isinstance(params.PhenotypeParameters, PhenotypeParameters)


def test_assign_phenotype_invalid():
    params = ParameterManager()
    params.assign_phenotype(
        {
            "filepath": "tests/test_data/test.bioactivity.qualitative.csv",
        }
    )
    assert params.PhenotypeParameters is None


def test_assign_group_metadata_valid():
    params = ParameterManager()
    params.assign_group_metadata(
        {"filepath": "tests/test_data/test.group_metadata.csv", "format": "fermo"}
    )
    assert isinstance(params.GroupMetadataParameters, GroupMetadataParameters)


def test_assign_group_metadata_invalid():
    params = ParameterManager()
    params.assign_group_metadata(
        {
            "filepath": "tests/test_data/test.group_metadata.csv",
        }
    )
    assert params.GroupMetadataParameters is None


def test_assign_spectral_library_valid():
    params = ParameterManager()
    params.assign_spectral_library(
        {"dirpath": "tests/test_data/spec_lib/", "format": "mgf"}
    )
    assert isinstance(params.SpecLibParameters, SpecLibParameters)


def test_assign_spectral_library_invalid():
    params = ParameterManager()
    params.assign_spectral_library(
        {
            "dirpath": "tests/test_data/spec_lib/",
        }
    )
    assert params.SpecLibParameters is None


def test_assign_ms2query_results_valid():
    params = ParameterManager()
    params.assign_ms2query_results(
        {
            "filepath": "tests/test_data/test.ms2query_results.csv",
            "score_cutoff": 0.7,
        }
    )
    assert isinstance(params.MS2QueryResultsParameters, MS2QueryResultsParameters)


def test_assign_ms2query_results_invalid():
    params = ParameterManager()
    params.assign_ms2query_results(
        {"filepath": "tests/test_data/test.ms2query_results.csv"}
    )
    assert params.MS2QueryResultsParameters is None


def test_assign_as_results_valid():
    params = ParameterManager()
    params.assign_as_results(
        {
            "directory_path": "tests/test_data/JABTEZ000000000.1/",
            "similarity_cutoff": "0.7",
        }
    )
    assert isinstance(params.AsResultsParameters, AsResultsParameters)


def test_assign_as_results_invalid():
    params = ParameterManager()
    params.assign_as_results(
        {"directory_path": "example_data/case_study_peak_table_quant_full.csv"}
    )
    assert params.AsResultsParameters is None


def test_assign_adduct_annotation_valid():
    params = ParameterManager()
    params.assign_adduct_annotation({"activate_module": True, "mass_dev_ppm": 20.0})
    assert isinstance(params.AdductAnnotationParameters, AdductAnnotationParameters)


def test_assign_adduct_annotation_invalid():
    params = ParameterManager()
    params.assign_adduct_annotation({"activate_module": True})
    assert params.AdductAnnotationParameters is None


def test_assign_neutral_loss_valid():
    params = ParameterManager()
    params.assign_neutral_loss_annotation(
        {"activate_module": True, "mass_dev_ppm": 20.0}
    )
    assert isinstance(params.NeutralLossParameters, NeutralLossParameters)


def test_assign_neutral_loss_invalid():
    params = ParameterManager()
    params.assign_neutral_loss_annotation({"activate_module": True})
    assert params.NeutralLossParameters is None


def test_assign_fragment_annotation_valid():
    params = ParameterManager()
    params.assign_fragment_annotation({"activate_module": True, "mass_dev_ppm": 20.0})
    assert isinstance(params.FragmentAnnParameters, FragmentAnnParameters)


def test_assign_fragment_annotation_invalid():
    params = ParameterManager()
    params.assign_fragment_annotation({})
    assert params.FragmentAnnParameters is None


def test_assign_spec_sim_networking_cosine_valid():
    params = ParameterManager()
    params.assign_spec_sim_networking_cosine(
        {
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
            "max_precursor_mass_diff": 400,
        }
    )
    assert isinstance(
        params.SpecSimNetworkCosineParameters, SpecSimNetworkCosineParameters
    )


def test_assign_spec_sim_networking_cosine_invalid():
    params = ParameterManager()
    params.assign_spec_sim_networking_cosine({"asdfg": "asdfg"})
    assert params.SpecSimNetworkCosineParameters is None


def test_assign_spec_sim_networking_ms2deepscore_valid():
    params = ParameterManager()
    params.assign_spec_sim_networking_ms2deepscore(
        {
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
        }
    )
    assert isinstance(
        params.SpecSimNetworkDeepscoreParameters, SpecSimNetworkDeepscoreParameters
    )


def test_assign_spec_sim_networking_ms2deepscore_invalid():
    params = ParameterManager()
    params.assign_spec_sim_networking_ms2deepscore({"asdfg": "asdfg"})
    assert params.SpecSimNetworkDeepscoreParameters is None


def test_assign_feature_filtering_valid():
    params = ParameterManager()
    params.assign_feature_filtering(
        {
            "activate_module": True,
            "filter_rel_int_range_min": 0.0,
            "filter_rel_int_range_max": 1.0,
            "filter_rel_area_range_min": 0.0,
            "filter_rel_area_range_max": 1.0,
        }
    )
    assert isinstance(params.FeatureFilteringParameters, FeatureFilteringParameters)


def test_assign_feature_filtering_invalid():
    params = ParameterManager()
    params.assign_feature_filtering({"asdfg": "asdfg"})
    assert params.FeatureFilteringParameters is None


def test_assign_blank_assignment_valid():
    params = ParameterManager()
    params.assign_blank_assignment(
        {"activate_module": True, "factor": 10, "algorithm": "mean", "value": "area"}
    )
    assert isinstance(params.BlankAssignmentParameters, BlankAssignmentParameters)


def test_assign_blank_assignment_invalid():
    params = ParameterManager()
    params.assign_blank_assignment({"asdfg": "asdfg"})
    assert params.BlankAssignmentParameters is None


def test_assign_group_factor_assignment_valid():
    params = ParameterManager()
    params.assign_group_factor_assignment(
        {"activate_module": True, "algorithm": "mean", "value": "area"}
    )
    assert params.GroupFactAssignmentParameters.activate_module is True


def test_assign_group_factor_assignment_invalid():
    params = ParameterManager()
    params.assign_group_factor_assignment({"asdfg": "asdfg"})
    assert params.GroupFactAssignmentParameters is None


def test_assign_phenotype_qualitative_valid():
    params = ParameterManager()
    params.assign_phenotype_qualitative(
        {"activate_module": True, "factor": 5, "algorithm": "minmax", "value": "area"}
    )
    assert isinstance(params.PhenoQualAssgnParams, PhenoQualAssgnParams)


def test_assign_phenotype_qualitative_invalid():
    params = ParameterManager()
    params.assign_phenotype_qualitative({"asdfg": "asdfg"})
    assert params.PhenoQualAssgnParams is None


def test_assign_phenotype_quant_percent_valid():
    params = ParameterManager()
    params.assign_phenotype_quant_percent(
        {
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "algorithm": "pearson",
            "fdr_corr": "bonferroni",
            "p_val_cutoff": 0.05,
            "coeff_cutoff": 0.7,
        }
    )
    assert isinstance(params.PhenoQuantPercentAssgnParams, PhenoQuantPercentAssgnParams)


def test_assign_phenotype_quant_percent_invalid():
    params = ParameterManager()
    params.assign_phenotype_quant_percent({"asdfg": "asdfg"})
    assert params.PhenoQuantPercentAssgnParams is None


def test_assign_phenotype_quant_concentration_valid():
    params = ParameterManager()
    params.assign_phenotype_quant_concentration(
        {
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "fdr_corr": "bonferroni",
            "algorithm": "pearson",
            "p_val_cutoff": 0.05,
            "coeff_cutoff": 0.7,
        }
    )
    assert isinstance(params.PhenoQuantConcAssgnParams, PhenoQuantConcAssgnParams)


def test_assign_phenotype_quant_concentration_invalid():
    params = ParameterManager()
    params.assign_phenotype_quant_concentration({"asdfg": "asdfg"})
    assert params.PhenoQuantConcAssgnParams is None


def test_assign_spec_lib_matching_cosine_valid():
    params = ParameterManager()
    params.assign_spec_lib_matching_cosine(
        {
            "activate_module": True,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.7,
            "max_precursor_mass_diff": 600,
        }
    )
    assert isinstance(
        params.SpectralLibMatchingCosineParameters, SpectralLibMatchingCosineParameters
    )


def test_assign_spec_lib_matching_cosine_invalid():
    params = ParameterManager()
    params.assign_spec_lib_matching_cosine({"asdfg": "asdfg"})
    assert params.SpectralLibMatchingCosineParameters is None


def test_assign_spec_lib_matching_ms2deepscore_valid():
    params = ParameterManager()
    params.assign_spec_lib_matching_ms2deepscore(
        {"activate_module": True, "score_cutoff": 0.8, "max_precursor_mass_diff": 600}
    )
    assert isinstance(
        params.SpectralLibMatchingDeepscoreParameters,
        SpectralLibMatchingDeepscoreParameters,
    )


def test_assign_spec_lib_matching_ms2deepscore_invalid():
    params = ParameterManager()
    params.assign_spec_lib_matching_ms2deepscore({"asdfg": "asdfg"})
    assert params.SpectralLibMatchingDeepscoreParameters is None


def test_assign_as_kcb_matching_cosine_valid():
    params = ParameterManager()
    params.assign_as_kcb_matching_cosine(
        {
            "activate_module": True,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.5,
            "max_precursor_mass_diff": 600,
        }
    )
    assert isinstance(params.AsKcbCosineMatchingParams, AsKcbCosineMatchingParams)


def test_assign_as_kcb_matching_cosine_invalid():
    params = ParameterManager()
    params.assign_as_kcb_matching_cosine({"asdfg": "asdfg"})
    assert params.AsKcbCosineMatchingParams is None


def test_assign_as_kcb_matching_deepscore_valid():
    params = ParameterManager()
    params.assign_as_kcb_matching_deepscore(
        {"activate_module": True, "score_cutoff": 0.7, "max_precursor_mass_diff": 600}
    )
    assert isinstance(params.AsKcbDeepscoreMatchingParams, AsKcbDeepscoreMatchingParams)


def test_assign_as_kcb_matching_deepscore_invalid():
    params = ParameterManager()
    params.assign_as_kcb_matching_deepscore({"asdfg": "asdfg"})
    assert params.AsKcbDeepscoreMatchingParams is None


def test_assign_parameters_cli_valid():
    json_in = FileManager.load_json_file("tests/test_data/test.parameters.json")
    params = ParameterManager()
    params.assign_parameters_cli(json_in)
    assert params.PeaktableParameters.format == "mzmine3"


def test_assign_parameters_cli_invalid():
    params = ParameterManager()
    with pytest.raises(KeyError):
        params.assign_parameters_cli({"adsasd": "dsfaa"})


def test_to_json_files_valid():
    params = ParameterManager()
    params.PeaktableParameters = PeaktableParameters(
        format="mzmine3",
        filepath="tests/test_data/test.peak_table_quant_full.csv",
        polarity="positive",
    )
    json_dict = params.to_json()
    assert json_dict["PeaktableParameters"]["format"] == "mzmine3"


def test_to_json_output():
    params = ParameterManager()
    json_dict = params.to_json()
    assert (
        json_dict["OutputParameters"] == "No parameters provided or assignment failed"
    )
