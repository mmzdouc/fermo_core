import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_parameter_manager import ParameterManager


def test_instantiate_class():
    assert isinstance(GeneralParser(), GeneralParser)


@pytest.fixture
def params_manager():
    params_manager = ParameterManager("0.1.0", "my/path/here")
    user_params = params_manager.load_json_file(
        "tests/example_files/example_parameters.json"
    )
    default_params = params_manager.load_json_file(
        "fermo_core/config/default_parameters.json"
    )
    params_manager.parse_parameters(user_params, default_params)
    return params_manager


def test_parse_valid(params_manager):
    stats, features, samples = GeneralParser().parse(params_manager)
    assert stats is not None


def test_parse_peaktable_invalid(params_manager):
    params_manager.peaktable["format"] = None
    with pytest.raises(RuntimeError):
        stats, features, samples = GeneralParser().parse(params_manager)
