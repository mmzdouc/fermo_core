import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from fermo_core.input_output.param_handlers import (
    AsResultsParameters,
    GroupMetadataParameters,
    MS2QueryResultsParameters,
    MsmsParameters,
    PeaktableParameters,
    PhenotypeParameters,
    SpecLibParameters,
    AsKcbCosineMatchingParams,
    AsKcbDeepscoreMatchingParams,
    BlankAssignmentParameters,
    FeatureFilteringParameters,
    GroupFactAssignmentParameters,
    PhenoQualAssgnParams,
    PhenoQuantConcAssgnParams,
    PhenoQuantPercentAssgnParams,
    SpectralLibMatchingCosineParameters,
    SpectralLibMatchingDeepscoreParameters,
    AdductAnnotationParameters,
    FragmentAnnParameters,
    NeutralLossParameters,
    SpecSimNetworkCosineParameters,
    SpecSimNetworkDeepscoreParameters,
    OutputParameters
)

def test_init_as_kcb_valid():
    i = AsKcbCosineMatchingParams(**{
            "activate_module": True,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.5,
            "max_precursor_mass_diff": 600
        })
    assert isinstance(i, AsKcbCosineMatchingParams)
    assert i.to_json().get("activate_module") is not None


def test_init_as_kcb_fail():
    with pytest.raises(TypeError):
        AsKcbCosineMatchingParams(None)


def test_init_as_kcb_deepscore_matching_parameters_valid():
    i = AsKcbDeepscoreMatchingParams(**{
            "activate_module": True,
            "score_cutoff": 0.7,
            "max_precursor_mass_diff": 600
        })
    assert isinstance(i, AsKcbDeepscoreMatchingParams)
    assert i.to_json().get("activate_module") is not None


def test_init_as_kcb_deepscore_matching_parameters_fail():
    with pytest.raises(TypeError):
        AsKcbDeepscoreMatchingParams(None)



def test_init_blank_assignment_parameters_valid():
    assert isinstance(
        BlankAssignmentParameters(
            activate_module=True, value="area", algorithm="median", factor=10
        ),
        BlankAssignmentParameters,
    )


def test_blank_assignment_parameters_algorithm():
    i = BlankAssignmentParameters(**{
            "activate_module": True,
            "factor": 10,
            "algorithm": "mean",
            "value": "area"
        })
    assert isinstance(i, BlankAssignmentParameters)
    assert i.to_json().get("value") == "area"


def test_init_blank_assignment_parameters_fail():
    with pytest.raises(TypeError):
        BlankAssignmentParameters(None)


def test_init_feature_filtering_parameters_valid():
    i = FeatureFilteringParameters(**{
        "activate_module": True,
        "filter_rel_int_range_min": 0.1,
        "filter_rel_int_range_max": 1.0,
        "filter_rel_area_range_min": 0.1,
        "filter_rel_area_range_max": 1.0,
    })
    assert isinstance(
        i, FeatureFilteringParameters
    )
    assert i.to_json().get("filter_rel_int_range_min") == 0.1

def test_init_feature_filtering_parameters_fail():
    with pytest.raises(TypeError):
        FeatureFilteringParameters(None)
    with pytest.raises(ValueError):
        FeatureFilteringParameters(**{
            "filter_rel_int_range_min": 1.0,
            "filter_rel_int_range_max": 0.1,
        })
    with pytest.raises(ValueError):
        FeatureFilteringParameters(**{"filter_rel_area_range_min": 1.0, "filter_rel_area_range_max": 0.1})


def test_phenoqualassgnparams_valid():
    i = PhenoQualAssgnParams(**{
        "activate_module": True,
        "factor": 10,
        "algorithm": "minmax",
        "value": "area",
        "module_passed": True,
    })
    assert isinstance(i, PhenoQualAssgnParams)
    assert i.to_json().get("value") == "area"


def test_phenoqualassgnparams_invalid():
    with pytest.raises(TypeError):
        PhenoQualAssgnParams(None)
    with pytest.raises(ValueError):
        PhenoQualAssgnParams(**{
            "activate_module": True,
            "factor": 10,
            "algorithm": "minmax",
            "value": "asfasd",
            "module_passed": True,
        })
    with pytest.raises(ValueError):
        PhenoQualAssgnParams(**{
            "activate_module": True,
            "factor": 10,
            "algorithm": "asdfasd",
            "value": "area",
            "module_passed": True,
        })


def test_init_group_fact_assignment_parameters_valid():
    i = GroupFactAssignmentParameters(**{
            "activate_module": True,
            "algorithm": "mean",
            "value": "area"
        })
    assert isinstance(i, GroupFactAssignmentParameters)
    assert i.to_json().get("value") == "area"


def test_init_group_fact_assignment_parameters_fail():
    with pytest.raises(TypeError):
        GroupFactAssignmentParameters(None)

def test_phenoquantconcassgnparams_valid():
    i = PhenoQuantConcAssgnParams(**{
        "activate_module": True,
        "sample_avg": "mean",
        "value": "area",
        "algorithm": "pearson",
        "fdr_corr": "bonferroni",
        "p_val_cutoff": 0.05,
        "coeff_cutoff": 0.7,
        "module_passed": True,
    })
    assert isinstance(i, PhenoQuantConcAssgnParams)
    assert i.to_json().get("sample_avg") == "mean"

