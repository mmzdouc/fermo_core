from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import (
    GroupMetadataParameters,
)


def test_init_group_metadata_parameters_valid():
    json_dict = {
        "filepath": "example_data/case_study_group_metadata.csv",
        "format": "fermo",
    }
    assert isinstance(GroupMetadataParameters(**json_dict), GroupMetadataParameters)


def test_init_group_metadata_parameters_fail():
    with pytest.raises(ValidationError):
        GroupMetadataParameters()


def test_init_group_metadata_parameters_format_fail():
    json_dict = {
        "filepath": "example_data/case_study_group_metadata.csv",
        "format": "qwertz",
    }
    with pytest.raises(ValueError):
        GroupMetadataParameters(**json_dict)
