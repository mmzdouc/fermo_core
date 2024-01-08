import pandas as pd
import pytest

from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager


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
