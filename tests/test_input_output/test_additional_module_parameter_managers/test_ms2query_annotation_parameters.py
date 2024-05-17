import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    Ms2QueryAnnotationParameters,
)


def test_init_ms2query_annotation_parameters_valid():
    json_dict = {
        "activate_module": True,
        "score_cutoff": 0.7,
        "maximum_runtime": 600,
    }
    assert isinstance(
        Ms2QueryAnnotationParameters(**json_dict),
        Ms2QueryAnnotationParameters,
    )


def test_init_ms2query_annotation_parameters_fail():
    with pytest.raises(TypeError):
        Ms2QueryAnnotationParameters(None)
