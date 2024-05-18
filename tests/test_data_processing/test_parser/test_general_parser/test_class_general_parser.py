import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository


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


def test_parse_parameters_valid(parameter_instance):
    general_parser = GeneralParser()
    general_parser.parse_parameters(parameter_instance)
    assert isinstance(general_parser.stats, Stats)


def test_parse_parameters_invalid():
    general_parser = GeneralParser()
    with pytest.raises(TypeError):
        general_parser.parse_parameters()


def test_parse_peaktable_valid(parameter_instance):
    general_parser = GeneralParser()
    general_parser.parse_peaktable(parameter_instance)
    assert general_parser.stats.features == 143


def test_parse_peaktable_invalid(parameter_instance):
    general_parser = GeneralParser()
    with pytest.raises(TypeError):
        general_parser.parse_peaktable()


def test_parse_msms_valid(parameter_instance, general_parser_instance):
    general_parser_instance.parse_msms(parameter_instance)
    assert general_parser_instance.features.entries.get(126).Spectrum is not None


def test_parse_msms_invalid(parameter_instance, general_parser_instance):
    parameter_instance.MsmsParameters = None
    general_parser_instance.features.entries.get(126).Spectrum = None
    general_parser_instance.parse_msms(parameter_instance)
    assert general_parser_instance.features.entries.get(126).Spectrum is None


def test_parse_group_metadata_valid(parameter_instance, general_parser_instance):
    general_parser_instance.parse_group_metadata(parameter_instance)
    assert len(general_parser_instance.stats.GroupMData.ctgrs) == 2


def test_parse_group_metadata_invalid(parameter_instance, general_parser_instance):
    parameter_instance.GroupMetadataParameters = None
    general_parser_instance.parse_group_metadata(parameter_instance)
    assert len(general_parser_instance.stats.GroupMData.default_s_ids) == 0


def test_parse_phenotype_valid(parameter_instance, general_parser_instance):
    general_parser_instance.parse_phenotype(parameter_instance)
    assert len(general_parser_instance.stats.phenotypes[0].s_negative) == 7


def test_parse_phenotype_invalid(parameter_instance, general_parser_instance):
    parameter_instance.PhenotypeParameters = None
    general_parser_instance.stats.phenotypes = None
    general_parser_instance.parse_phenotype(parameter_instance)
    assert general_parser_instance.stats.phenotypes is None


def test_parse_spectral_library_valid(parameter_instance, general_parser_instance):
    general_parser_instance.parse_spectral_library(parameter_instance)
    assert general_parser_instance.stats.spectral_library is not None


def test_parse_spectral_library_invalid(parameter_instance, general_parser_instance):
    parameter_instance.SpecLibParameters = None
    general_parser_instance.stats.spectral_library = None
    general_parser_instance.parse_spectral_library(parameter_instance)
    assert general_parser_instance.stats.spectral_library is None
