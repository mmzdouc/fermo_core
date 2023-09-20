import pytest

from fermo_core.data_processing.parser.class_phenotype_parser import PhenotypeParser
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample, Phenotype
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


def test_instantiate_parser_valid():
    phenotype_parser = PhenotypeParser(
        "tests/example_files/example_phenotype_fermo.csv",
        "fermo",
    )
    assert isinstance(phenotype_parser, PhenotypeParser)


@pytest.fixture
def phenotype_parser():
    return PhenotypeParser(
        "tests/example_files/example_phenotype_fermo.csv",
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
    sample3 = Sample()
    sample3.s_id = "sample3"
    repository.add("sample3", sample3)
    return repository


@pytest.fixture
def stats():
    return Stats(polarity="positive")


def test_parse_valid(stats, sample_repo, phenotype_parser):
    stats, sample_repo = phenotype_parser.parse(stats, sample_repo)
    assert stats.phenotypes is not None


def test_parse_invalid(stats, sample_repo, phenotype_parser):
    phenotype_parser.phenotype_format = ""
    stats, sample_repo = phenotype_parser.parse(stats, sample_repo)
    assert isinstance(stats, Stats)
    assert stats.phenotypes is None


def test_parse_fermo_valid(stats, sample_repo, phenotype_parser):
    stats, sample_repo = phenotype_parser.parse_fermo(stats, sample_repo)
    assert stats.phenotypes.get("quant_data1") == ("sample1", "sample2")
    assert stats.phenotypes.get("quant_data2") == ("sample1", "sample2", "sample3")
    assert sample_repo.entries["sample1"].phenotypes is not None
    assert sample_repo.entries["sample1"].phenotypes["quant_data1"].value == 8.0
    assert sample_repo.entries["sample1"].phenotypes["quant_data2"].value == 2


def test_add_phenotype_to_sample_valid(phenotype_parser, sample_repo):
    sample_repo = phenotype_parser.add_phenotype_to_sample(
        sample_repo, "sample1", "quant_data1", 8.0, 1
    )
    assert isinstance(
        sample_repo.entries.get("sample1").phenotypes.get("quant_data1"), Phenotype
    )
    assert sample_repo.entries["sample1"].phenotypes["quant_data1"].value == 8.0
    assert sample_repo.entries["sample1"].phenotypes["quant_data1"].concentration == 1


def test_add_phenotype_to_sample_invalid(phenotype_parser, sample_repo):
    sample_repo = phenotype_parser.add_phenotype_to_sample(
        sample_repo, "nonexisting_sample", "quant_data1", 8.0, 1
    )
    with pytest.raises(KeyError):
        sample_repo.get("nonexisting_sample")
