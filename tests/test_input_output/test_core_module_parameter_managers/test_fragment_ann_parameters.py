import pytest

from fermo_core.input_output.core_module_parameter_managers import (
    FragmentAnnParameters,
)


def test_init_adduct_annotation_parameters_valid():
    json_dict = {
        "activate_module": True,
        "mass_dev_ppm": 20,
    }
    assert isinstance(FragmentAnnParameters(**json_dict), FragmentAnnParameters)


def test_init_adduct_annotation_parameters_fail():
    with pytest.raises(TypeError):
        FragmentAnnParameters(None)
