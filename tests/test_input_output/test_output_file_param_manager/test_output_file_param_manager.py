from pathlib import Path

from fermo_core.input_output.output_file_parameter_managers import OutputParameters


def test_init_valid():
    assert isinstance(
        OutputParameters(filepath=Path("example_data/")),
        OutputParameters,
    )


def test_format_invalid():
    output = OutputParameters(filepath=Path("dgsdgfsdfgs/"))
    assert output.dir_path.name == "results"