def test_phenoquantconcassgnparams_fail():
    with pytest.raises(TypeError):
        PhenoQuantConcAssgnParams(None)
    with pytest.raises(ValueError):
        PhenoQuantConcAssgnParams(**{
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "algorithm": "pearson",
            "fdr_corr": "asfasas",
            "p_val_cutoff": 0.05,
            "coeff_cutoff": 0.7,
            "module_passed": True,
        })
    with pytest.raises(ValueError):
        PhenoQuantConcAssgnParams(**{
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "algorithm": "pearson",
            "fdr_corr": "bonferroni",
            "p_val_cutoff": 50,
            "coeff_cutoff": 0.7,
            "module_passed": True,
        })

def test_phenoquantpercassgnparams_valid():
    i = PhenoQuantPercentAssgnParams(**{
        "activate_module": True,
        "sample_avg": "mean",
        "value": "area",
        "algorithm": "pearson",
        "fdr_corr": "bonferroni",
        "p_val_cutoff": 0.05,
        "coeff_cutoff": 0.7,
        "module_passed": True,
    })
    assert isinstance(i, PhenoQuantPercentAssgnParams)
    assert i.to_json().get("sample_avg") == "mean"

def test_phenoquantpercassgnparams_fail():
    with pytest.raises(TypeError):
        PhenoQuantPercentAssgnParams(None)
    with pytest.raises(ValueError):
        PhenoQuantPercentAssgnParams(**{
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "algorithm": "pearson",
            "fdr_corr": "asfasas",
            "p_val_cutoff": 0.05,
            "coeff_cutoff": 0.7,
            "module_passed": True,
        })
    with pytest.raises(ValueError):
        PhenoQuantPercentAssgnParams(**{
            "activate_module": True,
            "sample_avg": "mean",
            "value": "area",
            "algorithm": "pearson",
            "fdr_corr": "bonferroni",
            "p_val_cutoff": 50,
            "coeff_cutoff": 0.7,
            "module_passed": True,
        })


def test_init_spec_lib_matching_cosine_parameters_valid():
    i = SpectralLibMatchingCosineParameters(**{
            "activate_module": True,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.7,
            "max_precursor_mass_diff": 600
        })
    assert isinstance(
        i,
        SpectralLibMatchingCosineParameters,
    )
    assert i.to_json().get("fragment_tol") == 0.1


def test_init_spec_lib_matching_cosine_parameters_fail():
    with pytest.raises(TypeError):
        SpectralLibMatchingCosineParameters(None)


def test_init_spec_lib_matching_deepscore_parameters_valid():
    i = SpectralLibMatchingDeepscoreParameters(**{
            "activate_module": True,
            "score_cutoff": 0.8,
            "max_precursor_mass_diff": 600
        })
    assert isinstance(
        i,
        SpectralLibMatchingDeepscoreParameters,
    )
    assert i.to_json().get("score_cutoff") == 0.8


def test_init_spec_lib_matching_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        SpectralLibMatchingDeepscoreParameters(None)


def test_init_adduct_annotation_parameters_valid():
    i = AdductAnnotationParameters(**{
        "activate_module": True,
        "mass_dev_ppm": 20,
    })
    assert isinstance(
        i, AdductAnnotationParameters
    )
    assert i.to_json().get("mass_dev_ppm") == 20


def test_init_adduct_annotation_parameters_fail():
    with pytest.raises(TypeError):
        AdductAnnotationParameters(None)


def test_init_frag_annotation_parameters_valid():
    i = FragmentAnnParameters(**{
        "activate_module": True,
        "mass_dev_ppm": 20,
    })
    assert isinstance(i, FragmentAnnParameters)
    assert i.to_json().get("mass_dev_ppm") == 20


def test_init_frag_annotation_parameters_fail():
    with pytest.raises(TypeError):
        FragmentAnnParameters(None)


def test_init_neutral_loss_parameters_valid():
    i = NeutralLossParameters(**{"activate_module": True, "mass_dev_ppm": 20})
    assert isinstance(i, NeutralLossParameters)
    assert i.to_json().get("mass_dev_ppm") == 20


def test_init_neutral_loss_parameters_invalid():
    with pytest.raises(TypeError):
        NeutralLossParameters(None)


def test_init_spec_sim_network_cosine_parameters_valid():
    i = SpecSimNetworkCosineParameters(**{
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "fragment_tol": 0.1,
            "min_nr_matched_peaks": 5,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
            "max_precursor_mass_diff": 400,
        })
    assert isinstance(
        i, SpecSimNetworkCosineParameters
    )
    assert i.to_json().get("msms_min_frag_nr") == 5


def test_init_spec_sim_network_cosine_parameters_fail():
    with pytest.raises(TypeError):
        SpecSimNetworkCosineParameters(None)


