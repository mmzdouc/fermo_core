import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    PhenotypeAssignmentFoldParameters,
)


def test_init_phenotype_assignment_fold_parameters_valid():
    json_dict = {"activate_module": True, "fold_diff": 10, "data_type": "percentage"}
    assert isinstance(
        PhenotypeAssignmentFoldParameters(**json_dict),
        PhenotypeAssignmentFoldParameters,
    )


def test_init_phenotype_assignment_fold_parameters_fail():
    with pytest.raises(TypeError):
        PhenotypeAssignmentFoldParameters(None)
