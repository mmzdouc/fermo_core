import networkx
import pandas as pd
from pydantic import ValidationError
import pytest

from fermo_core.data_processing.class_stats import Stats, SpecSimNet, Group, GroupMData
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_file_manager import FileManager


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


def test_init_stats_valid():
    assert isinstance(Stats(), Stats)


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
    stats.samples = ("s1", "s2")
    stats.GroupMData.default_s_ids = {"s1", "s2"}
    json_dict = stats.to_json()
    assert json_dict["groups"]["default_s_ids"] is not None


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


def test_group_valid():
    group = Group(s_ids={"s1", "s2"}, f_ids={1, 3, 4})
    json_dict = group.to_json()
    assert len(json_dict["s_ids"]) == 2


def test_groupmdata_valid():
    groupmdata = GroupMData(
        default_s_ids={"s1", "s2"},
        ctgrs={"phenotype": {"G": Group(s_ids={"s1", "s2"}, f_ids={1, 3, 4})}},
    )
    json_dict = groupmdata.to_json()
    assert len(json_dict["categories"]["phenotype"]["G"]["s_ids"]) == 2