def test_init_spec_sim_network_deepscore_parameters_valid():
    i = SpecSimNetworkDeepscoreParameters(**{
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
        })
    assert isinstance(
        i,
        SpecSimNetworkDeepscoreParameters,
    )
    assert i.to_json().get("score_cutoff") == 0.7


def test_init_spec_sim_network_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        SpecSimNetworkDeepscoreParameters(None)


def test_init_as_result_parameters_valid():
    i = AsResultsParameters(**{
            "directory_path": "tests/test_data/JABTEZ000000000.1/",
            "similarity_cutoff": "0.7"
        })
    assert isinstance(
        i,
        AsResultsParameters,
    )
    assert i.to_json().get("directory_path") == "JABTEZ000000000.1"


def test_init_as_result_parameters_invalid():
    with pytest.raises(ValidationError):
        AsResultsParameters()


def test_init_group_metadata_parameters_valid():
    i = GroupMetadataParameters(** {"filepath": "tests/test_data/test.group_metadata.csv", "format": "fermo"})
    assert isinstance(i, GroupMetadataParameters)
    assert i.to_json().get("filepath") == "test.group_metadata.csv"


def test_init_group_metadata_parameters_fail():
    with pytest.raises(ValidationError):
        GroupMetadataParameters()
    with pytest.raises(ValueError):
        GroupMetadataParameters(**{
        "filepath": "tests/test_data/test.group_metadata.csv",
        "format": "qwertz",
    })


def test_init_ms2query_result_parameters_valid():
    i = MS2QueryResultsParameters(**{
            "filepath": "tests/test_data/test.ms2query_results.csv",
            "score_cutoff": 0.7,
        })
    assert isinstance(i, MS2QueryResultsParameters)
    assert i.to_json().get("filepath") == "test.ms2query_results.csv"


def test_init_ms2query_result_parameters_invalid():
    with pytest.raises(ValidationError):
        MS2QueryResultsParameters()
    with pytest.raises(ValueError):
        MS2QueryResultsParameters(**{
            "filepath": "tests/test_data/test.ms2query_results.csv",
            "score_cutoff": 5,
        })


def test_init_msms_parameters_valid():
    i = MsmsParameters(**{
            "filepath": "tests/test_data/test.msms.mgf",
            "format": "mgf",
            "rel_int_from": 0.05,
        })
    assert isinstance(i, MsmsParameters)
    assert i.to_json().get("filepath") == "test.msms.mgf"


def test_init_msms_parameters_fail():
    with pytest.raises(ValidationError):
        MsmsParameters()
    with pytest.raises(ValueError):
        MsmsParameters(**{
        "filepath": "tests/test_data/test.msms.mgf",
        "format": "qwertz",
        "rel_int_from": 0.005,
    })
    with pytest.raises(ValueError):
        MsmsParameters(**{
        "filepath": "tests/test_data/test.msms.mgf",
        "format": "mgf",
        "rel_int_from": 5.0,
    })


def test_init_peaktable_parameters_valid():
    i = PeaktableParameters(**{
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        })
    assert isinstance(i, PeaktableParameters)
    assert i.to_json().get("filepath") == "test.peak_table_quant_full.csv"


def test_init_peaktable_parameters_fail():
    with pytest.raises(ValidationError):
        PeaktableParameters()
    with pytest.raises(ValueError):
        PeaktableParameters(**{
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "asdfasdf",
            "polarity": "positive",
        })
    with pytest.raises(ValueError):
        PeaktableParameters(**{
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "asdfasd",
        })


def test_init_phenotype_parameters_valid():
    i = PhenotypeParameters(**{
            "filepath": "tests/test_data/test.bioactivity.qualitative.csv",
            "format": "qualitative",
        })
    assert isinstance(i, PhenotypeParameters)
    assert i.to_json().get("filepath") == "test.bioactivity.qualitative.csv"


def test_init_phenotype_parameters_fail():
    with pytest.raises(ValidationError):
        PhenotypeParameters()
    with pytest.raises(ValueError):
        PhenotypeParameters(**{
            "filepath": "tests/test_data/test.bioactivity.qualitative.csv",
            "format": "asdfasdf",
        })


def test_init_speclib_parameters_valid():
    i = SpecLibParameters(**{"dirpath": "tests/test_data/spec_lib/", "format": "mgf"})
    assert isinstance(i, SpecLibParameters)
    assert i.to_json().get("dirpath") == "spec_lib"


def test_init_speclib_parameters_fail():
    with pytest.raises(ValidationError):
        SpecLibParameters()
    with pytest.raises(ValueError):
        SpecLibParameters(**{"dirpath": "tests/test_data/spec_lib/", "format": "asdfas"})



def test_outputparams_valid():
    i = OutputParameters(
        directory_path=Path("tests/test_data/")
    )
    assert isinstance(i, OutputParameters)
    assert i.to_json().get("directory_path") == "test_data/results"
    assert i.directory_path.exists()
    os.rmdir("tests/test_data/results")


def test_test_outputparams_fail():
    with pytest.raises(ValidationError):
        OutputParameters(directory_path=Path("dgsdgfsdfgs/"))
    with pytest.raises(ValidationError):
        OutputParameters()


