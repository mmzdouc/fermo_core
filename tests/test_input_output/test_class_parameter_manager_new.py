import pytest


from pydantic import ValidationError

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.core_module_parameter_managers import (
    AdductAnnotationParameters,
)


def test_init_parameter_manager_valid():
    assert isinstance(ParameterManager(), ParameterManager)


def test_parameter_manager_properties_valid():
    params = ParameterManager()
    assert params.PeaktableParameters is None
    assert isinstance(params.AdductAnnotationParameters, AdductAnnotationParameters)


def test_assign_peaktable_valid():
    params = ParameterManager()
    params.assign_peaktable(
        {
            "filepath": "example_data/case_study_peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )


def test_assign_peaktable_invalid():
    params = ParameterManager()
    with pytest.raises(ValidationError):
        params.assign_peaktable(
            {
                "filepath": "example_data/case_study_peak_table_quant_full.csv",
            }
        )


def test_assign_msms_valid():
    params = ParameterManager()
    params.assign_msms(
        {"filepath": "example_data/case_study_MSMS.mgf", "format": "mgf"}
    )


def test_assign_msms_invalid():
    params = ParameterManager()
    params.assign_msms(
        {
            "filepath": "example_data/case_study_MSMS.mgf",
        }
    )
    assert params.MsmsParameters is None
