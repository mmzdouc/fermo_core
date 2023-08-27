import pytest

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def feature():
    return Feature()


@pytest.fixture
def expected_attributes():
    return (
        "f_id",
        "mz",
        "rt",
        "rt_start",
        "rt_stop",
        "rt_range",
        "trace",
        "fwhm",
        "intensity",
        "rel_intensity",
        "area",
        "msms",
        "samples",
        "blank",
        "groups",
        "groups_fold",
        "phenotypes",
        "annotations",
        "networks",
        "scores",
    )


def test_expected_values_dataclass_feature(feature, expected_attributes):
    for attr in expected_attributes:
        assert hasattr(
            feature, attr
        ), f"Attribute '{attr} is missing in dataclass Feature."


def test_unexpected_values_dataclass_feature(feature, expected_attributes):
    unexpected_attributes = []
    for attr in dir(feature):
        if not attr.startswith("_") and attr not in expected_attributes:
            unexpected_attributes.append(attr)
    assert (
        len(unexpected_attributes) == 0
    ), f"Unexpected attributes found in dataclass Feature: {unexpected_attributes}."
