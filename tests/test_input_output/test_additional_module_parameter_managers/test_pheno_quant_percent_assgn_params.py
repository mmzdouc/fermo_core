import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    PhenoQuantPercentAssgnParams,
)


def test_json_export_valid():
    dict_in = {
        "activate_module": True,
        "sample_avg": "mean",
        "value": "area",
        "algorithm": "pearson",
        "p_val_cutoff": 0.05,
        "coeff_cutoff": 0.7,
        "module_passed": True,
    }
    obj = PhenoQuantPercentAssgnParams(**dict_in)
    dict_out = obj.to_json()
    assert dict_out == dict_in


def test_json_export_invalid():
    obj = PhenoQuantPercentAssgnParams()
    dict_out = obj.to_json()
    assert dict_out["activate_module"] is False
    assert dict_out.get("sample_avg") is None


def test_init_invalid_none():
    with pytest.raises(TypeError):
        PhenoQuantPercentAssgnParams(None)


def test_init_invalid_sample_avg():
    obj = PhenoQuantPercentAssgnParams(sample_avg="asfasdfa")
    assert obj.sample_avg == "mean"


def test_init_invalid_value():
    obj = PhenoQuantPercentAssgnParams(value="asfasdfa")
    assert obj.value == "area"


def test_init_invalid_algorithm():
    obj = PhenoQuantPercentAssgnParams(algorithm="asfasdfa")
    assert obj.algorithm == "pearson"


def test_init_invalid_p_val_cutoff():
    obj = PhenoQuantPercentAssgnParams(p_val_cutoff=5.0)
    assert obj.p_val_cutoff == 0.05


def test_init_invalid_coeff_cutoff():
    obj = PhenoQuantPercentAssgnParams(coeff_cutoff=5.0)
    assert obj.coeff_cutoff == 0.7
