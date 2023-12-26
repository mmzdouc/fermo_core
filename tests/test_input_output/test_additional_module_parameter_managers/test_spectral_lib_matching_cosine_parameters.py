import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    SpectralLibMatchingCosineParameters,
)


def test_init_spec_lib_matching_cosine_parameters_valid():
    json_dict = {
        "activate_module": True,
        "fragment_tol": 0.1,
        "min_nr_matched_peaks": 5,
        "score_cutoff": 0.7,
    }
    assert isinstance(
        SpectralLibMatchingCosineParameters(**json_dict),
        SpectralLibMatchingCosineParameters,
    )


def test_init_spec_lib_matching_cosine_parameters_fail():
    with pytest.raises(TypeError):
        SpectralLibMatchingCosineParameters(None)
