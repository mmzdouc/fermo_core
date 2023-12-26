import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository


@pytest.fixture
def params_manager():
    params_json = FileManager.load_json_file("example_data/case_study_parameters.json")
    params_manager = ParameterManager()
    params_manager.assign_parameters_cli(params_json)
    return params_manager


@pytest.fixture
def general_parser(params_manager):
    general_parser = GeneralParser()
    general_parser.parse_parameters(params_manager)
    return general_parser


def test_instantiate_class_valid():
    assert isinstance(GeneralParser(), GeneralParser)


def test_return_attributes_valid():
    general_parser = GeneralParser()
    general_parser.stats = Stats()
    general_parser.features = Repository()
    general_parser.samples = Repository()
    stats, features, samples = general_parser.return_attributes()
    assert isinstance(stats, Stats)


def test_return_attributes_invalid():
    general_parser = GeneralParser()
    stats, features, samples = general_parser.return_attributes()
    assert stats is None


def test_parse_parameters_valid(params_manager):
    general_parser = GeneralParser()
    general_parser.parse_parameters(params_manager)
    assert isinstance(general_parser.stats, Stats)


def test_parse_parameters_invalid():
    general_parser = GeneralParser()
    with pytest.raises(TypeError):
        general_parser.parse_parameters()


def test_parse_peaktable_valid(params_manager):
    general_parser = GeneralParser()
    general_parser.parse_peaktable(params_manager)
    assert len(general_parser.stats.features) == 143


def test_parse_peaktable_invalid(params_manager):
    general_parser = GeneralParser()
    with pytest.raises(TypeError):
        general_parser.parse_peaktable()


def test_parse_msms_valid(params_manager, general_parser):
    general_parser.parse_msms(params_manager)
    assert general_parser.features.entries.get(126).msms is not None


def test_parse_msms_invalid(params_manager, general_parser):
    params_manager.MsmsParameters = None
    general_parser.features.entries.get(126).msms = None
    general_parser.parse_msms(params_manager)
    assert general_parser.features.entries.get(126).msms is None


def test_parse_group_metadata_valid(params_manager, general_parser):
    general_parser.parse_group_metadata(params_manager)
    assert len(general_parser.stats.groups.get("DEFAULT")) == 0


def test_parse_group_metadata_invalid(params_manager, general_parser):
    params_manager.GroupMetadataParameters = None
    general_parser.stats.groups = {"DEFAULT": set()}
    general_parser.parse_group_metadata(params_manager)
    assert general_parser.stats.groups == {"DEFAULT": set()}


def test_parse_phenotype_valid(params_manager, general_parser):
    general_parser.parse_phenotype(params_manager)
    assert len(general_parser.stats.phenotypes.get("quant_data")) == 4


def test_parse_phenotype_invalid(params_manager, general_parser):
    params_manager.PhenotypeParameters = None
    general_parser.stats.phenotypes = None
    general_parser.parse_phenotype(params_manager)
    assert general_parser.stats.phenotypes is None


def test_parse_spectral_library_valid(params_manager, general_parser):
    general_parser.parse_spectral_library(params_manager)
    assert general_parser.stats.spectral_library is not None


def test_parse_spectral_library_invalid(params_manager, general_parser):
    params_manager.SpecLibParameters = None
    general_parser.stats.spectral_library = None
    general_parser.parse_spectral_library(params_manager)
    assert general_parser.stats.spectral_library is None
