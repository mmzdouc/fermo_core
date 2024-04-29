import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    AsKcbDeepscoreMatchingParams,
)


def test_init_as_kcb_deepscore_matching_parameters_valid():
    assert isinstance(
        AsKcbDeepscoreMatchingParams(),
        AsKcbDeepscoreMatchingParams,
    )


def test_init_spec_lib_matching_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        AsKcbDeepscoreMatchingParams(None)


def test_to_json():
    obj_inst = AsKcbDeepscoreMatchingParams()
    assert obj_inst.to_json().get("activate_module") is not None
