import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    PhenoQuantAssgnParams,
)


def test_json_export_valid():
    dict_in = {
        "activate_module": True,
        "factor": 10,
        "algorithm": "minmax",
        "value": "area",
    }
    obj = PhenoQuantAssgnParams(**dict_in)
    dict_out = obj.to_json()
    assert dict_out == dict_in


def test_json_export_invalid():
    obj = PhenoQuantAssgnParams()
    dict_out = obj.to_json()
    assert dict_out["activate_module"] is False
    assert dict_out.get("factor") is None


def test_init_invalid_none():
    with pytest.raises(TypeError):
        PhenoQuantAssgnParams(None)


def test_init_invalid_alg():
    obj = PhenoQuantAssgnParams(algorithm="asfasdfa")
    assert obj.algorithm == "minmax"


def test_init_invalid_value():
    obj = PhenoQuantAssgnParams(value="asfasdfa")
    assert obj.value == "area"
