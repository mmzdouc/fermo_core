import pytest

from fermo_core.data_analysis.sim_networks_manager.class_ms2deepscore_networker import (
    Ms2deepscoreNetworker,
)
from fermo_core.input_output.param_handlers import SpecSimNetworkDeepscoreParameters


def test_init_valid():
    assert isinstance(Ms2deepscoreNetworker(), Ms2deepscoreNetworker)


def test_spec_sim_networking_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkDeepscoreParameters(
        **{
            "activate_module": True,
            "score_cutoff": 0.8,
            "max_nr_links": 10,
            "msms_min_frag_nr": 5,
        }
    )
    assert (
        Ms2deepscoreNetworker().spec_sim_networking(
            features, feature_instance, settings
        )
        is not None
    )


def test_create_network_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkDeepscoreParameters(
        **{
            "activate_module": True,
            "score_cutoff": 0.8,
            "max_nr_links": 10,
            "msms_min_frag_nr": 5,
        }
    )
    scores = Ms2deepscoreNetworker().spec_sim_networking(
        features, feature_instance, settings
    )
    assert Ms2deepscoreNetworker().create_network(scores, settings) is not None
