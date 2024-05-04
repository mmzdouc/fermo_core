from pathlib import Path

from fermo_core.input_output.output_file_parameter_managers import OutputParameters


def test_init_valid():
    output_params = OutputParameters(directory_path=Path("example_data/"))
    assert output_params.directory_path.name == "example_data"


def test_format_invalid():
    output = OutputParameters(directory_path=Path("dgsdgfsdfgs/"))
    assert output.directory_path.name == "results"
