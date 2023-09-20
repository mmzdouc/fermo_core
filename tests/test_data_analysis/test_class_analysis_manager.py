import pytest

from fermo_core.data_analysis.class_analysis_manager import AnalysisManager


def test_init_analysis_manager():
    assert isinstance(AnalysisManager(), AnalysisManager)


@pytest.fixture
def analysis_manager():
    return AnalysisManager()
