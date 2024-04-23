from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from fermo_core.input_output.class_export_manager import ExportManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.output_file_parameter_managers import OutputParameters
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    SimNetworks,
    Feature,
    Annotations,
    Ribosomal,
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
    assert real_data_export.session is not None


def test_write_fermo_json_invalid(export_m_dummy):
    export_m_dummy.session = {"asdfasdfa": "sdtaesrawe"}
    export_m_dummy.params.OutputParameters = OutputParameters()
    export_m_dummy.params.OutputParameters.dir_path = Path("dsa/asdas/sdasd")
    export_m_dummy.params.PeaktableParameters = PeaktableParameters(
        filepath="example_data/case_study_peak_table_quant_full.csv",
        format="mzmine3",
        polarity="positive",
    )
    export_m_dummy.define_filename()
    with pytest.raises(FileNotFoundError):
        export_m_dummy.write_fermo_json(version="0.1.0", starttime=datetime.now())


def test_build_json_dict_valid(export_m_dummy):
    export_m_dummy.build_json_dict(version="0.0.0", starttime=datetime.now())
    assert isinstance(export_m_dummy.session, dict)


def test_export_params_json_valid(export_m_dummy):
    export_m_dummy.export_params_json()
    assert export_m_dummy.session.get("parameters") is not None


def test_export_stats_json_valid(export_m_dummy):
    export_m_dummy.export_stats_json()
    assert export_m_dummy.session.get("stats") is not None


def test_export_features_json_valid(export_m_dummy):
    export_m_dummy.export_features_json()
    assert export_m_dummy.session.get("general_features") is not None


def test_export_samples_json_valid(export_m_dummy):
    export_m_dummy.stats.samples = tuple()
    export_m_dummy.export_samples_json()
    assert export_m_dummy.session.get("samples") is not None


def test_export_metadata_json_valid(export_m_dummy):
    export_m_dummy.export_metadata_json(version="0.0.0", starttime=datetime.now())
    assert export_m_dummy.session["metadata"]["runtime_seconds"] is not None


def test_build_csv_output_valid(real_data_export):
    real_data_export.stats.networks = {"xyz": {}}
    real_data_export.features.entries[1].networks = {
        "xyz": SimNetworks(algorithm="xyz", network_id=99)
    }
    real_data_export.build_csv_output()
    assert real_data_export.df["fermo:networks:xyz:network_id"].values[0] == 99
    assert real_data_export.df_full["fermo:networks:xyz:network_id"].values[0] == 99
    assert real_data_export.df_abbrev["fermo:networks:xyz:network_id"].values[0] == 99


def test_add_networks_info_csv_valid(real_data_export):
    real_data_export.stats.networks = {"xyz": {}}
    real_data_export.features.entries[1].networks = {
        "xyz": SimNetworks(algorithm="xyz", network_id=99)
    }
    real_data_export.df = pd.read_csv(
        real_data_export.params.PeaktableParameters.filepath
    )
    real_data_export.add_networks_info_csv()
    assert real_data_export.df["fermo:networks:xyz:network_id"].values[0] == 99


def test_get_network_value_valid(export_m_dummy):
    export_m_dummy.features.add(
        1,
        Feature(networks={"xyz": SimNetworks(algorithm="xyz", network_id=99)}, f_id=1),
    )
    assert export_m_dummy.get_network_value(1, "fermo:networks:xyz:network_id") == 99


def test_get_network_value_invalid(export_m_dummy):
    assert export_m_dummy.get_network_value(1, "fermo:networks:xyz:network_id") is None


def test_add_class_evidence_csv(real_data_export):
    feature = Feature()
    feature.Annotations = Annotations(
        classes={"ribosomal": Ribosomal(aa_tags=["F", "Q-T"])}
    )
    real_data_export.features.modify(1, feature)
    real_data_export.df = pd.read_csv(
        real_data_export.params.PeaktableParameters.filepath
    )
    real_data_export.add_class_evidence_csv()
    assert (
        real_data_export.df["fermo:annotation:ribosomal:monomers"].values[0] is not None
    )


def test_add_sample_info_csv(real_data_export):
    real_data_export.df = pd.read_csv(
        real_data_export.params.PeaktableParameters.filepath
    )
    real_data_export.add_sample_info_csv()
    assert real_data_export.df["fermo:samples"] is not None
