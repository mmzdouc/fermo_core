import pytest

from fermo_core.data_processing.parser.group_metadata_parser.class_fermo_metadata_parser import (
    MetadataFermoParser,
)
from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import (
    PeaktableParameters,
    GroupMetadataParameters,
)


@pytest.fixture
def params():
    params = ParameterManager()
    params.PeaktableParameters = PeaktableParameters(
        **{
            "filepath": "example_data/case_study_peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    params.GroupMetadataParameters = GroupMetadataParameters(
        **{"filepath": "example_data/case_study_group_metadata.csv", "format": "fermo"}
    )
    return params


@pytest.fixture
def stats(params):
    return PeakMzmine3Parser().extract_stats(params)


@pytest.fixture
def sample_repo(params, stats):
    return PeakMzmine3Parser().extract_samples(stats, params)


def test_instantiate_parser_valid():
    assert isinstance(MetadataFermoParser(), MetadataFermoParser)


def test_parse_valid(stats, sample_repo, params):
    stats, sample_repo = MetadataFermoParser().parse(stats, sample_repo, params)
    assert len(stats.groups.get("DEFAULT")) == 0
    assert len(stats.groups) == 6


def test_remove_sample_id_from_group_default_valid(stats):
    stats = MetadataFermoParser.remove_sample_id_from_group_default(
        stats, "5425_5426_mod.mzXML"
    )
    assert "5425_5426_mod.mzXML" not in stats.groups.get("DEFAULT")


def test_remove_sample_id_from_group_default_invalid(stats):
    stats = MetadataFermoParser.remove_sample_id_from_group_default(stats, "sample1")
    assert len(stats.groups.get("DEFAULT")) == 11


def test_add_group_id_to_sample_repo_valid(sample_repo):
    sample_repo = MetadataFermoParser.add_group_id_to_sample_repo(
        sample_repo, "5425_5426_mod.mzXML", "groupA"
    )
    assert sample_repo.get("5425_5426_mod.mzXML").groups == {"groupA"}
