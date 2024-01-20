import pandas as pd
import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def df_mzmine3():
    """Fixture to create Pandas DataFrame object from MZmine3-style table."""
    return pd.read_csv("example_data/case_study_peak_table_quant_full.csv")


@pytest.fixture
def parameter_instance():
    """Fixture to generate ParameterManager instance from MZmine3 example data."""
    params_json = FileManager.load_json_file("example_data/case_study_parameters.json")
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
