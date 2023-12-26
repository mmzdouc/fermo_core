import pytest

from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)


def test_init_spec_sim_network_cosine_parameters_valid():
    json_dict = {
        "activate_module": True,
        "mass_dev_ppm": 5,
        "fragment_tol": 0.1,
        "min_nr_matched_peaks": 5,
        "score_cutoff": 0.7,
        "max_nr_links": 10,
        "max_precursor_mass_diff": 400,
    }
    assert isinstance(
        SpecSimNetworkCosineParameters(**json_dict), SpecSimNetworkCosineParameters
    )


def test_init_spec_sim_network_cosine_parameters_fail():
    with pytest.raises(TypeError):
        SpecSimNetworkCosineParameters(None)
