import argparse
import json
import jsonschema
from pathlib import Path
import pytest

from fermo_core.input_output.class_parameter_manager import ParameterManager


def test_instantiate_object():
    assert isinstance(ParameterManager("0.1.0", Path("my/path/here")), ParameterManager)


@pytest.fixture
def params_manager():
    return ParameterManager("0.1.0", Path("my/path/here"))


@pytest.fixture
def attributes():
    return (
        "version",
        "root",
        "session",
        "peaktable",
        "msms",
        "phenotype",
        "group_metadata",
        "spectral_library",
        "phenotype_algorithm_settings",
        "mass_dev_ppm",
        "msms_frag_min",
        "column_ret_fold",
        "fragment_tol",
        "spectral_sim_score_cutoff",
        "max_nr_links_spec_sim",
        "min_nr_matched_peaks",
        "spectral_sim_network_alg",
        "ms2query",
        "rel_int_range",
        "max_library_size",
    )


def test_expected_attributes(params_manager, attributes):
    for attr in attributes:
        assert hasattr(
            params_manager, attr
        ), f"Attribute '{attr}  is missing in ParamsManager"


def test_unexpected_values_stats(params_manager, attributes):
    unexpected_attributes = []
    for attr in dir(params_manager):
        if (
            (not attr.startswith("_"))
            and (attr not in attributes)
            and (not callable(getattr(params_manager, attr)))
        ):
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in class 'Stats': {unexpected_attributes}."


def test_define_argparse_args(params_manager):
    parser = params_manager.define_argparse_args()
    assert isinstance(parser, argparse.ArgumentParser)


def test_json_default_parameters_jsonschema(params_manager):
    schema = params_manager.load_json_file("fermo_core/config/schema.json")
    default_params = params_manager.load_json_file(
        "fermo_core/example_data/case_study_parameters.json"
    )
    try:
        jsonschema.validate(instance=default_params, schema=schema)
    except jsonschema.exceptions.ValidationError:
        pytest.fail("JSON schema validation failed.")


@pytest.fixture
def default_params(params_manager):
    return params_manager.load_json_file(
        "fermo_core/example_data/case_study_parameters.json"
    )


@pytest.fixture
def example_params(params_manager):
    return params_manager.load_json_file(
        "fermo_core/example_data/case_study_parameters.json"
    )


def test_assign_peaktable_valid(params_manager, example_params, default_params):
    params_manager.assign_peaktable(example_params, default_params)
    assert (
        params_manager.peaktable.get("filename")
        == "example_data/case_study_peak_table_quant_full.csv"
    )
    assert params_manager.peaktable.get("format") == "mzmine3"


def test_assign_peaktable_invalid(params_manager, default_params):
    with pytest.raises(KeyError):
        params_manager.assign_peaktable(dict(), default_params)


def test_assign_msms_valid(params_manager, example_params, default_params):
    params_manager.assign_msms(example_params, default_params)
    assert params_manager.msms.get("filename") == "example_data/case_study_MSMS.mgf"
    assert params_manager.msms.get("format") == "mgf"


def test_assign_msms_invalid(params_manager, default_params):
    assert params_manager.assign_msms(dict(), default_params) is None


def test_assign_phenotype_valid(params_manager, example_params, default_params):
    params_manager.assign_phenotype(example_params, default_params)
    assert (
        params_manager.phenotype.get("filename")
        == "example_data/case_study_bioactivity.csv"
    )
    assert params_manager.phenotype.get("format") == "fermo"
    assert params_manager.phenotype.get("mode") == "percentage"
    assert params_manager.phenotype.get("algorithm") == "all"


def test_assign_group_metadata_valid(params_manager, example_params, default_params):
    params_manager.assign_group_metadata(example_params, default_params)
    assert (
        params_manager.group_metadata.get("filename")
        == "example_data/case_study_group_metadata.csv"
    )
    assert params_manager.group_metadata.get("format") == "fermo"


def test_assign_spectral_library_valid(params_manager, example_params, default_params):
    params_manager.assign_spectral_library(example_params, default_params)
    assert (
        params_manager.spectral_library.get("filename")
        == "example_data/case_study_spectral_library.mgf"
    )
    assert params_manager.spectral_library.get("format") == "mgf"


def test_assign_phenotype_algorithm_valid(
    params_manager, example_params, default_params
):
    params_manager.assign_phenotype_algorithm_settings(example_params, default_params)
    assert (
        params_manager.phenotype_algorithm_settings.get("fold_difference").get("value")
        == 10
    )


def test_assign_mass_dev_ppm_valid(params_manager, example_params, default_params):
    params_manager.assign_mass_dev_ppm(example_params, default_params)
    assert params_manager.mass_dev_ppm == 20


def test_assign_msms_frag_min_valid(params_manager, example_params, default_params):
    params_manager.assign_msms_frag_min(example_params, default_params)
    assert params_manager.msms_frag_min == 5


def test_assign_column_ret_fold_valid(params_manager, example_params, default_params):
    params_manager.assign_column_ret_fold(example_params, default_params)
    assert params_manager.column_ret_fold == 10


def test_assign_fragment_tol_valid(params_manager, example_params, default_params):
    params_manager.assign_fragment_tol(example_params, default_params)
    assert params_manager.fragment_tol == 0.1


def test_assign_spectral_sim_score_cutoff_valid(
    params_manager, example_params, default_params
):
    params_manager.assign_spectral_sim_score_cutoff(example_params, default_params)
    assert params_manager.spectral_sim_score_cutoff == 0.7


def test_assign_max_nr_links_spec_sim_valid(
    params_manager, example_params, default_params
):
    params_manager.assign_max_nr_links_spec_sim(example_params, default_params)
    assert params_manager.max_nr_links_spec_sim == 10


def test_assign_min_nr_matched_peaks_valid(
    params_manager, example_params, default_params
):
    params_manager.assign_min_nr_matched_peaks(example_params, default_params)
    assert params_manager.min_nr_matched_peaks == 5


def test_assign_spectral_sim_network_alg_valid(
    params_manager, example_params, default_params
):
    params_manager.assign_spectral_sim_network_alg(example_params, default_params)
    assert params_manager.spectral_sim_network_alg == "modified_cosine"


def test_assign_ms2query_valid(params_manager, example_params, default_params):
    params_manager.assign_ms2query(example_params, default_params)
    assert params_manager.ms2query.get("mode") == "off"
    assert params_manager.ms2query.get("annot_features_from_blanks") == "off"
    assert params_manager.ms2query.get("range") == [0.0, 1.0]


def test_assign_rel_int_range_valid(params_manager, example_params, default_params):
    params_manager.assign_rel_int_range(example_params, default_params)
    assert params_manager.rel_int_range == (0.0, 1.0)


def test_parse_parameters_valid(params_manager, example_params, default_params):
    params_manager.parse_parameters(example_params, default_params)
    assert params_manager.mass_dev_ppm == 20
