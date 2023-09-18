import pytest

from fermo_core.data_processing.parser.class_peaktable_parser import PeaktableParser


def test_instantiate_parser_valid():
    peaktable_parser = PeaktableParser(
        "tests/example_files/example_peaktable_mzmine3.csv",
        "mzmine3",
        (0.0, 1.0),
        (0.0, 1.0),
    )
    assert isinstance(peaktable_parser, PeaktableParser)


@pytest.fixture
def peaktable_parser():
    return PeaktableParser(
        "tests/example_files/example_peaktable_mzmine3.csv",
        "mzmine3",
        (0.0, 1.0),
        (0.0, 1.0),
    )


def test_parse_valid(peaktable_parser):
    stats, feature_repo, sample_repo = peaktable_parser.parse()
    assert stats.features == tuple([1])


def test_parse_mzmine3_valid(peaktable_parser):
    stats, feature_repo, sample_repo = peaktable_parser.parse_mzmine3()
    assert stats.features == tuple([1])
