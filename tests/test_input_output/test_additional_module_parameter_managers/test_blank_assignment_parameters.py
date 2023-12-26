import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    BlankAssignmentParameters,
)


def test_init_blank_assignment_parameters_valid():
    json_dict = {
        "activate_module": True,
        "column_ret_fold": 10,
    }
    assert isinstance(BlankAssignmentParameters(**json_dict), BlankAssignmentParameters)


def test_init_blank_assignment_parameters_fail():
    with pytest.raises(TypeError):
        BlankAssignmentParameters(None)
