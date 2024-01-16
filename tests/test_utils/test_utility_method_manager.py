import os
from urllib.error import URLError

import pytest

from fermo_core.utils.utility_method_manager import UtilityMethodManager


def test_download_file_valid():
    UtilityMethodManager().download_file(
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",
        os.devnull,
    )


def test_download_file_invalid():
    with pytest.raises(URLError):
        UtilityMethodManager().download_file("https://asdfasdfasdfa", os.devnull)
