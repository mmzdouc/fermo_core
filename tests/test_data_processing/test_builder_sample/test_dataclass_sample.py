import pytest

from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


def test_success_initialize_sample():
    assert isinstance(Sample(), Sample), (
        "Could not initialize instance of object " "Sample"
    )


@pytest.fixture
def sample():
    return Sample()


@pytest.fixture
def expected_attributes():
    return (
        "s_id",
        "features",
        "groups",
        "cliques",
        "phenotypes",
        "max_intensity",
    )


def test_expected_values_dataclass_sample(sample, expected_attributes):
    for attr in expected_attributes:
        assert hasattr(
            sample, attr
        ), f"Attribute '{attr} is missing in dataclass Sample."


def test_unexpected_values_dataclass_sample(sample, expected_attributes):
    unexpected_attributes = []
    for attr in dir(sample):
        if not attr.startswith("_") and attr not in expected_attributes:
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in dataclass Sample: {unexpected_attributes}."
