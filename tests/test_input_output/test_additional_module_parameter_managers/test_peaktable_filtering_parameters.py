import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    PeaktableFilteringParameters,
)


def test_init_peaktable_filtering_parameters_valid():
    json_dict = {
        "activate_module": True,
        "filter_rel_int_range": [0.0, 1.0],
    }
    assert isinstance(
        PeaktableFilteringParameters(**json_dict), PeaktableFilteringParameters
    )


def test_init_peaktable_filtering_parameters_fail():
    with pytest.raises(TypeError):
        PeaktableFilteringParameters(None)


def test_rel_int_range_scrambled_valid():
    json_dict = {
        "activate_module": True,
        "filter_rel_int_range": [1.0, 0.0],
    }
    assert isinstance(
        PeaktableFilteringParameters(**json_dict), PeaktableFilteringParameters
    )


def test_rel_int_range_invalid():
    with pytest.raises(ValueError):
        json_dict = {
            "activate_module": True,
            "filter_rel_int_range": [0.0],
        }
        PeaktableFilteringParameters(**json_dict)
