import pytest

from fermo_core.input_output.core_module_parameter_managers import (
    NeutralLossParameters,
)


def test_init_neutral_loss_parameters_valid():
    json_dict = {
        "activate_module": True,
        "mass_dev_ppm": 20,
    }
    assert isinstance(NeutralLossParameters(**json_dict), NeutralLossParameters)


def test_init_neutral_loss_parameters_invalid():
    with pytest.raises(TypeError):
        NeutralLossParameters(None)
