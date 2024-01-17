import pytest

from fermo_core.data_analysis.class_analysis_manager import AnalysisManager


@pytest.fixture
def analysis_manager_instance(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return AnalysisManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


def test_init_valid(analysis_manager_instance):
    assert isinstance(analysis_manager_instance, AnalysisManager)


def test_return_valid(analysis_manager_instance):
    stats, features, samples = analysis_manager_instance.return_attributes()
    assert stats is not None


@pytest.mark.slow
def test_analyze_valid(analysis_manager_instance):
    analysis_manager_instance.analyze()
    value = (
        analysis_manager_instance.samples.get("5440_5439_mod.mzXML")
        .features.get(1)
        .trace_rt
    )
    assert isinstance(value, tuple)
