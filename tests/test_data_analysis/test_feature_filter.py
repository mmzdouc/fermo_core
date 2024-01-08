import pytest

from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter


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


def test_filter_rel_int_range_valid(feature_filter_instance):
    feature_filter_instance.filter_rel_int_range()
    assert len(feature_filter_instance.stats.active_features) == 143


def test_filter_rel_int_range_cut_grass_valid(feature_filter_instance):
    feature_filter_instance.params.FeatureFilteringParameters.filter_rel_int_range = [
        0.1,
        1.0,
    ]
    feature_filter_instance.filter_rel_int_range()
    assert len(feature_filter_instance.stats.active_features) == 98
    assert len(feature_filter_instance.stats.inactive_features) == 45
