import pytest


@pytest.fixture
def stats_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return stats


@pytest.fixture
def feature_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return features


@pytest.fixture
def sample_instance(general_parser_instance):
    stats, features, samples = general_parser_instance.return_attributes()
    return samples
