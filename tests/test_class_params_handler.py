from pathlib import Path

import pandas as pd
import pytest
from fermo_core.input_output.class_params_handler import ParamsHandler


@pytest.fixture
def params_handler():
    return ParamsHandler("0.1.0", Path("my/path/here"))


def test_default_values_class_params_handler(params_handler):
    for a in [
        a
        for a in dir(params_handler)
        if not (a.startswith("_") or a.startswith("validate"))
    ]:
        if a == "version":
            assert getattr(params_handler, a) == "0.1.0"
        elif a == "root":
            assert getattr(params_handler, a) == Path("my/path/here")
        elif a == "session":
            assert getattr(params_handler, a) is None
        elif a == "peaktable_mzmine3":
            assert getattr(params_handler, a) is None
        elif a == "msms_mgf":
            assert getattr(params_handler, a) is None
        elif a == "phenotype_fermo":
            assert getattr(params_handler, a) is None
        elif a == "group_fermo":
            assert getattr(params_handler, a) is None
        elif a == "speclib_mgf":
            assert getattr(params_handler, a) is None
        elif a == "mass_dev_ppm":
            assert getattr(params_handler, a) == 20
        elif a == "msms_frag_min":
            assert getattr(params_handler, a) == 5
        elif a == "phenotype_fold":
            assert getattr(params_handler, a) == 10
        elif a == "column_ret_fold":
            assert getattr(params_handler, a) == 10
        elif a == "fragment_tol":
            assert getattr(params_handler, a) == 0.1
        elif a == "spectral_sim_score_cutoff":
            assert getattr(params_handler, a) == 0.7
        elif a == "max_nr_links_spec_sim":
            assert getattr(params_handler, a) == 10
        elif a == "min_nr_matched_peaks":
            assert getattr(params_handler, a) == 5
        elif a == "spectral_sim_network_alg":
            assert getattr(params_handler, a) == "modified_cosine"
        elif a == "flag_ms2query":
            assert getattr(params_handler, a) is False
        elif a == "flag_ms2query_blank":
            assert getattr(params_handler, a) is False
        elif a == "ms2query_filter_range":
            assert getattr(params_handler, a) == (0.0, 1.0)
        elif a == "rel_int_range":
            assert getattr(params_handler, a) == (0.0, 1.0)
        else:
            assert False, f"{a} is not covered by this unit test."


@pytest.mark.parametrize(
    "b",
    [
        True,
        False,
    ],
)
def test_success_validate_bool(b):
    assert ParamsHandler.validate_bool(b)[0]


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
    assert not ParamsHandler.validate_bool(b)[0]


def test_success_validate_string():
    assert ParamsHandler.validate_string("fermo_core/main.py")[0]


def test_fail_validate_string():
    assert not ParamsHandler.validate_string(1)[0]


@pytest.mark.parametrize(
    "i",
    [
        1,
        0,
    ],
)
def test_success_validate_pos_int_or_zero(i):
    assert ParamsHandler.validate_pos_int_or_zero(i)[0]


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
    assert not ParamsHandler.validate_pos_int_or_zero(i)[0]


@pytest.mark.parametrize(
    "i",
    [
        1,
        100,
    ],
)
def test_success_validate_pos_int(i):
    assert ParamsHandler.validate_pos_int(i)[0]


@pytest.mark.parametrize("i", [-1, 0, 1.0, -1.0, "string"])
def test_fail_validate_pos_int(i):
    assert not ParamsHandler.validate_pos_int(i)[0]


@pytest.mark.parametrize(
    "mass_dev_ppm",
    [
        10,
        100,
        1,
    ],
)
def test_success_validate_mass_dev_ppm(params_handler, mass_dev_ppm):
    assert params_handler.validate_mass_dev_ppm(mass_dev_ppm)[0]


@pytest.mark.parametrize(
    "mass_dev_ppm",
    [
        "string",
        -1,
        0,
        150,
    ],
)
def test_fail_validate_mass_dev_ppm(params_handler, mass_dev_ppm):
    assert not params_handler.validate_mass_dev_ppm(mass_dev_ppm)[0]


@pytest.mark.parametrize(
    "f",
    [
        0.0,
        0.5,
        1.0,
    ],
)
def test_success_validate_float_zero_one(f):
    assert ParamsHandler.validate_float_zero_one(f)[0]


@pytest.mark.parametrize(
    "f",
    [
        -1.0,
        1.5,
    ],
)
def test_fail_validate_float_zero_one(f):
    assert not ParamsHandler.validate_float_zero_one(f)[0]


@pytest.mark.parametrize(
    "alg",
    [
        "all",
        "modified_cosine",
        "ms2deepscore",
    ],
)
def test_success_validate_spectral_sim_network_alg(params_handler, alg):
    assert params_handler.validate_spectral_sim_network_alg(alg)[0]


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
def test_fail_validate_spectral_sim_network_alg(params_handler, alg):
    assert not params_handler.validate_spectral_sim_network_alg(alg)[0]


@pytest.mark.parametrize(
    "r",
    [
        (0.0, 1.0),
        (0.5, 1.0),
        (0.5, 0.6),
    ],
)
def test_success_validate_range_zero_one(r):
    assert ParamsHandler.validate_range_zero_one(r)[0]


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
    assert not ParamsHandler.validate_range_zero_one(r)[0]


def test_success_validate_file_exists():
    assert ParamsHandler.validate_file_exists(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )[0]


def test_fail_validate_file_exists():
    assert not ParamsHandler.validate_file_exists(Path("file/which/does/not/exist"))[0]


def test_success_validate_csv_file():
    assert ParamsHandler.validate_csv_file(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )[0]


def test_fail_validate_csv_file():
    assert not ParamsHandler.validate_csv_file(
        Path("tests/example_files/example_invalid_csv.md")
    )[0]


def test_success_validate_csv_duplicate_col_entries():
    assert ParamsHandler.validate_csv_duplicate_col_entries(
        pd.DataFrame({"id": [1, 2]}), "id"
    )[0]


def test_fail_validate_csv_duplicate_col_entries():
    assert not ParamsHandler.validate_csv_duplicate_col_entries(
        pd.DataFrame({"id": [1, 1]}), "id"
    )[0]


def test_success_validate_peaktable_mzmine3(params_handler):
    assert params_handler.validate_peaktable_mzmine3(
        Path("tests/example_files/example_peaktable_mzmine3.csv")
    )[0]


def test_fail_validate_peaktable_mzmine3(params_handler):
    assert not params_handler.validate_peaktable_mzmine3(
        Path("tests/example_files/example_group_fermo.csv")
    )[0]


def test_success_validate_mgf(params_handler):
    assert params_handler.validate_mgf(
        Path("tests/example_files/example_msms_mgf.mgf")
    )[0]


def test_fail_validate_mgf(params_handler):
    assert not params_handler.validate_mgf(
        Path("tests/example_files/example_invalid_csv.md")
    )[0]
