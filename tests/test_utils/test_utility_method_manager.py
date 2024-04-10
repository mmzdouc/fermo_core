import os
from urllib.error import URLError

import matchms
import numpy as np
import pytest

from fermo_core.utils.utility_method_manager import UtilityMethodManager


def test_check_ms2deepscore_req_valid():
    assert UtilityMethodManager().check_ms2deepscore_req()


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
        }
    )
    assert isinstance(spectrum, matchms.Spectrum)
