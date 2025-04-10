import logging
from datetime import datetime

import pytest

from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_validation_manager import ValidationManager
from fermo_core.main import main

logger = logging.getLogger()


@pytest.mark.slow
def test_mzmine3_integration():
    user_input = FileManager.load_json_file(
        "tests/test_data/mzmine3/mzmine3.9.0.params.json"
    )
    ValidationManager().validate_file_vs_jsonschema(
        user_input, "tests/test_data/mzmine3/mzmine3.9.0.params.json"
    )
    param_manager = ParameterManager()
    param_manager.assign_parameters_cli(user_input)
    main(params=param_manager, starttime=datetime.now(), logger=logger)


@pytest.mark.slow
def test_mzmine4_integration():
    user_input = FileManager.load_json_file(
        "tests/test_data/mzmine4/mzmine4.5.37.params.json"
    )
    ValidationManager().validate_file_vs_jsonschema(
        user_input, "tests/test_data/mzmine4/mzmine4.5.37.params.json"
    )
    param_manager = ParameterManager()
    param_manager.assign_parameters_cli(user_input)
    main(params=param_manager, starttime=datetime.now(), logger=logger)


@pytest.mark.slow
def test_mzmine4_annot_integration():
    user_input = FileManager.load_json_file("tests/test_data/mzmine4_annot/params.json")
    ValidationManager().validate_file_vs_jsonschema(
        user_input, "tests/test_data/mzmine4_annot/params.json"
    )
    param_manager = ParameterManager()
    param_manager.assign_parameters_cli(user_input)
    main(params=param_manager, starttime=datetime.now(), logger=logger)
