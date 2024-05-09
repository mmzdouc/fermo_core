import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    GroupFactAssignmentParameters,
)


def test_init_group_fact_assignment_parameters_valid():
    assert isinstance(
        GroupFactAssignmentParameters(
            activate_module=True, value="area", algorithm="median"
        ),
        GroupFactAssignmentParameters,
    )


def test_init_group_fact_assignment_parameters_algorithm():
    obj = GroupFactAssignmentParameters(algorithm="abce")
    assert obj.algorithm == "mean"


def test_init_group_fact_assignment_parameters_value():
    obj = GroupFactAssignmentParameters(value="abce")
    assert obj.value == "area"


def test_init_group_fact_assignment_parameters_fail():
    with pytest.raises(TypeError):
        GroupFactAssignmentParameters(None)


def test_to_json_valid():
    obj = GroupFactAssignmentParameters(activate_module=True)
    assert obj.to_json().get("value") == "area"


def test_to_json_invalid():
    obj = GroupFactAssignmentParameters()
    assert obj.to_json().get("activate_module") is False
