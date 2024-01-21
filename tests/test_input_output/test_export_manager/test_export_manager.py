from datetime import datetime
from pathlib import Path

import pytest

from fermo_core.input_output.class_export_manager import ExportManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
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


def test_write_to_fermo_json_invalid(export_m_dummy):
    export_m_dummy.json_dict = {"asdfasdfa": "sdtaesrawe"}
    export_m_dummy.params.OutputParameters.filepath = Path("dsa/asdas/sdasd")
    export_m_dummy.params.OutputParameters.default_filepath = Path("dsa/asdas/sdasd")
    with pytest.raises(FileNotFoundError):
        export_m_dummy.write_to_fermo_json()


def test_build_json_dict_valid(real_data_export):
    real_data_export.build_json_dict(version="0.0.0", starttime=datetime.now())
    assert isinstance(real_data_export.json_dict, dict)


def test_export_params_valid(real_data_export):
    real_data_export.export_params()
    assert real_data_export.json_dict.get("parameters") is not None


def test_export_stats_valid(real_data_export):
    real_data_export.export_stats()
    assert isinstance(real_data_export.json_dict.get("stats").get("rt_min"), float)


def test_export_features_repo_valid(real_data_export):
    real_data_export.export_features_repo()
    assert (
        real_data_export.json_dict.get("general_features").get(1).get("spectrum")
        is not None
    )


def test_export_samples_repo_valid(real_data_export):
    real_data_export.export_samples_repo()
    assert (
        real_data_export.json_dict.get("samples").get("5425_5426_mod.mzXML") is not None
    )


def test_export_metadata_valid(export_m_dummy):
    export_m_dummy.export_metadata(version="0.0.0", starttime=datetime.now())
    assert export_m_dummy.json_dict["metadata"]["runtime_seconds"] is not None
