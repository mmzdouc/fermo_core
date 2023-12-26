import pytest
from pydantic import ValidationError

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


def test_init_feature_valid():
    assert isinstance(Feature(), Feature)


def test_init_feature_invalid():
    with pytest.raises(ValidationError):
        Feature(active=234123)
