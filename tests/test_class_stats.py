import pytest
import pandas as pd

from fermo_core.data_processing.class_stats import Stats


@pytest.fixture
def stats():
    return Stats()


@pytest.fixture
def dummy_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "datafile:A:feature_state": ["DETECTED", "DETECTED", "DETECTED"],
            "datafile:B:feature_state": ["DETECTED", "DETECTED", "DETECTED"],
            "datafile:A:intensity_range:max": [20, 20, 1000],
            "datafile:B:intensity_range:max": [20, 200, 1000],
        }
    )


def test_success_extract_sample_names_mzmine3(stats, dummy_df):
    assert set(stats._extract_sample_names_mzmine3(dummy_df)) == {"A", "B"}


@pytest.mark.parametrize(
    "range_results",
    [
        [(0.0, 1.0), (1, 2, 3)],
        [(0.1, 1.0), (2, 3)],
        [(0.5, 1.0), tuple([3])],
        [(0.0, 0.2), (1, 2)],
    ],
)
def test_success_get_features_in_range_mzmine3(stats, dummy_df, range_results):
    stats.samples = ("A", "B")
    incl, excl = stats._get_features_in_range_mzmine3(dummy_df, range_results[0])
    assert set(incl) == set(range_results[1])
