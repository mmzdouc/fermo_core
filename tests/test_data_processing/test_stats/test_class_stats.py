import pytest
import pandas as pd

from fermo_core.data_processing.class_stats import Stats, SpecLibEntry

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_file_manager import FileManager


def test_init_stats_valid():
    assert isinstance(Stats(), Stats)


@pytest.fixture
def stats():
    return Stats()


def test_init_spec_lib_entry_valid():
    assert isinstance(
        SpecLibEntry("entry1", 123.456, ((100.0, 101.0), (20, 40))), SpecLibEntry
    )


@pytest.fixture
def spec_lib_entry():
    return SpecLibEntry("entry1", 123.456, ((100.0, 101.0), (20, 40)))


@pytest.fixture
def dummy_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "datafile:sampleA:feature_state": ["DETECTED", "DETECTED", "DETECTED"],
            "datafile:sampleB:feature_state": ["DETECTED", "DETECTED", "DETECTED"],
            "datafile:sampleA:intensity_range:max": [20, 20, 1000],
            "datafile:sampleB:intensity_range:max": [20, 200, 1000],
        }
    )


def test_setattr_stats_valid(stats):
    setattr(stats, "rt_min", float(1.1))
    assert (
        getattr(stats, "rt_min") == 1.1
    ), "Could not assign value to attribute of class 'Stats'."


def test_success_extract_sample_names_mzmine3(stats, dummy_df):
    """Extract 'sampleA' and 'sampleB' from headers of fixture 'dummy_df'."""
    assert set(stats._extract_sample_names_mzmine3(dummy_df)) == {"sampleA", "sampleB"}


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
    stats.samples = ("sampleA", "sampleB")
    incl, excl = stats._get_features_in_range_mzmine3(dummy_df, range_results[0])
    assert set(incl) == set(range_results[1])


def test_success_parse_mzmine3(stats):
    params = ParameterManager()
    params.assign_parameters_cli(
        FileManager.load_json_file("example_data/case_study_parameters.json")
    )
    stats.parse_mzmine3(params)
    assert len(stats.features) == 143
