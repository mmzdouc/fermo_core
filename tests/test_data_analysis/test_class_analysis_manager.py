import pytest

from fermo_core.data_analysis.class_analysis_manager import AnalysisManager
from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager


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


def test_init_analysis_manager():
    assert isinstance(AnalysisManager(), AnalysisManager)


def test_analyze_valid(params_manager, general_parser):
    stats, features, samples = general_parser.return_attributes()
    stats, features, samples = AnalysisManager().analyze(
        params_manager, stats, features, samples
    )
    assert (
        samples.entries.get("5440_5439_mod.mzXML").features.get(1).trace_rt is not None
    )
