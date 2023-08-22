import pytest

from fermo_core.data_processing.builder_feature.class_feature_builder import (
    FeatureBuilder,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


def test_success_init_feature_builder():
    assert isinstance(
        FeatureBuilder().get_result(), Feature
    ), "Could not initialize the object Feature."


@pytest.mark.parametrize(
    "attr",
    (
        "f_id",
        "mz",
        "rt",
        "rt_start",
        "rt_stop",
        "rt_range",
        "trace",
        "fwhm",
        "intensity",
        "rel_intensity",
        "area",
        "msms",
        "samples",
        "blank",
        "groups",
        "groups_fold",
        "phenotypes",
        "annotations",
        "networks",
        "scores",
    ),
)
def test_success_default_values_for_attributes_feature_builder(attr):
    feature = FeatureBuilder().get_result()
    assert (
        getattr(feature, attr) is None
    ), f"Feature attribute '{attr} is not the default 'None'."


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
