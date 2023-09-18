import pytest

from fermo_core.data_processing.parser.class_msms_parser import MsmsParser
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


def test_instantiate_parser_valid():
    msms_parser = MsmsParser(
        "tests/example_files/example_msms_mgf.mgf",
        "mgf",
    )
    assert isinstance(msms_parser, MsmsParser)


@pytest.fixture
def feature_repo():
    repository = Repository()
    feature = Feature()
    feature.f_id = 1
    repository.add(1, feature)
    return repository


def test_parse_valid(feature_repo):
    msms_parser = MsmsParser(
        "tests/example_files/example_msms_mgf.mgf",
        "mgf",
    )
    features = msms_parser.parse(feature_repo)
    assert isinstance(features.entries[1].msms, tuple)


def test_parse_mgf_valid(feature_repo):
    msms_parser = MsmsParser(
        "tests/example_files/example_msms_mgf.mgf",
        "mgf",
    )
    features = msms_parser.parse_mgf(feature_repo)
    assert isinstance(features.entries[1].msms, tuple)
