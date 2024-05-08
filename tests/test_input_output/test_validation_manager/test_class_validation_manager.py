import json
import jsonschema
from pathlib import Path

import pytest

from fermo_core.input_output.class_validation_manager import ValidationManager


def test_init_validation_manager_valid():
    assert isinstance(ValidationManager(), ValidationManager)


def test_validate_mass_deviation_ppm_valid():
    assert ValidationManager.validate_mass_deviation_ppm(10) is None


def test_validate_mass_deviation_ppm_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_mass_deviation_ppm(200)


def test_validate_file_exists_valid():
    assert (
        ValidationManager.validate_file_exists(
            "tests/test_input_output/test_validation_manager/example_peaktable_mzmine3"
            ".csv"
        )
        is None
    )


def test_validate_file_exists_invalid():
    with pytest.raises(FileNotFoundError):
        ValidationManager.validate_file_exists("invalid/file/path")


def test_validate_file_extension_valid():
    assert (
        ValidationManager.validate_file_extension(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_peaktable_mzmine3.csv"
            ),
            ".csv",
        )
        is None
    )


def test_validate_file_extension_invalid():
    with pytest.raises(TypeError):
        ValidationManager.validate_file_extension(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_peaktable_mzmine3.csv"
            ),
            ".mgf",
        )


def test_validate_csv_file_valid():
    assert (
        ValidationManager.validate_csv_file(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_peaktable_mzmine3.csv"
            )
        )
        is None
    )


def test_validate_csv_file_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_csv_file(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "test_class_validation_manager.py"
            )
        )


def test_validate_peaktable_mzmine3_valid():
    assert (
        ValidationManager.validate_peaktable_mzmine3(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_peaktable_mzmine3.csv"
            )
        )
        is None
    )


def test_validate_peaktable_mzmine3_invalid():
    with pytest.raises(KeyError):
        ValidationManager.validate_peaktable_mzmine3(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_group_fermo.csv"
            )
        )


def test_validate_ms2query_results_valid():
    assert (
        ValidationManager.validate_ms2query_results(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_results_ms2query.csv"
            )
        )
        is None
    )


def test_validate_ms2query_results_format_invalid():
    with pytest.raises(KeyError):
        ValidationManager.validate_ms2query_results(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_group_fermo.csv"
            )
        )


def test_validate_csv_has_rows_valid():
    assert (
        ValidationManager.validate_csv_has_rows(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_results_ms2query.csv"
            )
        )
        is None
    )


def test_validate_csv_has_rows_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_csv_has_rows(
            Path("tests/test_input_output/test_validation_manager/" "example_empty.csv")
        )


def test_validate_no_duplicate_entries_valid():
    assert (
        ValidationManager.validate_no_duplicate_entries_csv_column(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_peaktable_mzmine3.csv"
            ),
            "id",
        )
        is None
    )


def test_validate_no_duplicate_entries_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_no_duplicate_entries_csv_column(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_duplicate_entries.csv"
            ),
            "sample_id",
        )


def test_validate_mgf_file_valid():
    assert (
        ValidationManager.validate_mgf_file(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_msms_mgf.mgf"
            )
        )
        is None
    )


def test_validate_mgf_file_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_mgf_file(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_duplicate_entries.csv"
            )
        )


def test_validate_pheno_qualitative_fermo_valid():
    assert (
        ValidationManager.validate_pheno_qualitative_fermo(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_phenotype_qualitative.csv"
            )
        )
        is None
    )


def test_validate_pheno_qualitative_fermo_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_pheno_qualitative_fermo(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_duplicate_entries.csv"
            )
        )


def test_validate_group_metadata_fermo_valid():
    assert (
        ValidationManager.validate_group_metadata_fermo(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_group_fermo.csv"
            )
        )
        is None
    )


def test_validate_group_metadata_fermo_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_group_metadata_fermo(
            Path(
                "tests/test_input_output/test_validation_manager/"
                "example_invalid_group_fermo.csv"
            )
        )


@pytest.mark.parametrize(
    "variable",
    [
        [0.0, 1.0],
        [0.1, 1.0],
        [0.0, 0.7],
    ],
)
def test_validate_range_zero_one_valid(variable):
    assert ValidationManager.validate_range_zero_one(variable) is None


@pytest.mark.parametrize(
    "variable",
    [
        [0.1, 0.5, 1.0],
        [1.0, 2.0],
        [1.0, 0.0],
    ],
)
def test_validate_range_zero_one_invalid(variable):
    with pytest.raises(ValueError):
        ValidationManager.validate_range_zero_one(variable)


def test_validate_file_vs_jsonschema_valid():
    with open(Path("example_data/case_study_parameters.json")) as infile:
        json_dict = json.load(infile)
    assert ValidationManager.validate_file_vs_jsonschema(json_dict, "name") is None


def test_validate_file_vs_jsonschema_invalid():
    with pytest.raises(jsonschema.exceptions.ValidationError):
        ValidationManager.validate_file_vs_jsonschema({"key": "value"}, "name")


def test_validate_output_created_valid():
    assert (
        ValidationManager.validate_output_created(
            Path("example_data/case_study_parameters.json")
        )
        is None
    )


def test_validate_output_created_invalid():
    with pytest.raises(FileNotFoundError):
        ValidationManager().validate_output_created(Path("sadasa/adsasd"))
