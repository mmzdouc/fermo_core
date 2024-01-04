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


# TODO(MMZ 04.01.24): continue covering methods
