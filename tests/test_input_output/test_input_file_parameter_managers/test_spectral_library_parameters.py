from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import SpecLibParameters


def test_init_speclib_parameters_valid():
    json_dict = {
        "filepath": "example_data/case_study_spectral_library.mgf",
        "format": "mgf",
    }
    assert isinstance(SpecLibParameters(**json_dict), SpecLibParameters)


def test_init_speclib_parameters_fail():
    with pytest.raises(ValidationError):
        SpecLibParameters()


def test_init_speclib_parameters_format_fail():
    json_dict = {
        "filepath": "example_data/case_study_spectral_library.mgf",
        "format": "qwertz",
    }
    with pytest.raises(ValueError):
        SpecLibParameters(**json_dict)
