from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import PhenotypeParameters


def test_init_phenotype_parameters_valid():
    json_dict = {
        "filepath": "example_data/case_study_bioactivity_qualitative.csv",
        "format": "qualitative",
    }
    assert isinstance(PhenotypeParameters(**json_dict), PhenotypeParameters)


def test_init_phenotype_parameters_fail():
    with pytest.raises(ValidationError):
        PhenotypeParameters()


def test_init_phenotype_parameters_format_fail():
    json_dict = {
        "filepath": "example_data/case_study_bioactivity.csv",
        "format": "qwertz",
    }
    with pytest.raises(ValueError):
        PhenotypeParameters(**json_dict)
