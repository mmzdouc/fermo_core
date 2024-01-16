import pytest

from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkDeepscoreParameters,
)


def test_init_spec_sim_network_deepscore_parameters_valid():
    json_dict = {
        "activate_module": True,
        "default_file_path": "fermo_core/libraries",
        "file_path": "fermo_core/libraries",
        "score_cutoff": 0.7,
        "max_nr_links": 10,
        "msms_min_frag_nr": 5,
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
    default_dir_name = instance.default_file_path.parent.resolve()
    assert default_dir_name.name == "ms2deepscore"
    assert default_dir_name.exists()
