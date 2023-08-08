from fermo_core.data_processing.builder.class_feature_builder import FeatureBuilder


def test_success_feature_builder():
    feature = FeatureBuilder().set_f_id(1).get_result()
    assert feature.f_id == 1
