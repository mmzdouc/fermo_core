import pytest

from fermo_core.data_analysis.sim_networks_manager.class_sim_networks_manager import (
    SimNetworksManager,
)

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)
from fermo_core.data_analysis.sim_networks_manager.class_ms2deepscore_networker import (
    Ms2deepscoreNetworker,
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


def test_log_filtered_feature_no_msms_valid(sim_networks_manager_instance):
    assert sim_networks_manager_instance.log_filtered_feature_no_msms(1) is None


def test_log_filtered_feature_nr_fragments_valid(sim_networks_manager_instance):
    assert (
        sim_networks_manager_instance.log_filtered_feature_nr_fragments(1, 1, 1) is None
    )


def test_return_valid(sim_networks_manager_instance):
    stats, features, samples = sim_networks_manager_instance.return_attrs()
    assert stats is not None


@pytest.mark.slow
def test_run_analysis_valid(sim_networks_manager_instance):
    sim_networks_manager_instance.run_analysis()
    assert sim_networks_manager_instance.stats.networks is not None
    assert sim_networks_manager_instance.features.get(12).networks is not None


@pytest.mark.slow
def test_run_modified_cosine_alg_valid(sim_networks_manager_instance):
    sim_networks_manager_instance.run_modified_cosine_alg()
    assert sim_networks_manager_instance.stats.networks is not None
    assert sim_networks_manager_instance.features.get(12).networks is not None


@pytest.mark.slow
def test_run_ms2deepscore_alg_valid(sim_networks_manager_instance):
    sim_networks_manager_instance.run_ms2deepscore_alg()
    assert sim_networks_manager_instance.stats.networks is not None
    assert sim_networks_manager_instance.features.get(12).networks is not None


def test_filter_input_spectra_valid(sim_networks_manager_instance, feature_instance):
    features = (12, 13)
    assert (
        sim_networks_manager_instance.filter_input_spectra(
            features=features, feature_repo=feature_instance, msms_min_frag_nr=5
        )
        is not None
    )


def test_filter_input_spectra_invalid(sim_networks_manager_instance, feature_instance):
    features = (12, 13)
    assert (
        sim_networks_manager_instance.filter_input_spectra(
            features=features, feature_repo=feature_instance, msms_min_frag_nr=10000
        )["included"]
        == set()
    )


@pytest.mark.slow
def test_format_network_for_storage_cosine_valid(
    sim_networks_manager_instance, feature_instance
):
    features = (12, 13)
    scores = ModCosineNetworker().spec_sim_networking(
        features=features,
        feature_repo=feature_instance,
        settings=sim_networks_manager_instance.params.SpecSimNetworkCosineParameters,
    )
    network = ModCosineNetworker().create_network(
        scores=scores,
        settings=sim_networks_manager_instance.params.SpecSimNetworkCosineParameters,
    )
    assert (
        sim_networks_manager_instance.format_network_for_storage(graph=network)
        is not None
    )


@pytest.mark.slow
def test_format_network_for_storage_ms2deep_valid(
    sim_networks_manager_instance, feature_instance
):
    features = (12, 13)
    scores = Ms2deepscoreNetworker().spec_sim_networking(
        features=features,
        feature_repo=feature_instance,
        settings=sim_networks_manager_instance.params.SpecSimNetworkDeepscoreParameters,
    )
    network = Ms2deepscoreNetworker().create_network(
        scores=scores,
        settings=sim_networks_manager_instance.params.SpecSimNetworkDeepscoreParameters,
    )
    assert (
        sim_networks_manager_instance.format_network_for_storage(graph=network)
        is not None
    )


def test_store_network_data_valid(sim_networks_manager_instance):
    network_name = "foo"
    network_data = {
        "network": "foo",
        "subnetworks": {0: "bar"},
        "summary": {0: {12, 13}},
    }
    included = tuple([12, 13])
    sim_networks_manager_instance.store_network_data(
        network_name=network_name, network_data=network_data, features=included
    )
    assert sim_networks_manager_instance.stats.networks is not None
