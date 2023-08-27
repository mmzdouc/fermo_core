import pytest
import pandas as pd
from fermo_core.data_processing.class_parser import Parser
from fermo_core.input_output.dataclass_params_handler import ParamsHandler
from pathlib import Path


@pytest.fixture
def group_fermo():
    return pd.DataFrame(
        {
            "sample_name": ["sample1", "sample2"],
            "attr1": ["group1", "groupA"],
            "attr2": ["group2", "groupB"],
        }
    )


@pytest.fixture
def params():
    params = ParamsHandler("0.0.1", Path("not/a/real/path"))
    return params


def test_instantiate_parser():
    assert isinstance(Parser(), Parser), "Could not instantiate class 'Parser'."


# TODO(MMZ): continue with parse_group_mzmine3;
#  separate out _remove_sample_id_from_group_general
# TODO(MMZ): Add additional tests to test parser
