from pathlib import Path

import pandas as pd
import pytest
from fermo_core.input_output.class_validation_handler import ValidationHandler


@pytest.fixture
def validation_handler():
    return ValidationHandler()


@pytest.mark.parametrize(
    "b",
    [
        True,
        False,
    ],
)
def test_success_validate_bool(b):
    result = ValidationHandler.validate_bool(b)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "b",
    [
        "True",
        "False",
        "",
        1,
        None,
    ],
)
def test_fail_validate_bool(b):
    result = ValidationHandler.validate_bool(b)
    assert not result[0], result[1]


def test_success_validate_string():
    result = ValidationHandler.validate_string("fermo_core/main.py")
    assert result[0], result[1]


def test_fail_validate_string():
    result = ValidationHandler.validate_string(1)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "i",
    [
        1,
        0,
    ],
)
def test_success_validate_pos_int_or_zero(i):
    result = ValidationHandler.validate_pos_int_or_zero(i)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "i",
    [
        -1,
        "string",
        1.0,
        -1.0,
        [1],
        (1, 1),
    ],
)
def test_fail_validate_pos_int_or_zero(i):
    result = ValidationHandler.validate_pos_int_or_zero(i)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "i",
    [
        1,
        100,
    ],
)
def test_success_validate_pos_int(i):
    result = ValidationHandler.validate_pos_int(i)
    assert result[0], result[1]


@pytest.mark.parametrize("i", [-1, 0, 1.0, -1.0, "string"])
def test_fail_validate_pos_int(i):
    result = ValidationHandler.validate_pos_int(i)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "mass_dev_ppm",
    [
        10,
        100,
        1,
    ],
)
def test_success_validate_mass_dev_ppm(validation_handler, mass_dev_ppm):
    result = validation_handler.validate_mass_dev_ppm(mass_dev_ppm)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "mass_dev_ppm",
    [
        "string",
        -1,
        0,
        150,
    ],
)
def test_fail_validate_mass_dev_ppm(validation_handler, mass_dev_ppm):
    result = validation_handler.validate_mass_dev_ppm(mass_dev_ppm)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "f",
    [
        0.0,
        0.5,
        1.0,
    ],
)
def test_success_validate_float_zero_one(f):
    result = ValidationHandler.validate_float_zero_one(f)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "f",
    [
        -1.0,
        1.5,
    ],
)
def test_fail_validate_float_zero_one(f):
    result = ValidationHandler.validate_float_zero_one(f)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "alg",
    [
        "all",
        "modified_cosine",
        "ms2deepscore",
    ],
)
def test_success_validate_spectral_sim_network_alg(validation_handler, alg):
    result = validation_handler.validate_spectral_sim_network_alg(alg)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "alg",
    [
        "",
        "nonexisting",
        "ms2deeps",
        [],
        ["all"],
    ],
)
def test_fail_validate_spectral_sim_network_alg(validation_handler, alg):
    result = validation_handler.validate_spectral_sim_network_alg(alg)
    assert not result[0], result[1]


@pytest.mark.parametrize(
    "r",
    [
        (0.0, 1.0),
        (0.5, 1.0),
        (0.5, 0.6),
    ],
)
def test_success_validate_range_zero_one(r):
    result = ValidationHandler.validate_range_zero_one(r)
    assert result[0], result[1]


@pytest.mark.parametrize(
    "r",
    [
        (0, 1),
        (0, 1, 2),
        (0.0, 1),
        (0.0, 2.0),
        (-0.1, 1.0),
        (1.0, 0.0),
    ],
)
def test_fail_validate_range_zero_one(r):
    result = ValidationHandler.validate_range_zero_one(r)
    assert not result[0], result[1]


def test_success_validate_file_exists():
    result = ValidationHandler.validate_file_exists(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )
    assert result[0], result[1]


def test_fail_validate_file_exists():
    result = ValidationHandler.validate_file_exists(Path("file/which/does/not/exist"))
    assert not result[0], result[1]


def test_success_validate_csv_file(validation_handler):
    result = validation_handler.validate_csv_file(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )
    assert result[0], result[1]


def test_fail_validate_csv_file(validation_handler):
    result = validation_handler.validate_csv_file(
        Path("tests/example_files/example_invalid_csv.md")
    )
    assert not result[0], result[1]


def test_success_validate_csv_duplicate_col_entries():
    result = ValidationHandler.validate_csv_duplicate_col_entries(
        pd.DataFrame({"id": [1, 2]}), "id"
    )
    assert result[0], result[1]


def test_fail_validate_csv_duplicate_col_entries():
    result = ValidationHandler.validate_csv_duplicate_col_entries(
        pd.DataFrame({"id": [1, 1]}), "id"
    )
    assert not result[0], result[1]


def test_success_validate_peaktable_mzmine3(validation_handler):
    result = validation_handler.validate_peaktable_mzmine3(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )
    assert result[0], result[1]


def test_fail_validate_peaktable_mzmine3(validation_handler):
    result = validation_handler.validate_peaktable_mzmine3(
        Path("tests/example_files/example_group_fermo.csv")
    )
    assert not result[0], result[1]


def test_success_validate_mgf(validation_handler):
    result = validation_handler.validate_mgf(
        Path("tests/example_files/example_msms_mgf.mgf")
    )
    assert result[0], result[1]


def test_fail_validate_mgf(validation_handler):
    result = validation_handler.validate_mgf(
        Path("tests/example_files/example_invalid_csv.md")
    )
    assert not result[0], result[1]


def test_success_validate_file_ending():
    result = ValidationHandler.validate_file_ending(
        Path("../example_files/example_phenotype_fermo.csv"), ".csv"
    )
    assert result[0], result[1]


def test_fail_validate_file_ending():
    result = ValidationHandler.validate_file_ending(
        Path("../example_files/example_phenotype_fermo.csv"), ".mgf"
    )
    assert not result[0], result[1]


def test_success_validate_path():
    result = ValidationHandler.validate_path(
        "example_files/example_phenotype_fermo.csv"
    )
    assert result[0], result[1]


@pytest.mark.parametrize("s", [None, 22, ["percentage", "concentration"]])
def test_fail_validate_path(s):
    result = ValidationHandler.validate_path(s)
    assert not result[0], result[1]


def test_success_validate_phenotype_fermo(validation_handler):
    result = validation_handler.validate_phenotype_fermo(
        Path("tests/example_files/example_phenotype_fermo.csv"),
        "percentage",
    )
    assert result[0], result[1]


def test_fail_validate_phenotype_fermo(validation_handler):
    result = validation_handler.validate_phenotype_fermo(
        Path("tests/example_files/example_msms_mgf.mgf"),
        "percentage",
    )
    assert not result[0], result[1]


def test_success_validate_group_fermo(validation_handler):
    result = validation_handler.validate_group_fermo(
        Path("tests/example_files/example_group_fermo.csv")
    )
    assert result[0], result[1]


def test_fail_validate_group_fermo(validation_handler):
    result = validation_handler.validate_group_fermo(
        Path("tests/example_files/example_msms_mgf.mgf")
    )
    assert not result[0], result[1]
