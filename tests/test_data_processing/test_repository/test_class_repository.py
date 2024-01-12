import pytest
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def repository():
    return Repository()


@pytest.fixture
def feature():
    return Feature()


def test_success_add_and_get_repository(repository, feature):
    repository.add(1, feature)
    assert repository.get(1) == feature, "Could not retrieve feature from repository."


def test_success_modify_repository(repository, feature):
    repository.add(1, feature)
    new_feature = Feature()
    repository.modify(1, new_feature)
    assert repository.get(1) == new_feature, "Could not modify existing feature."


def test_fail_add_existing_entry_repository(repository, feature):
    repository.add(1, feature)
    with pytest.raises(ValueError):
        repository.add(1, feature)


def test_fail_get_nonexisting_entry_repository(repository, feature):
    with pytest.raises(KeyError):
        repository.get(1)


def test_fail_modify_nonexisting_entry_repository(repository, feature):
    with pytest.raises(KeyError):
        repository.modify(1, feature)


def test_success_multiple_instances_repository(feature):
    repository1 = Repository()
    repository1.add(1, feature)
    repository2 = Repository()
    with pytest.raises(KeyError):
        repository2.get(1)


def test_remove_valid():
    repository1 = Repository()
    repository1.add(1, Feature())
    assert repository1.get(1) is not None
    repository1.remove(1)
    with pytest.raises(KeyError):
        repository1.get(1)


def test_remove_invalid():
    repository1 = Repository()
    with pytest.raises(KeyError):
        repository1.remove(1)
