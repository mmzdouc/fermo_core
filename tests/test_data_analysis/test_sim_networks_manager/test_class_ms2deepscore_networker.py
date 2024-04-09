from func_timeout import FunctionTimedOut

import pytest

from fermo_core.data_analysis.sim_networks_manager.class_ms2deepscore_networker import (
    Ms2deepscoreNetworker,
)
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkDeepscoreParameters,
)


def test_init_valid():
    assert isinstance(Ms2deepscoreNetworker(), Ms2deepscoreNetworker)


def test_spec_sim_networking_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkDeepscoreParameters()
    assert (
        Ms2deepscoreNetworker().spec_sim_networking(
            features, feature_instance, settings
        )
        is not None
    )


def test_spec_sim_networking_timeout_invalid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkDeepscoreParameters()
    settings.maximum_runtime = 0.1
    with pytest.raises(FunctionTimedOut):
        Ms2deepscoreNetworker().spec_sim_networking(
            features, feature_instance, settings
        )


def test_create_network_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkDeepscoreParameters()
    scores = Ms2deepscoreNetworker().spec_sim_networking(
        features, feature_instance, settings
    )
    assert Ms2deepscoreNetworker().create_network(scores, settings) is not None
