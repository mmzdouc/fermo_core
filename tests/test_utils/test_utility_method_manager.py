import os
from urllib.error import URLError

import matchms
import numpy as np
import pytest

from fermo_core.utils.utility_method_manager import UtilityMethodManager
from fermo_core.config.class_default_settings import DefaultPaths


def test_download_file_valid():
    UtilityMethodManager().download_file(
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",
        os.devnull,
        200,
    )


def test_download_file_invalid():
    with pytest.raises(URLError):
        UtilityMethodManager().download_file("https://asdfasdfasdfa", os.devnull, 200)


def test_download_file_timeout():
    with pytest.raises(URLError):
        UtilityMethodManager().download_file(
            "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",
            os.devnull,
            0.00001,
        )


def test_create_spectrum_object_valid():
    spectrum = UtilityMethodManager.create_spectrum_object(
        {
            "mz": np.array([10, 40, 60], dtype=float),
            "intens": np.array([10, 20, 100], dtype=float),
            "f_id": 0,
            "precursor_mz": 100.0,
        },
        0.005,
    )
    assert isinstance(spectrum, matchms.Spectrum)
    assert len(spectrum.mz) == 3


def test_mass_deviation_valid():
    assert round(UtilityMethodManager.mass_deviation(100.0, 100.001, 1), 0) == 10.0


def test_mass_deviation_invalid():
    with pytest.raises(ZeroDivisionError):
        UtilityMethodManager.mass_deviation(100.0, 0, 1)


@pytest.mark.slow
def test_check_ms2query_req_pos():
    UtilityMethodManager().check_ms2query_req("positive")
    assert len(list(DefaultPaths().dirpath_ms2query_pos.glob("*"))) == (
        len(DefaultPaths().url_ms2query_pos) + 1  # accounts for '.placeholder'
    )


@pytest.mark.slow
def test_check_ms2query_req_neg():
    UtilityMethodManager().check_ms2query_req("negative")
    assert len(list(DefaultPaths().dirpath_ms2query_neg.glob("*"))) == (
        len(DefaultPaths().url_ms2query_neg) + 1  # accounts for '.placeholder'
    )


@pytest.mark.slow
def test_check_ms2deepscore_req_valid():
    UtilityMethodManager().check_ms2deepscore_req("positive")
    assert len(list(DefaultPaths().dirpath_ms2deepscore_pos.glob("*"))) == (
        1 + 1  # accounts for '.placeholder'
    )
