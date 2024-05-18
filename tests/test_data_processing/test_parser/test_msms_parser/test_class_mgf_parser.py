import pytest

from fermo_core.data_processing.parser.msms_parser.class_mgf_parser import MgfParser
from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import MsmsParameters
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters


@pytest.fixture
def params():
    params = ParameterManager()
    params.MsmsParameters = MsmsParameters(
        **{
            "filepath": "tests/test_data/test.msms.mgf",
            "format": "mgf",
            "rel_int_from": 0.005,
        }
    )
    params.PeaktableParameters = PeaktableParameters(
        **{
            "filepath": "tests/test_data/test.peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    return params


@pytest.fixture
def feature_repo(params):
    return PeakMzmine3Parser().extract_features(params)


def test_instantiate_parser_valid(params, feature_repo):
    assert isinstance(MgfParser(params=params, features=feature_repo), MgfParser)


def test_parse_valid(feature_repo, params):
    parser = MgfParser(params=params, features=feature_repo)
    parser.parse()
    feature_repo = parser.return_features()
    assert feature_repo.entries.get(126).Spectrum is not None


def test_modify_features_valid(params, feature_repo):
    parser = MgfParser(params=params, features=feature_repo)
    parser.modify_features()
    feature_repo = parser.return_features()
    assert feature_repo.entries.get(126).Spectrum is not None
