import pytest
import pandas as pd
from fermo_core.data_processing.builder_feature.class_general_feature_director import (
    GeneralFeatureDirector,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def dummy_row():
    return pd.Series(
        {
            "id": 1,
            "area": 200,
            "mz": 100.1,
            "rt": 5.1,
            "rt_range:min": 4.9,
            "rt_range:max": 5.2,
        }
    )


def test_success_construct_mzmine(dummy_row):
    assert isinstance(GeneralFeatureDirector.construct_mzmine3(dummy_row), Feature)
