import pytest
import pandas as pd
from fermo_core.data_processing.builder.class_general_feature_director import (
    GeneralFeatureDirector,
)


@pytest.fixture
def dummy_df():
    return pd.DataFrame(
        {
            "id": [1],
            "height": [100],
            "area": [200],
            "mz": [100.1],
            "rt": [5.1],
            "rt_range:min": [4.9],
            "rt_range:max": [5.2],
        }
    )


def test_success_construct_mzmine(dummy_df):
    feature_dict = GeneralFeatureDirector.construct_mzmine(dummy_df, tuple([1]))
    assert feature_dict[1].f_id == 1


# TODO(MMZ): also test for the correct types of the input
