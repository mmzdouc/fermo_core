import pytest

from fermo_core.input_output.class_validation_manager import ValidationManager


def test_validation_manager_creation():
    assert isinstance(ValidationManager(), ValidationManager)


@pytest.mark.parametrize(
    "variable",
    [
        "testing",
        "your/filepath/here.py",
    ],
)
def test_validate_string_valid(variable):
    assert ValidationManager.validate_string(variable) is None


@pytest.mark.parametrize(
    "variable",
    ["", 22, True],
)
def test_validate_string_invalid(variable):
    with pytest.raises(TypeError):
        ValidationManager.validate_string(variable)


def test_validate_string_no_exception_valid_input():
    try:
        ValidationManager.validate_string("your/filepath/here")
    except TypeError:
        pytest.fail("Validation raised an exception for valid input")


@pytest.mark.parametrize(
    "variable",
    [
        True,
        False,
    ],
)
def test_validate_bool_valid(variable):
    assert ValidationManager.validate_bool(variable) is None


@pytest.mark.parametrize(
    "variable",
    [
        None,
        "True",
    ],
)
def test_validate_bool_invalid(variable):
    with pytest.raises(TypeError):
        ValidationManager.validate_bool(variable)


def test_validate_bool_no_exception_valid_input():
    try:
        ValidationManager.validate_bool(True)
    except TypeError:
        pytest.fail("Validation raised an exception for valid input")


@pytest.mark.parametrize(
    "variable",
    [-1, 0, 1],
)
def test_validate_integer_valid(variable):
    assert ValidationManager.validate_integer(variable) is None


@pytest.mark.parametrize(
    "variable",
    [-0.1, 0.0, 1.0],
)
def test_validate_integer_invalid(variable):
    with pytest.raises(TypeError):
        ValidationManager.validate_integer(variable)


def test_validate_integer_no_exception_valid_input():
    try:
        ValidationManager.validate_integer(1)
    except TypeError:
        pytest.fail("Validation raised an exception for valid input")


@pytest.mark.parametrize(
    "variable",
    [-0.1, 0.0, 1.0],
)
def test_validate_float_valid(variable):
    assert ValidationManager.validate_float(variable) is None


@pytest.mark.parametrize(
    "variable",
    [-1, 0, 1],
)
def test_validate_float_invalid(variable):
    with pytest.raises(TypeError):
        ValidationManager.validate_float(variable)


def test_validate_float_no_exception_valid_input():
    try:
        ValidationManager.validate_float(1.0)
    except TypeError:
        pytest.fail("Validation raised an exception for valid input")


@pytest.mark.parametrize(
    "variable",
    [0.1, 1.0, 10],
)
def test_validate_positive_number_valid(variable):
    assert ValidationManager.validate_positive_number(variable) is None


@pytest.mark.parametrize(
    "variable",
    [-1, -0.1, 0.0, 0],
)
def test_validate_positive_number_invalid(variable):
    with pytest.raises(ValueError):
        ValidationManager.validate_positive_number(variable)


def test_validate_positive_number_no_exception_valid_input():
    try:
        ValidationManager.validate_positive_number(1.0)
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_mass_deviation_ppm_valid():
    assert ValidationManager.validate_mass_deviation_ppm(10) is None


def test_validate_mass_deviation_ppm_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_mass_deviation_ppm(200)


def test_validate_mass_deviation_ppm_no_exception_valid_input():
    try:
        ValidationManager.validate_positive_number(10)
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_file_exists_valid():
    assert (
        ValidationManager.validate_file_exists(
            "tests/example_files/example_peaktable_mzmine3.csv"
        )
        is None
    )


@pytest.mark.parametrize(
    "variable",
    [
        "1",
        "file/which/does/not/exist.py",
    ],
)
def test_validate_file_exists_invalid(variable):
    with pytest.raises(FileNotFoundError):
        ValidationManager.validate_file_exists(variable)


def test_validate_file_exists_no_exception_valid_input():
    try:
        ValidationManager.validate_file_exists(
            "tests/example_files/example_peaktable_mzmine3.csv"
        )
    except FileNotFoundError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_file_extension_valid():
    assert (
        ValidationManager.validate_file_extension(
            "tests/example_files/example_peaktable_mzmine3.csv", ".csv"
        )
        is None
    )


def test_validate_file_extension_invalid():
    with pytest.raises(TypeError):
        ValidationManager.validate_file_extension(
            "tests/example_files/example_peaktable_mzmine3.csv", ".mgf"
        )


def test_validate_file_extension_no_exception_valid_input():
    try:
        ValidationManager.validate_file_extension(
            "tests/example_files/example_peaktable_mzmine3.csv", ".csv"
        )
    except TypeError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_keys_valid():
    assert (
        ValidationManager.validate_keys(
            {"A": "one", "B": "two", "C": "three"}, "A", "B", "C"
        )
        is None
    )


