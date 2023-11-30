import pytest

from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkDeepscoreParameters,
)


def test_init_spec_sim_network_deepscore_parameters_valid():
    json_dict = {
        "activate_module": True,
        "directory_path": "fermo_core/libraries",
        "score_cutoff": 0.7,
        "max_nr_links": 10,
    }
    assert isinstance(
        SpecSimNetworkDeepscoreParameters(**json_dict),
        SpecSimNetworkDeepscoreParameters,
    )


def test_init_spec_sim_network_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        SpecSimNetworkDeepscoreParameters(None)


def test_default_libraries_folder_valid():
    instance = SpecSimNetworkDeepscoreParameters()
    default_path = instance.directory_path.name
    assert default_path == "libraries"
    assert instance.directory_path.exists()
