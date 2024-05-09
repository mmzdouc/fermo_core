import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    BlankAssignmentParameters,
)


def test_init_blank_assignment_parameters_valid():
    assert isinstance(
        BlankAssignmentParameters(
            activate_module=True, value="area", algorithm="median", factor=10
        ),
        BlankAssignmentParameters,
    )


def test_blank_assignment_parameters_algorithm():
    obj = BlankAssignmentParameters(algorithm="abce")
    assert obj.algorithm == "mean"


def test_blank_assignment_parameters_value():
    obj = BlankAssignmentParameters(value="abce")
    assert obj.value == "area"


def test_init_blank_assignment_parameters_fail():
    with pytest.raises(TypeError):
        BlankAssignmentParameters(None)


def test_to_json_valid():
    obj = BlankAssignmentParameters(activate_module=True)
    assert obj.to_json().get("value") == "area"


def test_to_json_invalid():
    obj = BlankAssignmentParameters()
    assert obj.to_json().get("activate_module") is False
