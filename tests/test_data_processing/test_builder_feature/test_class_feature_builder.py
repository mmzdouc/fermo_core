import pytest

from fermo_core.data_processing.builder_feature.class_feature_builder import (
    FeatureBuilder,
)


def test_success_set_attributes_feature_builder():
    feature = FeatureBuilder().set_f_id(10).get_result()
    assert feature.f_id == 10, "Builder could not set value when building object."


def test_success_assign_new_attributes_feature_builder():
    feature = FeatureBuilder().set_f_id(10).get_result()
    feature.f_id = 5
    assert feature.f_id == 5, "Could not assign new value to Feature."


def test_fail_init_with_invalid_values_feature_builder():
    with pytest.raises(ValueError):
        FeatureBuilder().set_f_id("10")


def test_success_init_multiple_instances_feature_builder():
    feature1 = FeatureBuilder().set_f_id(1).get_result()
    feature2 = FeatureBuilder().set_f_id(2).get_result()
    assert feature1.f_id != feature2.f_id, (
        "Could not build multiple instances with different attributes using the same "
        "builder."
    )


def test_type_testing_valid():
    assert FeatureBuilder.type_testing(1, int) is None


def test_type_testing_invalid():
    with pytest.raises(ValueError):
        FeatureBuilder.type_testing(1, str)
