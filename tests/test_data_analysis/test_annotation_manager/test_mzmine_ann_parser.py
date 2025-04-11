import pandas as pd
import pytest

from fermo_core.data_analysis.annotation_manager.class_mzmine_ann_parser import (
    MzmineAnnParser,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Annotations
from fermo_core.data_processing.parser.class_general_parser import GeneralParser
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def df_mzmine_ann():
    return pd.read_csv("tests/test_data/mzmine4_annot/mzmine4_ann.csv")


@pytest.fixture
def params_mzmine_annot():
    params_json = FileManager.load_json_file(
        "tests/test_data/mzmine4_annot/params.json"
    )
    params_manager = ParameterManager()
    params_manager.assign_parameters_cli(params_json)
    return params_manager


@pytest.fixture
def gp_mzmine_annot(params_mzmine_annot):
    general_parser = GeneralParser()
    general_parser.parse_parameters(params_mzmine_annot)
    return general_parser


@pytest.fixture
def mzmine_ann_p_inst(params_mzmine_annot, gp_mzmine_annot):
    stats, features, samples = gp_mzmine_annot.return_attributes()
    return MzmineAnnParser(params=params_mzmine_annot, stats=stats, features=features)


def test_init(mzmine_ann_p_inst):
    assert isinstance(mzmine_ann_p_inst, MzmineAnnParser)


def test_run_valid(mzmine_ann_p_inst):
    mzmine_ann_p_inst.run()
    features = mzmine_ann_p_inst.return_attributes()
    f = features.get(120)
    assert f.Annotations.adducts[0].adduct_type == "[M+NH4]+(mzmine)"


def test_contains_values_valid(mzmine_ann_p_inst, df_mzmine_ann):
    assert mzmine_ann_p_inst.contains_values(df_mzmine_ann.iloc[1])


def test_contains_values_fail(mzmine_ann_p_inst):
    df = pd.read_csv("tests/test_data/mzmine3/mzmine3.9.0.csv")
    assert not mzmine_ann_p_inst.contains_values(df.iloc[1])


def test_parse_ion_ident_valid(mzmine_ann_p_inst, df_mzmine_ann):
    mzmine_ann_p_inst.f.Annotations = Annotations()
    mzmine_ann_p_inst.parse_ion_ident(df_mzmine_ann.iloc[0], df_mzmine_ann)
    assert mzmine_ann_p_inst.f.Annotations.adducts[0].adduct_type == "[M+NH4]+(mzmine)"


def test_parse_ion_ident_fail(mzmine_ann_p_inst):
    df = pd.read_csv("tests/test_data/mzmine3/mzmine3.9.0.csv")
    mzmine_ann_p_inst.f.Annotations = Annotations()
    mzmine_ann_p_inst.parse_ion_ident(df.iloc[0], df)
    assert mzmine_ann_p_inst.f.Annotations.adducts is None


def test_parse_spectral_db_valid(mzmine_ann_p_inst, df_mzmine_ann):
    mzmine_ann_p_inst.f.Annotations = Annotations()
    mzmine_ann_p_inst.parse_spectral_db(
        df_mzmine_ann.iloc[0],
    )
    assert mzmine_ann_p_inst.f.Annotations.matches[0].id == "GLUTAMINE - 20.0 eV"
