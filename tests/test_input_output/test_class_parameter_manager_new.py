import pytest


from pydantic import ValidationError

from fermo_core.input_output.class_parameter_manager import ParameterManager
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


def test_assign_peaktable_filtering_valid():
    params = ParameterManager()
    params.assign_peaktable_filtering(
        {"activate_module": True, "filter_rel_int_range": [0.0, 1.0]}
    )
    assert isinstance(params.PeaktableFilteringParameters, PeaktableFilteringParameters)


def test_assign_peaktable_filtering_invalid():
    params = ParameterManager()
    params.assign_peaktable_filtering({"asdfg": "asdfg"})
    assert params.PeaktableFilteringParameters.filter_rel_int_range[0] == 0.0
