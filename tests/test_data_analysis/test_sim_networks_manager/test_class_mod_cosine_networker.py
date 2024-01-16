import func_timeout
import pytest

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)

from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)


def test_init_mod_cosine_networker_valid():
    assert isinstance(ModCosineNetworker(), ModCosineNetworker)


@pytest.mark.slow
def test_spec_sim_networking_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkCosineParameters()
    assert (
        ModCosineNetworker().spec_sim_networking(features, feature_instance, settings)
        is not None
    )


def test_spec_sim_networking_runtime_invalid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkCosineParameters()
    settings.maximum_runtime = 0.0000001
    with pytest.raises(func_timeout.FunctionTimedOut):
        ModCosineNetworker().spec_sim_networking(features, feature_instance, settings)


@pytest.mark.slow
def test_create_network_valid(feature_instance):
    features = (12, 13)
    settings = SpecSimNetworkCosineParameters()
    scores = ModCosineNetworker().spec_sim_networking(
        features, feature_instance, settings
    )
    assert ModCosineNetworker().create_network(scores, settings) is not None
