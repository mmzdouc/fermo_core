import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    SpectralLibMatchingDeepscoreParameters,
)


def test_init_spec_lib_matching_deepscore_parameters_valid():
    json_dict = {
        "activate_module": True,
        "directory_path": "fermo_core/libraries",
        "score_cutoff": 0.7,
    }
    assert isinstance(
        SpectralLibMatchingDeepscoreParameters(**json_dict),
        SpectralLibMatchingDeepscoreParameters,
    )


def test_init_spec_lib_matching_deepscore_parameters_fail():
    with pytest.raises(TypeError):
        SpectralLibMatchingDeepscoreParameters(None)


def test_default_libraries_folder_valid():
    instance = SpectralLibMatchingDeepscoreParameters()
    default_path = instance.directory_path.name
    assert default_path == "libraries"
    assert instance.directory_path.exists()
