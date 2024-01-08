from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


def test_init_feature_valid():
    assert isinstance(Feature(), Feature)
