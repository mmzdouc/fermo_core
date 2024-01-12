from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_feature.dataclass_feature import SimNetworks


def test_init_feature_valid():
    assert isinstance(Feature(), Feature)


def test_init_sim_networks_valid():
    assert isinstance(SimNetworks(algorithm="mod_cosine", network_id=0), SimNetworks)
