import pytest

from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def feature_filter_instance(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return FeatureFilter(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


@pytest.fixture
def dummy_data():
    feature1 = Feature()
    feature1.rel_intensity = 0.1
    feature1.f_id = 1
    feature2 = Feature()
    feature2.rel_intensity = 1
    feature2.f_id = 2
    sample1 = Sample()
    sample1.feature_ids = {1, 2}
    sample1.features = {1: feature1, 2: feature2}
    samples = Repository()
    samples.entries["sample1"] = sample1
    stats = Stats()
    stats.samples = tuple(["sample1"])
    features = Repository()
    features.add(1, feature1)
    features.add(2, feature2)
    return {"stats": stats, "samples": samples, "features": features}


def test_instance_feature_filter_valid(feature_filter_instance):
    assert isinstance(feature_filter_instance, FeatureFilter)


def test_return_values_valid(feature_filter_instance):
    stats, features, samples = feature_filter_instance.return_values()
    assert stats is not None


def test_filter_valid(feature_filter_instance):
    feature_filter_instance.filter()
    assert len(feature_filter_instance.stats.active_features) == 143


def test_filter_rel_int_range_valid(feature_filter_instance):
    feature_filter_instance.filter_rel_int_range()
    assert len(feature_filter_instance.stats.active_features) == 143


def test_filter_rel_area_range_valid(feature_filter_instance):
    feature_filter_instance.filter_rel_area_range()
    assert len(feature_filter_instance.stats.active_features) == 143


def test_filter_rel_int_range_mod_valid(feature_filter_instance):
    feature_filter_instance.params.FeatureFilteringParameters.filter_rel_int_range = [
        0.06,
        1.0,
    ]
    feature_filter_instance.filter_rel_int_range()
    assert len(feature_filter_instance.stats.active_features) == 140
    assert len(feature_filter_instance.stats.inactive_features) == 3


def test_filter_rel_area_range_mod_valid(feature_filter_instance):
    feature_filter_instance.params.FeatureFilteringParameters.filter_rel_area_range = [
        0.06,
        1.0,
    ]
    feature_filter_instance.filter_rel_area_range()
    assert len(feature_filter_instance.stats.active_features) == 104
    assert len(feature_filter_instance.stats.inactive_features) == 39


def test_filter_features_for_range_valid(dummy_data):
    filtered = FeatureFilter.filter_features_for_range(
        dummy_data["stats"], dummy_data["samples"], [0.0, 0.5], "rel_intensity"
    )
    assert filtered == {2}


def test_remove_filtered_features_valid(dummy_data):
    feature_filter = FeatureFilter(
        params=ParameterManager(),
        stats=dummy_data["stats"],
        features=dummy_data["features"],
        samples=dummy_data["samples"],
    )
    feature_filter.stats.inactive_features.add(1)
    feature_filter.remove_filtered_features()
    assert len(feature_filter.features.entries) == 1
    assert feature_filter.samples.entries["sample1"].feature_ids == {2}
    assert feature_filter.samples.entries["sample1"].features.get(1) is None
