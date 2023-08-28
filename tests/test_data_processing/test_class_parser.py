import pytest
import pandas as pd
from pathlib import Path
from fermo_core.data_processing.class_parser import Parser
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def df_group_fermo():
    return pd.DataFrame(
        {
            "sample_name": ["sample1"],
            "attr1": ["group1"],
            "attr2": ["group2"],
        }
    )


@pytest.fixture
def sample_repo():
    sample_repo = Repository()
    sample_repo.add("sample1", Sample())
    return sample_repo


@pytest.fixture
def stats():
    stats = Stats()
    stats.groups["DEFAULT"].add("sample1")
    return stats


def test_instantiate_parser():
    assert isinstance(Parser(), Parser), "Could not instantiate class 'Parser'."


def test_parse_group_fermo(df_group_fermo, sample_repo, stats):
    stats, sample_repo = Parser.parse_group_fermo(df_group_fermo, stats, sample_repo)
    assert (
        "sample1" not in stats.groups["DEFAULT"]
    ), "Could not remove 'sample1' from 'Stats'."
    assert "sample1" in stats.groups["group1"], "Could not add 'sample1' to 'group1'."
    assert (
        "DEFAULT" not in sample_repo.entries["sample1"].groups
    ), "Could not remove 'DEFAULT' from set in 'sample.groups'."
    assert (
        "group1" in sample_repo.entries["sample1"].groups
    ), "Could not add 'group1' to set in 'sample.groups'."


def test_parse_msms_mgf():
    feature = Feature()
    feature.f_id = 1
    feature_repo = Repository()
    feature_repo.add(1, feature)
    feature_repo = Parser.parse_msms_mgf(
        Path("tests/example_files/example_msms_mgf.mgf"), feature_repo
    )
    assert (
        feature_repo.entries[1].msms is not None
    ), "Could not assign MS/MS data to feature id '1'."
