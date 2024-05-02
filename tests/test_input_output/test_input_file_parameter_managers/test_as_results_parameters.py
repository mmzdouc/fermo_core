from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import (
    AsResultsParameters,
)


def test_init_ms2query_result_parameters_valid():
    assert isinstance(
        AsResultsParameters(directory_path="example_data/JABTEZ000000000.1"),
        AsResultsParameters,
    )


def test_init_ms2query_result_parameters_invalid():
    with pytest.raises(ValidationError):
        AsResultsParameters()


def test_to_json():
    obj = AsResultsParameters(directory_path="example_data/JABTEZ000000000.1")
    json_dict = obj.to_json()
    assert json_dict.get("directory_path") is not None
