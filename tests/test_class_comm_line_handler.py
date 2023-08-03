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
