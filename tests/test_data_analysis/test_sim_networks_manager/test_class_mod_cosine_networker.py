import pytest

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)
from fermo_core.input_output.param_handlers import SpecSimNetworkCosineParameters


def test_init_mod_cosine_networker_valid():
    assert isinstance(ModCosineNetworker(), ModCosineNetworker)


@pytest.mark.slow
def test_spec_sim_networking_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkCosineParameters(
        **{
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "fragment_tol": 0.1,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
        }
    )
    assert (
        ModCosineNetworker().spec_sim_networking(features, feature_instance, settings)
        is not None
    )


@pytest.mark.slow
def test_create_network_valid(feature_instance):
    features = (12, 13)
    settings = settings = SpecSimNetworkCosineParameters(
        **{
            "activate_module": True,
            "msms_min_frag_nr": 5,
            "fragment_tol": 0.1,
            "score_cutoff": 0.7,
            "max_nr_links": 10,
        }
    )
    scores = ModCosineNetworker().spec_sim_networking(
        features, feature_instance, settings
    )
    assert ModCosineNetworker().create_network(scores, settings) is not None
