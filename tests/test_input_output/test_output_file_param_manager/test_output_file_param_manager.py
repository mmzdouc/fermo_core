import os
from pathlib import Path

from fermo_core.input_output.output_file_parameter_managers import OutputParameters


def test_init_valid():
    output = OutputParameters(
        directory_path=Path("tests/test_input_output/test_output_file_param_manager/")
    )
    assert output.directory_path.name == "test_output_file_param_manager"
    assert output.directory_path.exists()


def test_format_path_invalid():
    output = OutputParameters(directory_path=Path("dgsdgfsdfgs/"))
    output.validate_output_dir(
        Path("tests/test_input_output/test_output_file_param_manager/")
    )
    assert output.directory_path.name == "results"
    assert output.directory_path.exists()
    os.rmdir("tests/test_input_output/test_output_file_param_manager/results")


def test_format_no_input():
    output = OutputParameters()
    output.validate_output_dir(
        Path("tests/test_input_output/test_output_file_param_manager/")
    )
    assert output.directory_path.name == "results"
    assert output.directory_path.exists()
    os.rmdir("tests/test_input_output/test_output_file_param_manager/results")
