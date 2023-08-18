from fermo_core.data_processing.builder.class_feature_builder import FeatureBuilder
from fermo_core.data_processing.builder.dataclass_feature import Feature


def test_success_feature_builder():
    assert isinstance(FeatureBuilder().set_f_id(1).get_result(), Feature)
