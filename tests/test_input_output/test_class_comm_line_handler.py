import pytest

from pathlib import Path
import argparse

from fermo_core.input_output.class_comm_line_handler import CommLineHandler
from fermo_core.input_output.class_validation_handler import ValidationHandler
from fermo_core.input_output.dataclass_params_handler import ParamsHandler


@pytest.fixture
def validation_handler():
    return ValidationHandler()


@pytest.fixture
def commline_handler():
    return CommLineHandler()


@pytest.fixture
def params_handler():
    return ParamsHandler("0.1.0", Path("my/path/here"))


def test_success_assign_peaktable_mzmine3(validation_handler, commline_handler):
    assert (
        commline_handler.assign_peaktable_mzmine3(
            "peaktable_mzmine3",
            "tests/example_files/example_peaktable_mzmine3.csv",
            validation_handler,
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_peaktable_mzmine3(validation_handler, commline_handler):
    assert commline_handler.assign_peaktable_mzmine3(
        "peaktable_mzmine3",
        "tests/example_files/example_speclib_mgf.mgf",
        validation_handler,
    )


def test_success_assign_mgf(validation_handler, commline_handler):
    assert (
        commline_handler.assign_mgf(
            "msms_mgf", "tests/example_files/example_msms_mgf.mgf", validation_handler
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_mgf(validation_handler, commline_handler):
    assert commline_handler.assign_mgf(
        "msms_mgf",
        "tests/example_files/example_peaktable_mzmine3.csv",
        validation_handler,
    )


def test_success_assign_phenotype_fermo(validation_handler, commline_handler):
    assert (
        commline_handler.assign_phenotype_fermo(
            "phenotype_fermo",
            "tests/example_files/example_phenotype_fermo.csv",
            "percentage",
            validation_handler,
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_phenotype_fermo(validation_handler, commline_handler):
    assert commline_handler.assign_phenotype_fermo(
        "phenotype_fermo",
        "tests/example_files/example_msms_mgf.mgf",
        "percentage",
        validation_handler,
    )


def test_success_assign_group_fermo(validation_handler, commline_handler):
    assert (
        commline_handler.assign_group_fermo(
            "group_fermo",
            "tests/example_files/example_group_fermo.csv",
            validation_handler,
        )
        is not None
    )


@pytest.mark.xfail
def test_fail_assign_group_fermo(validation_handler, commline_handler):
    assert commline_handler.assign_group_fermo(
        "group_fermo", "tests/example_files/example_msms_mgf.mgf", validation_handler
    )


def test_success_assign_mass_dev_ppm(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_mass_dev_ppm("mass_dev_ppm", 20, validation_handler),
        int,
    )


@pytest.mark.xfail
def test_fail_assign_mass_dev_ppm(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_mass_dev_ppm("mass_dev_ppm", "200", validation_handler),
        int,
    )


def test_success_assign_pos_int(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_pos_int("mass_dev_ppm", 10, validation_handler), int
    )


@pytest.mark.xfail
def test_fail_assign_pos_int(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_pos_int("mass_dev_ppm", "-1", validation_handler), int
    )


def test_success_assign_float_zero_one(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_float_zero_one("fragment_tol", 0.1, validation_handler),
        float,
    )


@pytest.mark.xfail
def test_fail_assign_float_zero_one(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_float_zero_one("fragment_tol", 5.0, validation_handler),
        float,
    )


def test_success_assign_bool(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_bool("flag_ms2query", True, validation_handler), bool
    )


@pytest.mark.xfail
def test_fail_assign_bool(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_bool("flag_ms2query", "True", validation_handler), bool
    )


def test_success_assign_range_zero_one(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_range_zero_one(
            "rel_int_range", [0.0, 1.0], validation_handler
        ),
        tuple,
    )


@pytest.mark.xfail
def test_fail_assign_range_zero_one(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_range_zero_one(
            "rel_int_range", [0.0, 0.1, 0.5], validation_handler
        ),
        tuple,
    )


def test_success_assign_network_alg(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_network_alg(
            "spectral_sim_network_alg", "ms2deepscore", validation_handler
        ),
        str,
    )


@pytest.mark.xfail
def test_fail_assign_network_alg(validation_handler, commline_handler):
    assert isinstance(
        commline_handler.assign_network_alg(
            "spectral_sim_network_alg", "nonexisting_alg", validation_handler
        ),
        str,
    )


def test_define_argparse_args(params_handler):
    assert isinstance(
        CommLineHandler.define_argparse_args(params_handler), argparse.ArgumentParser
    ), "Could not instantiate 'argparse.ArgumentParser'."
