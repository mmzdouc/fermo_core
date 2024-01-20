import pytest


from pydantic import ValidationError

from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import (
    PeaktableParameters,
    MsmsParameters,
    PhenotypeParameters,
    GroupMetadataParameters,
    SpecLibParameters,
)
from fermo_core.input_output.output_file_parameter_managers import OutputParameters
from fermo_core.input_output.core_module_parameter_managers import (
    AdductAnnotationParameters,
    SpecSimNetworkCosineParameters,
    SpecSimNetworkDeepscoreParameters,
)
from fermo_core.input_output.additional_module_parameter_managers import (
    FeatureFilteringParameters,
    BlankAssignmentParameters,
    PhenotypeAssignmentFoldParameters,
    SpectralLibMatchingCosineParameters,
    SpectralLibMatchingDeepscoreParameters,
    Ms2QueryAnnotationParameters,
)


def test_init_parameter_manager_valid():
    assert isinstance(ParameterManager(), ParameterManager)


def test_parameter_manager_properties_valid():
    params = ParameterManager()
    assert params.PeaktableParameters is None
    assert isinstance(params.AdductAnnotationParameters, AdductAnnotationParameters)


def test_assign_peaktable_valid():
    params = ParameterManager()
    params.assign_peaktable(
        {
            "filepath": "example_data/case_study_peak_table_quant_full.csv",
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
                "filepath": "example_data/case_study_peak_table_quant_full.csv",
            }
        )


def test_assign_msms_valid():
    params = ParameterManager()
    params.assign_msms(
        {"filepath": "example_data/case_study_MSMS.mgf", "format": "mgf"}
    )
    assert isinstance(params.MsmsParameters, MsmsParameters)


def test_assign_msms_invalid():
    params = ParameterManager()
    params.assign_msms(
        {
            "filepath": "example_data/case_study_MSMS.mgf",
        }
    )
    assert params.MsmsParameters is None


def test_assign_phenotype_valid():
    params = ParameterManager()
    params.assign_phenotype(
        {"filepath": "example_data/case_study_bioactivity.csv", "format": "fermo"}
    )
    assert isinstance(params.PhenotypeParameters, PhenotypeParameters)


def test_assign_phenotype_invalid():
    params = ParameterManager()
    params.assign_phenotype(
        {
            "filepath": "example_data/case_study_bioactivity.csv",
        }
    )
    assert params.PhenotypeParameters is None


def test_assign_group_metadata_valid():
    params = ParameterManager()
    params.assign_group_metadata(
        {"filepath": "example_data/case_study_group_metadata.csv", "format": "fermo"}
    )
    assert isinstance(params.GroupMetadataParameters, GroupMetadataParameters)


def test_assign_group_metadata_invalid():
    params = ParameterManager()
    params.assign_group_metadata(
        {
            "filepath": "example_data/case_study_group_metadata.csv",
        }
    )
    assert params.GroupMetadataParameters is None


def test_assign_spectral_library_valid():
    params = ParameterManager()
    params.assign_spectral_library(
        {"filepath": "example_data/case_study_spectral_library.mgf", "format": "mgf"}
    )
    assert isinstance(params.SpecLibParameters, SpecLibParameters)


def test_assign_spectral_library_invalid():
    params = ParameterManager()
    params.assign_spectral_library(
        {
            "filepath": "example_data/case_study_spectral_library.mgf",
        }
    )
    assert params.SpecLibParameters is None


def test_assign_output_valid():
    params = ParameterManager()
    params.assign_output(
        {"filepath": "example_data/case_study_fermo.json", "format": "json"}
    )
    assert isinstance(params.OutputParameters, OutputParameters)


def test_assign_output_invalid():
    params = ParameterManager()
    params.assign_output(
        {
            "sasd": "dasdas",
        }
    )
    assert params.OutputParameters.format == "json"


def test_assign_adduct_annotation_valid():
    params = ParameterManager()
    params.assign_adduct_annotation({"activate_module": True, "mass_dev_ppm": 20.0})
    assert isinstance(params.AdductAnnotationParameters, AdductAnnotationParameters)


def test_assign_adduct_annotation_invalid():
    params = ParameterManager()
    params.assign_adduct_annotation(
        {
            "activate_module": True,
        }
    )
    assert params.AdductAnnotationParameters.mass_dev_ppm == 20.0


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
    assert params.SpecSimNetworkCosineParameters.msms_min_frag_nr == 5


