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


# def test_parse_valid(params_manager):
#     stats, features, samples = GeneralParser().parse(params_manager)
#     assert stats is not None


# def test_parse_peaktable_invalid(params_manager):
#     params_manager.peaktable["format"] = None
#     with pytest.raises(RuntimeError):
#         stats, features, samples = GeneralParser().parse(params_manager)
