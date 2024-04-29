import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    SpectralLibMatchingDeepscoreParameters,
)


def test_init_spec_lib_matching_deepscore_parameters_valid():
    json_dict = {
        "activate_module": True,
        "score_cutoff": 0.7,
    }
    assert isinstance(
        SpectralLibMatchingDeepscoreParameters(**json_dict),
        SpectralLibMatchingDeepscoreParameters,
    )


def test_init_spec_lib_matching_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        SpectralLibMatchingDeepscoreParameters(None)


def test_to_json():
    obj_inst = SpectralLibMatchingDeepscoreParameters()
    assert obj_inst.to_json().get("activate_module") is not None
