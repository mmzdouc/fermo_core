from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import MsmsParameters


def test_init_msms_parameters_valid():
    json_dict = {
        "filepath": "example_data/case_study_MSMS.mgf",
        "format": "mgf",
        "rel_int_from": 0.005,
    }
    assert isinstance(MsmsParameters(**json_dict), MsmsParameters)


def test_init_msms_parameters_fail():
    with pytest.raises(ValidationError):
        MsmsParameters()


def test_init_msms_parameters_format_fail():
    json_dict = {
        "filepath": "example_data/case_study_MSMS.mgf",
        "format": "qwertz",
        "rel_int_from": 0.005,
    }
    with pytest.raises(ValueError):
        MsmsParameters(**json_dict)


def test_init_msms_parameters_rel_int_from_fail():
    json_dict = {
        "filepath": "example_data/case_study_MSMS.mgf",
        "format": "mgf",
        "rel_int_from": 10.0,
    }
    with pytest.raises(ValueError):
        MsmsParameters(**json_dict)
