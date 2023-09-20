import pytest

from fermo_core.data_processing.parser.class_spectral_library_parser import (
    SpectralLibraryParser,
)
from fermo_core.data_processing.class_stats import Stats


@pytest.fixture
def stats():
    return Stats()


def test_instantiate_class():
    spec_lib_parser = SpectralLibraryParser(
        "tests/example_files/example_speclib_mgf.mgf", "mgf", 1000
    )
    assert isinstance(spec_lib_parser, SpectralLibraryParser)


@pytest.fixture
def spec_lib_parser():
    return SpectralLibraryParser(
        "tests/example_files/example_speclib_mgf.mgf", "mgf", 1000
    )


def test_parse_valid(stats, spec_lib_parser):
    stats = spec_lib_parser.parse(stats)
    assert stats.spectral_library is not None


def test_parse_invalid(stats, spec_lib_parser):
    spec_lib_parser.spectral_library_format = ""
    stats = spec_lib_parser.parse(stats)
    assert stats.spectral_library is None


def test_parse_mgf_valid(stats, spec_lib_parser):
    stats = spec_lib_parser.parse(stats)
    assert stats.spectral_library is not None
    assert stats.spectral_library.get(1) is not None
    assert stats.spectral_library.get(1).name == "Fakeomycin"
    assert stats.spectral_library.get(1).exact_mass == 1234.56
    assert isinstance(stats.spectral_library.get(1).msms, tuple)


def test_parse_mgf_invalid(stats, spec_lib_parser):
    spec_lib_parser.max_library_size = 0
    stats = spec_lib_parser.parse(stats)
    assert stats.spectral_library == dict()


def test_parse_mgf_invalid_input(stats, spec_lib_parser):
    spec_lib_parser.spectral_library_filepath = (
        "tests/example_files/example_invalid_speclib_mgf.mgf"
    )
    stats = spec_lib_parser.parse(stats)
    assert stats.spectral_library == dict()
