import pandas as pd
import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager


def pytest_addoption(parser):
    parser.addoption(
        "--run_slow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--run_high_cpu", action="store_true", default=False, help="run high cpu tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow-running")
    config.addinivalue_line("markers", "high_cpu: mark test as cpu-demanding")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--run_slow"):
        pytest.skip("test requires --run_slow option to run")
    if "high_cpu" in item.keywords and not item.config.getoption("--run_high_cpu"):
        pytest.skip("test requires --run_high_cpu option to run")


@pytest.fixture
def df_mzmine3():
    """Fixture to create Pandas DataFrame object from MZmine3-style table."""
    return pd.read_csv("tests/test_data/test.peak_table_quant_full.csv")


@pytest.fixture
def parameter_instance():
    """Fixture to generate ParameterManager instance from MZmine3 example data."""
    params_json = FileManager.load_json_file("tests/test_data/test.parameters.json")
    params_manager = ParameterManager()
    params_manager.assign_parameters_cli(params_json)
    return params_manager


@pytest.fixture
def general_parser_instance(parameter_instance):
    """Fixture to generate GeneralParser instance from parameter_instance fixture."""
    general_parser = GeneralParser()
    general_parser.parse_parameters(parameter_instance)
    return general_parser


@pytest.fixture
def stats_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return stats


@pytest.fixture
def feature_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return features


@pytest.fixture
def sample_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return samples