def test_assign_spec_sim_networking_ms2deepscore_valid():
    params = ParameterManager()
    params.assign_spec_sim_networking_ms2deepscore(
        {
            "activate_module": True,
            "directory_path": "fermo_core/libraries",
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
    assert params.SpecSimNetworkDeepscoreParameters.score_cutoff == 0.7


def test_assign_feature_filtering_valid():
    params = ParameterManager()
    params.assign_feature_filtering(
        {
            "activate_module": True,
            "filter_rel_int_range": [0.0, 1.0],
            "filter_rel_area_range": [0.0, 1.0],
        }
    )
    assert isinstance(params.FeatureFilteringParameters, FeatureFilteringParameters)


def test_assign_feature_filtering_invalid():
    params = ParameterManager()
    params.assign_feature_filtering({"asdfg": "asdfg"})
    assert params.FeatureFilteringParameters.filter_rel_int_range is None


def test_assign_blank_assignment_valid():
    params = ParameterManager()
    params.assign_blank_assignment({"activate_module": True, "column_ret_fold": 10})
    assert isinstance(params.BlankAssignmentParameters, BlankAssignmentParameters)


def test_assign_blank_assignment_invalid():
    params = ParameterManager()
    params.assign_blank_assignment({"asdfg": "asdfg"})
    assert params.BlankAssignmentParameters.column_ret_fold == 10


def test_assign_phenotype_assignment_fold_valid():
    params = ParameterManager()
    params.assign_phenotype_assignment_fold(
        {"activate_module": True, "fold_diff": 10, "data_type": "percentage"}
    )
    assert isinstance(
        params.PhenotypeAssignmentFoldParameters, PhenotypeAssignmentFoldParameters
    )


def test_assign_phenotype_assignment_fold_invalid():
    params = ParameterManager()
    params.assign_phenotype_assignment_fold({"asdfg": "asdfg"})
    assert params.PhenotypeAssignmentFoldParameters.fold_diff == 10


def test_assign_spec_lib_matching_cosine_valid():
    params = ParameterManager()
    params.assign_spec_lib_matching_cosine(
        {
            "activate_module": True,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.7,
        }
    )
    assert isinstance(
        params.SpectralLibMatchingCosineParameters, SpectralLibMatchingCosineParameters
    )


def test_assign_spec_lib_matching_cosine_invalid():
    params = ParameterManager()
    params.assign_spec_lib_matching_cosine({"asdfg": "asdfg"})
    assert params.SpectralLibMatchingCosineParameters.fragment_tol == 0.1


def test_assign_spec_lib_matching_ms2deepscore_valid():
    params = ParameterManager()
    params.assign_spec_lib_matching_ms2deepscore(
        {
            "activate_module": True,
            "directory_path": "fermo_core/libraries",
            "score_cutoff": 0.7,
        }
    )
    assert isinstance(
        params.SpectralLibMatchingDeepscoreParameters,
        SpectralLibMatchingDeepscoreParameters,
    )


def test_assign_spec_lib_matching_ms2deepscore_invalid():
    params = ParameterManager()
    params.assign_spec_lib_matching_ms2deepscore({"asdfg": "asdfg"})
    assert params.SpectralLibMatchingDeepscoreParameters.score_cutoff == 0.7


def test_assign_ms2query_valid():
    params = ParameterManager()
    params.assign_ms2query(
        {
            "activate_module": True,
            "directory_path": "fermo_core/libraries",
            "consider_blank": True,
            "filter_rel_int_range": [0.0, 0.1],
        }
    )
    assert isinstance(params.Ms2QueryAnnotationParameters, Ms2QueryAnnotationParameters)


def test_assign_ms2query_invalid():
    params = ParameterManager()
    params.assign_ms2query({"asdfg": "asdfg"})
    assert params.Ms2QueryAnnotationParameters.filter_rel_int_range is None


def test_assign_parameters_cli_valid():
    json_in = FileManager.load_json_file("example_data/case_study_parameters.json")
    params = ParameterManager()
    params.assign_parameters_cli(json_in)
    assert params.PeaktableParameters.format == "mzmine3"


def test_assign_parameters_cli_invalid():
    params = ParameterManager()
    with pytest.raises(KeyError):
        params.assign_parameters_cli({"adsasd": "dsfaa"})


def test_assign_files_parameters_valid():
    json_in = FileManager.load_json_file("example_data/case_study_parameters.json")
    params = ParameterManager()
    params.assign_files_parameters(json_in)
    assert params.PeaktableParameters.format == "mzmine3"


def test_assign_files_parameters_invalid():
    params = ParameterManager()
    with pytest.raises(KeyError):
        params.assign_files_parameters({"adsasd": "dsfaa"})


def test_assign_core_modules_parameters_valid():
    json_in = FileManager.load_json_file("example_data/case_study_parameters.json")
    params = ParameterManager()
    params.assign_core_modules_parameters(json_in)
    assert params.AdductAnnotationParameters.mass_dev_ppm == 20.0


def test_assign_core_modules_parameters_invalid():
    params = ParameterManager()
    params.assign_core_modules_parameters({"adsasd": "dsfaa"})
    assert params.AdductAnnotationParameters.mass_dev_ppm == 20.0


def test_assign_additional_modules_parameters_valid():
    json_in = FileManager.load_json_file("example_data/case_study_parameters.json")
    params = ParameterManager()
    params.assign_additional_modules_parameters(json_in)
    assert params.FeatureFilteringParameters.activate_module is True


def test_assign_additional_modules_parameters_invalid():
    params = ParameterManager()
    params.assign_additional_modules_parameters({"adsasd": "dsfaa"})
    assert params.FeatureFilteringParameters.activate_module is False


def test_to_json_files_valid():
    params = ParameterManager()
    params.PeaktableParameters = PeaktableParameters(
        format="mzmine3",
        filepath="example_data/case_study_peak_table_quant_full.csv",
        polarity="positive",
    )
    json_dict = params.to_json()
    assert json_dict["PeaktableParameters"]["format"] == "mzmine3"


def test_to_json_output():
    params = ParameterManager()
    json_dict = params.to_json()
    assert json_dict["OutputParameters"]["format"] == "json"
