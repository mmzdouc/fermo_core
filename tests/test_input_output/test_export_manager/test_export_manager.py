from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from fermo_core.input_output.class_export_manager import ExportManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    SimNetworks, Feature
)
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository


@pytest.fixture
def export_m_dummy():
    return ExportManager(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )


@pytest.fixture
def real_data_export(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return ExportManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


def test_run_valid(real_data_export):
    real_data_export.run("0.1.0", datetime.now())
    assert real_data_export.json_dict is not None


def test_validate_output_filepath_valid(export_m_dummy):
    export_m_dummy.params.OutputParameters.filepath = Path(
        "example_data/fermo_session.json"
    )
    export_m_dummy.validate_output_filepath()
    assert export_m_dummy.params.OutputParameters.filepath.name == "fermo_session"


def test_validate_output_filepath_invalid(export_m_dummy):
    export_m_dummy.params.OutputParameters.filepath = Path("dsa/asdas/sdasd.json")
    export_m_dummy.validate_output_filepath()
    assert export_m_dummy.params.OutputParameters.filepath.parent.name == "example_data"


def test_validate_output_created_valid(export_m_dummy):
    assert export_m_dummy.validate_output_created(
        Path("example_data/case_study_parameters.json")
    ) is None


def test_validate_output_created_invalid(export_m_dummy):
    with pytest.raises(FileNotFoundError):
        export_m_dummy.validate_output_created(Path("sadasa/adsasd"))


def test_write_fermo_json_invalid(export_m_dummy):
    export_m_dummy.json_dict = {"asdfasdfa": "sdtaesrawe"}
    export_m_dummy.params.OutputParameters.filepath = Path("dsa/asdas/sdasd")
    export_m_dummy.params.OutputParameters.default_filepath = Path("dsa/asdas/sdasd")
    with pytest.raises(FileNotFoundError):
        export_m_dummy.write_fermo_json()


def test_build_json_dict_valid(export_m_dummy):
    export_m_dummy.build_json_dict(version="0.0.0", starttime=datetime.now())
    assert isinstance(export_m_dummy.json_dict, dict)


def test_export_params_json_valid(export_m_dummy):
    export_m_dummy.export_params_json()
    assert export_m_dummy.json_dict.get("parameters") is not None


def test_export_stats_json_valid(export_m_dummy):
    export_m_dummy.export_stats_json()
    assert export_m_dummy.json_dict.get("stats") is not None


def test_export_features_json_valid(export_m_dummy):
    export_m_dummy.export_features_json()
    assert export_m_dummy.json_dict.get("general_features") is not None


def test_export_samples_json_valid(export_m_dummy):
    export_m_dummy.export_samples_json()
    assert export_m_dummy.json_dict.get("samples") is not None


def test_export_metadata_json_valid(export_m_dummy):
    export_m_dummy.export_metadata_json(version="0.0.0", starttime=datetime.now())
    assert export_m_dummy.json_dict["metadata"]["runtime_seconds"] is not None


def test_write_csv_output_invalid(export_m_dummy):
    export_m_dummy.df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    export_m_dummy.params.OutputParameters.filepath = Path("dsa/asdas/sdasd")
    export_m_dummy.params.OutputParameters.default_filepath = Path("dsa/asdas/sdasd")
    with pytest.raises(FileNotFoundError):
        export_m_dummy.write_fermo_json()


def test_build_csv_output_valid(real_data_export):
    real_data_export.stats.networks = {"xyz": {}}
    real_data_export.features.entries[1].networks = {
        "xyz": SimNetworks(algorithm="xyz", network_id=99)
    }
    real_data_export.build_csv_output()
    assert real_data_export.df["fermo:networks:xyz:network_id"].values[0] == 99


def test_get_attribute_value_valid(export_m_dummy):
    export_m_dummy.features.add(1, Feature(
        networks={"xyz": SimNetworks(algorithm="xyz", network_id=99)},
        f_id=1
    ))
    assert export_m_dummy.get_attribute_value(1, "fermo:networks:xyz:network_id") == 99


def test_get_attribute_value_invalid(export_m_dummy):
    assert export_m_dummy.get_attribute_value(
        1, "fermo:networks:xyz:network_id"
    ) is None
