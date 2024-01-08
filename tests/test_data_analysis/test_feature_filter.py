import pytest

from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


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
    assert len(feature_filter_instance.stats.active_features) == 140
    assert len(feature_filter_instance.stats.inactive_features) == 3


def test_filter_features_for_range_valid():
    feature1 = Feature()
    feature1.rel_intensity = 0.1
    feature1.f_id = 1
    feature2 = Feature()
    feature2.rel_intensity = 1
    feature2.f_id = 2
    sample1 = Sample()
    sample1.feature_ids = (1, 2)
    sample1.features = {1: feature1, 2: feature2}
    samples = Repository()
    samples.entries["sample1"] = sample1
    stats = Stats()
    stats.samples = tuple(["sample1"])

    filtered = FeatureFilter.filter_features_for_range(stats, samples, [0.0, 0.5])
    assert filtered == {2}