def test_validate_keys_invalid():
    with pytest.raises(KeyError):
        ValidationManager.validate_keys(
            {"A": "one", "B": "two", "C": "three"}, "no_valid_key"
        )


def test_validate_keys_invalid_no_exception_valid_input():
    try:
        ValidationManager.validate_keys(
            {"A": "one", "B": "two", "C": "three"}, "A", "B", "C"
        )
    except KeyError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_value_in_list_valid():
    assert ValidationManager.validate_value_in_list(["A", "B", "C"], "A") is None


def test_validate_value_in_list_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_value_in_list(["A", "B", "C"], "D")


def test_validate_value_in_list_no_exception_valid_input():
    try:
        ValidationManager.validate_value_in_list(["A", "B", "C"], "A")
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_csv_file_valid():
    assert (
        ValidationManager.validate_csv_file(
            "tests/example_files/example_peaktable_mzmine3.csv",
        )
        is None
    )


def test_validate_csv_file_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_csv_file(
            "tests/example_files/example_invalid_csv.md",
        )


def test_validate_csv_file_no_exception_valid_input():
    try:
        ValidationManager.validate_csv_file(
            "tests/example_files/example_peaktable_mzmine3.csv",
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_peaktable_mzmine3_valid():
    assert (
        ValidationManager.validate_peaktable_mzmine3(
            "tests/example_files/example_peaktable_mzmine3.csv",
        )
        is None
    )


def test_validate_peaktable_mzmine3_invalid():
    with pytest.raises(KeyError):
        ValidationManager.validate_peaktable_mzmine3(
            "tests/example_files/example_group_fermo.csv",
        )


def test_validate_peaktable_mzmine3_no_exception_valid_input():
    try:
        ValidationManager.validate_peaktable_mzmine3(
            "tests/example_files/example_peaktable_mzmine3.csv",
        )
    except KeyError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_no_duplicate_entries_valid():
    assert (
        ValidationManager.validate_no_duplicate_entries_csv_column(
            "tests/example_files/example_peaktable_mzmine3.csv", "id"
        )
        is None
    )


def test_validate_no_duplicate_entries_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_no_duplicate_entries_csv_column(
            "tests/example_files/example_duplicate_entries.csv", "sample_id"
        )


def test_validate_no_duplicate_entries_no_exception_valid_input():
    try:
        ValidationManager.validate_no_duplicate_entries_csv_column(
            "tests/example_files/example_peaktable_mzmine3.csv", "id"
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_mgf_file_valid():
    assert (
        ValidationManager.validate_mgf_file(
            "tests/example_files/example_msms_mgf.mgf",
        )
        is None
    )


def test_validate_mgf_file_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_mgf_file(
            "tests/example_files/example_duplicate_entries.csv",
        )


def test_validate_mgf_file_no_exception_valid_input():
    try:
        ValidationManager.validate_mgf_file(
            "tests/example_files/example_msms_mgf.mgf",
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_phenotype_fermo_valid():
    assert (
        ValidationManager.validate_phenotype_fermo(
            "tests/example_files/example_phenotype_fermo.csv",
        )
        is None
    )


def test_validate_phenotype_fermo_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_phenotype_fermo(
            "tests/example_files/example_duplicate_entries.csv",
        )


def test_validate_phenotype_fermo_no_exception_valid_input():
    try:
        ValidationManager.validate_phenotype_fermo(
            "tests/example_files/example_phenotype_fermo.csv",
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


def test_validate_group_metadata_fermo_valid():
    assert (
        ValidationManager.validate_group_metadata_fermo(
            "tests/example_files/example_group_fermo.csv",
        )
        is None
    )


def test_validate_group_metadata_fermo_invalid():
    with pytest.raises(ValueError):
        ValidationManager.validate_group_metadata_fermo(
            "tests/example_files/example_duplicate_entries.csv",
        )


def test_validate_group_metadata_fermo_no_exception_valid_input():
    try:
        ValidationManager.validate_group_metadata_fermo(
            "tests/example_files/example_group_fermo.csv",
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")


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
        (0.0, 1.0),
        [0.1, 0.5, 1.0],
        [0, 1],
        [1.0, 2.0],
        [1.0, 0.0],
    ],
)
def test_validate_range_zero_one_invalid(variable):
    with pytest.raises(ValueError):
        ValidationManager.validate_range_zero_one(variable)


def test_validate_range_zero_one_no_exception_valid_input():
    try:
        ValidationManager.validate_range_zero_one(
            [0.0, 1.0],
        )
    except ValueError:
        pytest.fail("Validation raised an exception for valid input")
