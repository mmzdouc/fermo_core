import pytest

from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.data_processing.parser.spec_library_parser.class_spec_lib_mgf_parser import (
    SpecLibMgfParser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import (
    PeaktableParameters,
    SpecLibParameters,
)


@pytest.fixture
def params():
    params = ParameterManager()
    params.PeaktableParameters = PeaktableParameters(
        **{
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    params.SpecLibParameters = SpecLibParameters(
        **{"filepath": "tests/test_data/test.spectral_library.mgf", "format": "mgf"}
    )
    return params


@pytest.fixture
def stats(params):
    return PeakMzmine3Parser().extract_stats(params)


def test_instantiate_parser_valid(params, stats):
    assert isinstance(SpecLibMgfParser(stats=stats, params=params), SpecLibMgfParser)


def test_parse_valid(stats, params):
    parser = SpecLibMgfParser(stats=stats, params=params)
    parser.parse()
    stats = parser.return_stats()
    assert stats.spectral_library is not None


def test_modify_stats(stats, params):
    parser = SpecLibMgfParser(stats=stats, params=params)
    parser.modify_stats()
    stats = parser.return_stats()
    assert stats.spectral_library is not None
