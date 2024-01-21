import matchms
import numpy as np
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
        **{"filepath": "example_data/case_study_MSMS.mgf", "format": "mgf"}
    )
    params.PeaktableParameters = PeaktableParameters(
        **{
            "filepath": "example_data/case_study_peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    return params


@pytest.fixture
def feature_repo(params):
    return PeakMzmine3Parser().extract_features(params)


def test_instantiate_parser_valid():
    assert isinstance(MgfParser(), MgfParser)


def test_parse_valid(feature_repo, params):
    feature_repo = MgfParser().parse(feature_repo, params)
    assert feature_repo.entries.get(126).Spectrum is not None


def test_modify_features_valid(params, feature_repo):
    feature_repo = MgfParser().modify_features(feature_repo, params)
    assert feature_repo.entries.get(126).Spectrum is not None


def test_create_spectrum_object_valid():
    spectrum = MgfParser().create_spectrum_object(
        {
            "mz": np.array([10, 40, 60], dtype=float),
            "intens": np.array([10, 20, 100], dtype=float),
            "f_id": 1,
            "precursor_mz": 100.0,
        }
    )
    assert isinstance(spectrum, matchms.Spectrum)
