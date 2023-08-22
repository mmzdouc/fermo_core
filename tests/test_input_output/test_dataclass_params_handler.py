from pathlib import Path

import pytest
from fermo_core.input_output.dataclass_params_handler import ParamsHandler


@pytest.fixture
def params_handler():
    return ParamsHandler("0.1.0", Path("my/path/here"))


@pytest.fixture
def expected_attributes():
    return (
        "version",
        "root",
        "session",
        "peaktable_mzmine3",
        "msms_mgf",
        "phenotype_fermo",
        "phenotype_fermo_mode",
        "group_fermo",
        "speclib_mgf",
        "mass_dev_ppm",
        "msms_frag_min",
        "phenotype_fold",
        "column_ret_fold",
        "fragment_tol",
        "spectral_sim_score_cutoff",
        "max_nr_links_spec_sim",
        "min_nr_matched_peaks",
        "spectral_sim_network_alg",
        "flag_ms2query",
        "flag_ms2query_blank",
        "ms2query_filter_range",
        "rel_int_range",
    )


def test_expected_values_dataclass_paramshandler(params_handler, expected_attributes):
    for attr in expected_attributes:
        assert hasattr(
            params_handler, attr
        ), f"Attribute '{attr}  is missing in dataclass ParamsHandler"


def test_unexpected_values_dataclass_paramshandler(params_handler, expected_attributes):
    unexpected_attributes = []
    for attr in dir(params_handler):
        if not attr.startswith("_") and attr not in expected_attributes:
            unexpected_attributes.append(attr)
    assert len(unexpected_attributes) == 0, (
        f"Unexpected attributes found in dataclass ParamsHandler:"
        f" {unexpected_attributes}."
    )
