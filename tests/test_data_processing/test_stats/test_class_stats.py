import networkx
import pandas as pd
from pydantic import ValidationError
import pytest

from fermo_core.data_processing.class_stats import Stats, SpecLibEntry, SpecSimNet

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_file_manager import FileManager


def test_init_stats_valid():
    assert isinstance(Stats(), Stats)


@pytest.fixture
def stats():
    return Stats()


def test_init_spec_lib_entry_valid():
    assert isinstance(
        SpecLibEntry(
            **{
                "name": "entry1",
                "exact_mass": 123.456,
                "msms": ((100.0, 101.0), (20, 40)),
            }
        ),
        SpecLibEntry,
    )


def test_init_spec_lib_entry_invalid():
    with pytest.raises(ValidationError):
        SpecLibEntry(**{"sda": "Ssdas"})


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


def test_success_parse_mzmine3(stats):
    params = ParameterManager()
    params.assign_parameters_cli(
        FileManager.load_json_file("example_data/case_study_parameters.json")
    )
    stats.parse_mzmine3(params)
    assert len(stats.features) == 143
    assert len(stats.samples) == 11


def test_init_spec_sim_net_valid():
    entry = SpecSimNet(
        algorithm="xyz",
        network=networkx.Graph(),
        subnetworks=[networkx.Graph()],
        summary={1: set([1, 2, 3])},
    )
    assert isinstance(entry, SpecSimNet)


def test_init_spec_sim_net_invalid():
    with pytest.raises(ValidationError):
        SpecSimNet(mod_cosine=[])
