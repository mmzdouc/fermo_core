from pathlib import Path

from pydantic import ValidationError
import pytest

from fermo_core.input_output.output_file_parameter_managers import OutputParameters


def test_init_valid():
    assert isinstance(
        OutputParameters(filepath=Path("example_data/fermo.json"), format="json"),
        OutputParameters,
    )


def test_format_invalid():
    with pytest.raises(ValidationError):
        OutputParameters(filepath=Path("example_data/fermo.json"), format="mgf")
