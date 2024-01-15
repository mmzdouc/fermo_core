import os
from urllib.error import URLError

import pytest

from fermo_core.data_analysis.sim_networks_manager.class_ms2deepscore_networker import (
    Ms2deepscoreNetworker,
)
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkDeepscoreParameters,
)


def test_init_valid():
    assert isinstance(Ms2deepscoreNetworker(), Ms2deepscoreNetworker)


def test_download_file_valid():
    Ms2deepscoreNetworker().download_file(
        "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv",
        os.devnull,
    )


def test_download_file_invalid():
    with pytest.raises(URLError):
        Ms2deepscoreNetworker().download_file("https://asdfasdfasdfa", os.devnull)


def test_verify_presence_ms2query_file_valid(parameter_instance):
    ms2deep = Ms2deepscoreNetworker()
    assert (
        ms2deep.verify_presence_ms2deepscore_file(
            parameter_instance.SpecSimNetworkDeepscoreParameters
        )
        is None
    )


def test_verify_presence_ms2query_file_invalid():
    ms2deep = Ms2deepscoreNetworker()
    settings = SpecSimNetworkDeepscoreParameters()
    settings.filename = "asfas"
    settings.url = "https://asdfasdfasdfa"
    with pytest.raises(URLError):
        ms2deep.verify_presence_ms2deepscore_file(settings)
