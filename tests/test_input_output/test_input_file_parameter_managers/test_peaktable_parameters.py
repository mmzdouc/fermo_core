from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters


def test_init_peaktable_parameters_valid():
    json_dict = {
        "filepath": "example_data/case_study_peak_table_quant_full.csv",
        "format": "mzmine3",
        "polarity": "positive",
    }
    assert isinstance(PeaktableParameters(**json_dict), PeaktableParameters)


def test_init_peaktable_parameters_fail():
    with pytest.raises(ValidationError):
        PeaktableParameters()


def test_init_peaktable_parameters_format_fail():
    json_dict = {
        "filepath": "example_data/case_study_peak_table_quant_full.csv",
        "format": "qwertz",
        "polarity": "positive",
    }
    with pytest.raises(ValueError):
        PeaktableParameters(**json_dict)
