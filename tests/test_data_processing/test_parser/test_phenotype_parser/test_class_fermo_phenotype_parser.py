import pytest

from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.data_processing.parser.phenotype_parser.class_fermo_phenotype_parser import (
    PhenotypeFermoParser,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Phenotype
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import (
    PeaktableParameters,
    PhenotypeParameters,
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
    params.PhenotypeParameters = PhenotypeParameters(
        **{"filepath": "example_data/case_study_bioactivity.csv", "format": "fermo"}
    )
    return params


@pytest.fixture
def stats(params):
    return PeakMzmine3Parser().extract_stats(params)


@pytest.fixture
def sample_repo(stats, params):
    return PeakMzmine3Parser().extract_samples(stats, params)


def test_instantiate_parser_valid():
    assert isinstance(PhenotypeFermoParser(), PhenotypeFermoParser)


def test_parse_valid(stats, sample_repo, params):
    stats, sample_repo = PhenotypeFermoParser().parse(stats, sample_repo, params)
    assert stats.phenotypes is not None


def test_add_phenotype_to_sample_valid(sample_repo):
    sample_repo = PhenotypeFermoParser().add_phenotype_to_sample(
        sample_repo, "5434_5433_mod.mzXML", "bacillus", 10, 1
    )
    assert isinstance(
        sample_repo.entries.get("5434_5433_mod.mzXML").phenotypes.get("bacillus"),
        Phenotype,
    )

    assert (
        sample_repo.entries.get("5434_5433_mod.mzXML").phenotypes.get("bacillus").value
        == 10
    )

    assert (
        sample_repo.entries.get("5434_5433_mod.mzXML")
        .phenotypes.get("bacillus")
        .concentration
        == 1
    )
