import pytest
import pandas as pd
from fermo_core.data_processing.builder_feature.class_specific_feature_director import (
    SpecificFeatureDirector,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def dummy_row():
    return pd.Series(
        {
            "id": 1,
            "mz": 123.456,
            "datafile:s:fwhm": 0.5,
            "datafile:s:intensity_range:max": 1000,
            "datafile:s:area": 200,
            "datafile:s:rt": 5.1,
            "datafile:s:rt_range:min": 4.9,
            "datafile:s:rt_range:max": 5.2,
        }
    )


def test_success_construct_mzmine(dummy_row):
    assert isinstance(
        SpecificFeatureDirector.construct_mzmine3(dummy_row, "s", 5000, 1000), Feature
    )
