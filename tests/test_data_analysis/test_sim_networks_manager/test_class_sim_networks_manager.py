import pytest

from fermo_core.data_analysis.sim_networks_manager.class_sim_networks_manager import (
    SimNetworksManager,
)


@pytest.fixture
def sim_networks_manager_instance(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return SimNetworksManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


def test_init_valid(sim_networks_manager_instance):
    assert isinstance(sim_networks_manager_instance, SimNetworksManager)


def test_return_valid(sim_networks_manager_instance):
    stats, features, samples = sim_networks_manager_instance.return_attrs()
    assert stats is not None


def test_run_modified_cosine_alg(sim_networks_manager_instance):
    sim_networks_manager_instance.run_modified_cosine_alg()
    assert sim_networks_manager_instance.stats.networks is not None
    assert sim_networks_manager_instance.features.get(33).networks is not None
