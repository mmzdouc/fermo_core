from pathlib import Path
import pytest

from fermo_core.input_output.class_comm_line_handler import CommLineHandler
from fermo_core.input_output.class_params_handler import ParamsHandler


@pytest.fixture
def params_handler():
    return ParamsHandler("0.1.0", Path("my/path/here"))


@pytest.fixture
def commline_handler():
    return CommLineHandler()


def test_success_assign_peaktable_mzmine3(params_handler, commline_handler):
    assert (
        commline_handler.assign_peaktable_mzmine3(
            "peaktable_mzmine3",
            "tests/example_files/example_peaktable_mzmine3.csv",
            params_handler,
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_peaktable_mzmine3(params_handler, commline_handler):
    assert commline_handler.assign_peaktable_mzmine3(
        "peaktable_mzmine3",
        "tests/example_files/example_speclib_mgf.mgf",
        params_handler,
    )


def test_success_assign_mgf(params_handler, commline_handler):
    assert (
        commline_handler.assign_mgf(
            "msms_mgf", "tests/example_files/example_msms_mgf.mgf", params_handler
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_mgf(params_handler, commline_handler):
    assert commline_handler.assign_mgf(
        "msms_mgf", "tests/example_files/example_peaktable_mzmine3.csv", params_handler
    )


def test_success_assign_phenotype_fermo(params_handler, commline_handler):
    assert (
        commline_handler.assign_phenotype_fermo(
            "phenotype_fermo",
            "tests/example_files/example_phenotype_fermo.csv",
            "percentage",
            params_handler,
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_phenotype_fermo(params_handler, commline_handler):
    assert commline_handler.assign_phenotype_fermo(
        "phenotype_fermo",
        "tests/example_files/example_msms_mgf.mgf",
        "percentage",
        params_handler,
    )


def test_success_assign_group_fermo(params_handler, commline_handler):
    assert (
        commline_handler.assign_group_fermo(
            "group_fermo", "tests/example_files/example_group_fermo.csv", params_handler
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_group_fermo(params_handler, commline_handler):
    assert commline_handler.assign_group_fermo(
        "group_fermo", "tests/example_files/example_msms_mgf.mgf", params_handler
    )


def test_success_assign_mass_dev_ppm(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_mass_dev_ppm("mass_dev_ppm", 20, params_handler), int
    )


@pytest.mark.xfail
def test_fail_assign_mass_dev_ppm(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_mass_dev_ppm("mass_dev_ppm", "200", params_handler), int
    )


def test_success_assign_pos_int(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_pos_int("mass_dev_ppm", 10, params_handler), int
    )


@pytest.mark.xfail
def test_fail_assign_pos_int(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_pos_int("mass_dev_ppm", "-1", params_handler), int
    )


def test_success_assign_float_zero_one(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_float_zero_one("fragment_tol", 0.1, params_handler),
        float,
    )


@pytest.mark.xfail
def test_fail_assign_float_zero_one(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_float_zero_one("fragment_tol", 5.0, params_handler),
        float,
    )


def test_success_assign_bool(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_bool("flag_ms2query", True, params_handler), bool
    )


@pytest.mark.xfail
def test_fail_assign_bool(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_bool("flag_ms2query", "True", params_handler), bool
    )


def test_success_assign_range_zero_one(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_range_zero_one(
            "rel_int_range", [0.0, 1.0], params_handler
        ),
        tuple,
    )


@pytest.mark.xfail
def test_fail_assign_range_zero_one(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_range_zero_one(
            "rel_int_range", [0.0, 0.1, 0.5], params_handler
        ),
        tuple,
    )


def test_success_assign_network_alg(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_network_alg(
            "spectral_sim_network_alg", "ms2deepscore", params_handler
        ),
        str,
    )


@pytest.mark.xfail
def test_fail_assign_network_alg(params_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_network_alg(
            "spectral_sim_network_alg", "nonexisting_alg", params_handler
        ),
        str,
    )
