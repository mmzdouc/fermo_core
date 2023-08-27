import pytest
import pandas as pd
from fermo_core.data_processing.builder_sample.class_samples_director import (
    SamplesDirector,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


@pytest.fixture
def dummy_df():
    return pd.DataFrame(
        {
            "id": [1],
            "datafile:s:fwhm": [0.5],
            "datafile:s:intensity_range:max": [1000],
            "datafile:s:area": [200],
            "datafile:s:rt": [5.1],
            "datafile:s:rt_range:min": [4.9],
            "datafile:s:rt_range:max": [5.2],
            "datafile:s:feature_state": ["DETECTED"],
        }
    )


def test_success_construct_mzmine(dummy_df):
    assert isinstance(
        SamplesDirector.construct_mzmine3("s", dummy_df, tuple([1])), Sample
    ), "Could not build an instance of object Sample using SamplesDirector."
