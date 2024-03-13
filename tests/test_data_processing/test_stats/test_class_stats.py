import networkx
import numpy as np
import pandas as pd
from pydantic import ValidationError
import pytest

from fermo_core.data_processing.class_stats import Stats, SpecLibEntry, SpecSimNet
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_file_manager import FileManager

from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


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
                "Spectrum": Utils.create_spectrum_object(
                    {
                        "mz": np.array([10, 40, 60], dtype=float),
                        "intens": np.array([10, 20, 100], dtype=float),
                        "f_id": 0,
                        "precursor_mz": 100.0,
                    }
                ),
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
    assert stats.features == 143
    assert len(stats.samples) == 11


def test_init_spec_sim_net_valid():
    entry = SpecSimNet(
        algorithm="xyz",
        network=networkx.Graph(),
        subnetworks={1: networkx.Graph()},
        summary={1: {1, 2, 3}},
    )
    assert isinstance(entry, SpecSimNet)


def test_specsimnet_to_json_valid():
    stats = Stats()
    stats.networks = {
        "xyz": SpecSimNet(
            algorithm="xyz",
            network=networkx.Graph(),
            subnetworks={1: networkx.Graph()},
            summary={1: {1, 2, 3}},
        )
    }
    assert stats.networks["xyz"].to_json() is not None


def test_init_spec_sim_net_invalid():
    with pytest.raises(ValidationError):
        SpecSimNet(mod_cosine=[])


def test_to_json_rt_min_valid():
    stats = Stats()
    stats.rt_min = 0
    json_dict = stats.to_json()
    assert json_dict["rt_min"] == 0.0


def test_to_json_groups_valid():
    stats = Stats()
    json_dict = stats.to_json()
    assert json_dict["groups"] == {"DEFAULT": []}


def test_to_json_networks_valid():
    stats = Stats()
    stats.networks = {
        "xyz": SpecSimNet(
            algorithm="xyz",
            network=networkx.Graph(),
            subnetworks={1: networkx.Graph()},
            summary={1: {1, 2, 3}},
        )
    }
    json_dict = stats.to_json()
    assert json_dict["networks"]["xyz"]["algorithm"] == "xyz"


def test_to_json_phenotypes_valid():
    stats = Stats()
    stats.phenotypes = {"test1": ("a", "b"), "test2": ("a", "c")}
    json_dict = stats.to_json()
    assert json_dict["phenotypes"]["test1"] == ["a", "b"]
