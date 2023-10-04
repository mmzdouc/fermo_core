import pytest

from fermo_core.data_processing.builder_sample.dataclass_sample import Sample, Phenotype


def test_success_initialize_sample():
    assert isinstance(Sample(), Sample), (
        "Could not initialize instance of object " "Sample"
    )


def test_success_initialize_phenotype():
    assert isinstance(
        Phenotype(10.0, 1), Phenotype
    ), "Could not initialize instance of object Phenotype"


@pytest.fixture
def sample():
    return Sample()


@pytest.fixture
def phenotype():
    return Phenotype(10.0, 1)


@pytest.fixture
def expected_attributes_sample():
    return (
        "s_id",
        "features",
        "feature_ids",
        "groups",
        "cliques",
        "phenotypes",
        "max_intensity",
    )


@pytest.fixture
def expected_attributes_phenotype():
    return ("value", "concentration")


def test_expected_values_dataclass_sample(sample, expected_attributes_sample):
    for attr in expected_attributes_sample:
        assert hasattr(
            sample, attr
        ), f"Attribute '{attr} is missing in dataclass Sample."


def test_unexpected_values_dataclass_sample(sample, expected_attributes_sample):
    unexpected_attributes = []
    for attr in dir(sample):
        if not attr.startswith("_") and attr not in expected_attributes_sample:
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in dataclass Sample: {unexpected_attributes}."


def test_expected_values_phenotype(phenotype, expected_attributes_phenotype):
    for attr in expected_attributes_phenotype:
        assert hasattr(
            phenotype, attr
        ), f"Attribute '{attr} is missing in class Phenotype."


def test_unexpected_values_phenotype(phenotype, expected_attributes_phenotype):
    unexpected_attributes = []
    for attr in dir(phenotype):
        if not attr.startswith("_") and attr not in expected_attributes_phenotype:
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in class Phenotype: {unexpected_attributes}."
