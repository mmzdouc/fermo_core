from pydantic import ValidationError
import pytest

from fermo_core.input_output.input_file_parameter_managers import (
    MS2QueryResultsParameters,
)


def test_init_ms2query_result_parameters_valid():
    assert isinstance(
        MS2QueryResultsParameters(
            filepath=(
                "tests/test_input_output/"
                "test_validation_manager/example_results_ms2query.csv"
            ),
            score_cutoff=0.7,
        ),
        MS2QueryResultsParameters,
    )


def test_init_ms2query_result_parameters_invalid():
    with pytest.raises(ValidationError):
        MS2QueryResultsParameters()
