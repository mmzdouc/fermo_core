import pytest
import pandas as pd
from pathlib import Path

from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.dataclass_params_handler import ParamsHandler


def test_success_instantiate_sample_object():
    assert isinstance(Stats(), Stats), "Could not instantiate object 'Sample'."


@pytest.fixture
def stats():
    return Stats()


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


@pytest.fixture
def expected_attributes():
    return (
        "rt_min",
        "rt_max",
        "rt_range",
        "samples",
        "features",
        "groups",
        "cliques",
        "phenotypes",
        "blank",
        "int_removed",
        "annot_removed",
        "ms2_removed",
    )


def test_expected_values_stats(stats, expected_attributes):
    for attr in expected_attributes:
        assert hasattr(stats, attr), f"Attribute '{attr} is missing in class 'Stats'."


def test_unexpected_values_stats(stats, expected_attributes):
    unexpected_attributes = []
    for attr in dir(stats):
        if (
            (not attr.startswith("_"))
            and (attr not in expected_attributes)
            and (not callable(getattr(stats, attr)))
        ):
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in class 'Stats': {unexpected_attributes}."


def test_default_values_stats(stats, expected_attributes):
    for attr in expected_attributes:
        match attr:
            case "groups":
                assert getattr(stats, attr) == {
                    "DEFAULT": set()
                }, "Attribute of class 'Stats' is not 'DEFAULT'."
            case _:
                assert (
                    getattr(stats, attr) is None
                ), f"Attribute '{attr}' of class 'Stats' is not the default 'None'."


def test_assign_value_to_attribute_class_stats(stats):
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
    params = ParamsHandler("0.0.1", Path("no/real/path"))
    params.peaktable_mzmine3 = "tests/example_files/example_peaktable_mzmine3.csv"
    stats.parse_mzmine3(params)
    assert (
        len(stats.features) == 1
    ), "Could not process test file 'example_peaktable_mzmine3.csv' properly."
