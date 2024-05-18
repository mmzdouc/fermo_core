from datetime import datetime
import glob
import os
from pathlib import Path

import networkx as nx
import pandas as pd
import pytest

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.data_analysis.annotation_manager.class_ms2query_annotator import (
    MS2QueryAnnotator,
)
from fermo_core.input_output.class_export_manager import (
    ExportManager,
    JsonExporter,
    CsvExporter,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SimNetworks,
    Annotations,
    Adduct,
    NeutralLoss,
    Match,
    CharFrag,
)
from fermo_core.data_processing.class_stats import Stats, SpecSimNet, PhenoData
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_repository import Repository


@pytest.fixture
def real_data_export(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    real_data_export = ExportManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )
    real_data_export.params.OutputParameters.directory_path = Path(
        "tests/test_input_output/test_export_manager/"
    )
    real_data_export.filename_base = "dummy"
    return real_data_export


@pytest.fixture
def json_exporter():
    json_exporter = JsonExporter(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
        starttime=datetime.now(),
        version="0.1.0",
    )
    json_exporter.stats.active_features = {1}
    json_exporter.features.add(1, Feature(f_id=1, mz=123.45))
    json_exporter.stats.samples = ("dummy",)
    json_exporter.samples.add("dummy", Sample(s_id="dummy"))
    return json_exporter


@pytest.fixture
def csv_exporter():
    df = pd.DataFrame({"id": [1], "mz": [123.456]})
    csv_exporter = CsvExporter(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
        df=df,
    )
    csv_exporter.params.SpectralLibMatchingCosineParameters.activate_module = True
    csv_exporter.params.SpectralLibMatchingDeepscoreParameters.activate_module = True
    csv_exporter.params.AsResultsParameters = "dummy"
    csv_exporter.params.Ms2QueryAnnotationParameters.activate_module = True
    csv_exporter.stats.active_features = {1}
    csv_exporter.stats.networks = {
        "abc": SpecSimNet(
            algorithm="abc",
            subnetworks={},
            summary={0: set()},
            network=nx.Graph(),
        )
    }
    csv_exporter.stats.GroupMData.ctgrs = {"abcde": {"a": "b"}}
    csv_exporter.features.add(
        1,
        Feature(
            f_id=1,
            mz=123.45,
            samples={"d1", "d2"},
            networks={"abc": SimNetworks(algorithm="abc", network_id=0)},
            blank=True,
            groups={"abcde": {"a", "b", "c"}},
        ),
    )
    csv_exporter.features.entries[1].Annotations = Annotations(
        adducts=[
            Adduct(
                adduct_type="[M+H]+",
                partner_adduct="[M+NH4]+",
                partner_id=6,
                partner_mz=261.1445,
                diff_ppm=6,
            )
        ]
    )
    csv_exporter.features.entries[1].Annotations.losses = [
        NeutralLoss(
            id="Arg-oxazole(ribosomal, putatively from AAs R-S)",
            loss_det=224.1121,
            loss_ex=224.114,
            mz_frag=191.0975,
            diff=8.48,
        ),
    ]
    csv_exporter.features.entries[1].Annotations.matches = [
        Match(
            id="fakeomycin",
            algorithm="ms2deepscore",
            library="user-lib",
            score=0.9,
            mz=123.456,
            diff_mz=22.2,
            module="user_library_annotation",
        ),
        Match(
            id="fakeomycin",
            algorithm="modified_cosine",
            library="user-lib",
            score=0.9,
            mz=123.456,
            diff_mz=22.2,
            module="antismash_kcb_annotation",
        ),
        Match(
            id="fakeomycin",
            algorithm="ms2query",
            library="user-lib",
            score=0.9,
            mz=123.456,
            diff_mz=22.2,
            module="ms2query_annotation",
        ),
    ]
    csv_exporter.features.entries[1].Annotations.fragments = [
        CharFrag(
            id="ala-ala",
            frag_ex=123.456,
            frag_det=123.455,
            diff=10.0,
        )
    ]
    csv_exporter.stats.phenotypes = [
        PhenoData(
            datatype="qualitative",
            category="qualitative",
            f_ids_positive={
                1,
            },
        )
    ]
    return csv_exporter


@pytest.mark.slow
def test_run_valid(real_data_export):
    assert real_data_export.run("0.1.0", datetime.now()) is None
    for filename in glob.glob("tests/test_input_output/test_export_manager/dummy.*"):
        os.remove(filename)


@pytest.mark.slow
def test_write_raw_ms2query_results_valid(real_data_export):
    path = DefaultPaths().dirpath_ms2query_base.joinpath("results/f_queries.csv")
    path.touch(exist_ok=True)
    assert real_data_export.write_raw_ms2query_results() is None
    os.remove("tests/test_input_output/test_export_manager/dummy.ms2query_results.csv")


