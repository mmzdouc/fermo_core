import pytest

from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters


@pytest.fixture
def params():
    params = ParameterManager()
    params.PeaktableParameters = PeaktableParameters(
        **{
            "filepath": "example_data/case_study_peak_table_quant_full.csv",
            "format": "mzmine3",
            "polarity": "positive",
        }
    )
    return params


def test_instantiate_parser_valid():
    assert isinstance(PeakMzmine3Parser(), PeakMzmine3Parser)


def test_parse_valid(params):
    stats, feature_repo, sample_repo = PeakMzmine3Parser().parse(params)
    assert len(stats.features) == 143


def test_extract_stats_valid(params):
    stats = PeakMzmine3Parser().extract_stats(params)
    assert len(stats.features) == 143


def test_extract_features_valid(params):
    feature_repo = PeakMzmine3Parser().extract_features(params)
    assert len(feature_repo.entries) == 143


def test_extract_samples_valid(params):
    stats = PeakMzmine3Parser.extract_stats(params)
    sample_repo = PeakMzmine3Parser().extract_samples(stats, params)
    assert len(sample_repo.entries) == 11
