import pytest
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def repository():
    return Repository()


@pytest.fixture
def feature():
    return Feature()


def test_success_add_repository(repository, feature):
    repository.add(1, feature)
    assert repository.entries[1] == feature


def test_success_get_repository(repository, feature):
    repository.add(1, feature)
    assert repository.get(1) == feature


def test_success_modify_repository(repository, feature):
    repository.add(1, feature)
    repository.modify(1, Feature())
    assert repository.get(1) != feature
