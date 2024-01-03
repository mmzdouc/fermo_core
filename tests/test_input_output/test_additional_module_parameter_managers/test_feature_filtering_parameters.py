import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    FeatureFilteringParameters,
)


def test_init_feature_filtering_parameters_valid():
    json_dict = {
        "activate_module": True,
        "filter_rel_int_range": [0.0, 1.0],
    }
    assert isinstance(
        FeatureFilteringParameters(**json_dict), FeatureFilteringParameters
    )


def test_init_feature_filtering_parameters_fail():
    with pytest.raises(TypeError):
        FeatureFilteringParameters(None)


def test_rel_int_range_scrambled_valid():
    json_dict = {
        "filter_rel_int_range": [1.0, 0.0],
    }
    assert isinstance(
        FeatureFilteringParameters(**json_dict), FeatureFilteringParameters
    )


def test_rel_int_range_invalid():
    with pytest.raises(ValueError):
        json_dict = {
            "filter_rel_int_range": [0.0],
        }
        FeatureFilteringParameters(**json_dict)