@pytest.mark.slow
def test_write_raw_ms2query_results_pass(real_data_export):
    MS2QueryAnnotator.remove_ms2query_temp_files()
    assert real_data_export.write_raw_ms2query_results() is None


@pytest.mark.slow
def test_write_cytoscape_output_valid(real_data_export):
    real_data_export.stats.networks = {
        "xyz": SpecSimNet(
            algorithm="xyz",
            subnetworks={},
            summary={1: set()},
            network=nx.Graph(),
        )
    }
    assert real_data_export.write_cytoscape_output() is None
    os.remove("tests/test_input_output/test_export_manager/dummy.fermo.xyz.graphml")


@pytest.mark.slow
def test_write_log_output_valid(real_data_export):
    path = Path("fermo_core/fermo_core.log")
    path.touch(exist_ok=True)
    assert real_data_export.write_log_output() is None
    os.remove("tests/test_input_output/test_export_manager/dummy.log")


@pytest.mark.slow
def test_write_csv_output_valid(real_data_export):
    assert real_data_export.write_csv_output() is None
    for filename in glob.glob("tests/test_input_output/test_export_manager/dummy.*"):
        os.remove(filename)


@pytest.mark.slow
def test_write_fermo_json(real_data_export):
    assert real_data_export.write_fermo_json("0.1.0", datetime.now()) is None
    os.remove("tests/test_input_output/test_export_manager/dummy.fermo.session.json")


def test_write_summary_output(real_data_export):
    assert real_data_export.write_summary_output() is None
    os.remove("tests/test_input_output/test_export_manager/dummy.summary.txt")


def test_export_metadata_json(json_exporter):
    json_exporter.export_metadata_json()
    assert json_exporter.session.get("metadata") is not None


def test_export_params_json(json_exporter):
    json_exporter.export_params_json()
    assert json_exporter.session.get("parameters") is not None


def test_export_stats_json(json_exporter):
    json_exporter.export_stats_json()
    assert json_exporter.session.get("stats") is not None


def test_export_features_json(json_exporter):
    json_exporter.export_features_json()
    assert json_exporter.session.get("general_features") is not None


def test_export_samples_json(json_exporter):
    json_exporter.export_samples_json()
    assert json_exporter.session.get("samples") is not None


def test_build_json_dict(json_exporter):
    json_exporter.build_json_dict()
    assert len(json_exporter.session) != 0


def test_return_session(json_exporter):
    session = json_exporter.return_session()
    assert session == {}


def test_add_activity_info_csv(csv_exporter):
    csv_exporter.add_activity_info_csv()
    assert csv_exporter.df.loc[0, "fermo:active"] == "true"


def test_add_blank_info_csv(csv_exporter):
    csv_exporter.add_blank_info_csv()
    assert csv_exporter.df.loc[0, "fermo:isblank"] == "true"


def test_add_sample_info_csv(csv_exporter):
    csv_exporter.add_sample_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:samples"], str)
    assert csv_exporter.df.loc[0, "fermo:samples:count"] == 2


def test_add_networks_info_csv(csv_exporter):
    csv_exporter.add_networks_info_csv()
    assert csv_exporter.df.loc[0, "fermo:networks:abc:network_id"] == 0


def test_add_adduct_info_csv(csv_exporter):
    csv_exporter.add_adduct_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:annotation:adducts"], str)


def test_add_loss_info_csv(csv_exporter):
    csv_exporter.add_loss_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:annotation:neutral_losses"], str)


def test_add_match_info_csv(csv_exporter):
    csv_exporter.add_match_info_csv()
    assert isinstance(
        csv_exporter.df.loc[0, "fermo:annotation:matches:user_library_annotation"], str
    )
    assert isinstance(
        csv_exporter.df.loc[0, "fermo:annotation:matches:ms2query_annotation"], str
    )
    assert isinstance(
        csv_exporter.df.loc[0, "fermo:annotation:matches:antismash_kcb_annotation"], str
    )


def test_add_fragment_info_csv(csv_exporter):
    csv_exporter.add_fragment_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:annotation:fragments"], str)


def test_add_group_info_csv(csv_exporter):
    csv_exporter.add_group_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:category:abcde"], str)


def test_add_phenotype_info_csv(csv_exporter):
    csv_exporter.add_phenotype_info_csv()
    assert isinstance(csv_exporter.df.loc[0, "fermo:phenotype:qualitative"], str)


def test_build_csv_output(csv_exporter):
    csv_exporter.build_csv_output()
    assert isinstance(csv_exporter.df.loc[0, "fermo:samples"], str)


def test_return_dfs_invalid(csv_exporter):
    csv_exporter.build_csv_output()
    with pytest.raises(KeyError):
        csv_exporter.return_dfs()
