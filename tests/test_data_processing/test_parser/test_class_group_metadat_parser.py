import pytest

from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.parser.class_group_metadata_parser import (
    GroupMetadataParser,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


def test_instantiate_parser_valid():
    group_parser = GroupMetadataParser(
        "tests/example_files/example_group_fermo.csv",
        "fermo",
    )
    assert isinstance(group_parser, GroupMetadataParser)


@pytest.fixture
def group_parser():
    return GroupMetadataParser(
        "tests/example_files/example_group_fermo.csv",
        "fermo",
    )


@pytest.fixture
def sample_repo():
    repository = Repository()
    sample1 = Sample()
    sample1.s_id = "sample1"
    repository.add("sample1", sample1)
    sample2 = Sample()
    sample2.s_id = "sample2"
    repository.add("sample2", sample2)
    return repository


@pytest.fixture
def stats_obj():
    stats_obj = Stats(polarity="positive")
    stats_obj.groups.get("DEFAULT").add("sample1")
    stats_obj.groups.get("DEFAULT").add("sample2")
    return stats_obj


def test_parse_valid(group_parser, stats_obj, sample_repo):
    stats_obj, sample_repo = group_parser.parse(stats_obj, sample_repo)
    assert len(stats_obj.groups.get("DEFAULT")) == 0
    assert sample_repo.entries.get("sample1").groups == {"groupA", "medium1"}


def test_parse_invalid(stats_obj, sample_repo):
    group_parser = GroupMetadataParser("", "")
    stats_obj, sample_repo = group_parser.parse(stats_obj, sample_repo)
    assert len(stats_obj.groups.get("DEFAULT")) != 0
    assert sample_repo.entries.get("sample1").groups == {"DEFAULT"}


def test_parse_fermo_valid(group_parser, stats_obj, sample_repo):
    stats_obj, sample_repo = group_parser.parse(stats_obj, sample_repo)
    assert len(stats_obj.groups.get("DEFAULT")) == 0
    assert sample_repo.entries.get("sample1").groups == {"groupA", "medium1"}


def test_remove_sample_id_from_group_default_valid(stats_obj, group_parser):
    stats_obj = group_parser.remove_sample_id_from_group_default(stats_obj, "sample1")
    assert "sample1" not in stats_obj.groups.get("DEFAULT")


def test_remove_sample_id_from_group_default_invalid(stats_obj, group_parser):
    stats_obj = group_parser.remove_sample_id_from_group_default(stats_obj, "sample3")
    assert stats_obj.groups.get("DEFAULT") == {"sample1", "sample2"}


def test_add_group_id_to_sample_repo_valid(group_parser, sample_repo):
    sample_repo = group_parser.add_group_id_to_sample_repo(
        sample_repo, "sample1", "groupA"
    )
    assert sample_repo.get("sample1").groups == {"groupA"}


def test_add_group_id_to_sample_repo_invalid(group_parser, sample_repo):
    sample_repo = group_parser.add_group_id_to_sample_repo(
        sample_repo, "sample3", "groupA"
    )
    assert isinstance(sample_repo, Repository)  # Checks error handling
