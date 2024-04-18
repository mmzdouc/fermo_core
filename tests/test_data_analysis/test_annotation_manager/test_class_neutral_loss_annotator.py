import numpy as np
from pathlib import Path
import pytest

from fermo_core.data_analysis.annotation_manager.class_neutral_loss_annotator import (
    NeutralLossAnnotator,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature, Adduct
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import MsmsParameters
from fermo_core.input_output.core_module_parameter_managers import NeutralLossParameters
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def annotator_pos():
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array(
                    [167.9576, 242.978, 256.9275, 281.9894, 284.9765], dtype=float
                ),
                "intens": np.array([10, 20, 100, 15, 30], dtype=float),
                "f_id": 1,
                "precursor_mz": 300.0,
            },
            intensity_from=0.0,
        ),
    )
    features = Repository()
    features.add(1, feature1)
    stats = Stats(active_features={1})
    params = ParameterManager()
    params.MsmsParameters = MsmsParameters(
        filepath=Path("example_data/case_study_MSMS.mgf"),
        format="mgf",
        rel_int_from=0.0,
    )
    params.PeaktableParameters = PeaktableParameters(
        filepath=Path("example_data/case_study_peak_table_quant_full.csv"),
        format="mzmine3",
        polarity="positive",
    )
    params.NeutralLossParameters = NeutralLossParameters(nonbiological=True)
    return NeutralLossAnnotator(
        features=features, samples=Repository(), params=params, stats=stats
    )


@pytest.fixture
def annotator_neg():
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array(
                    [167.9576, 242.978, 256.9275, 281.9894, 284.9765], dtype=float
                ),
                "intens": np.array([10, 20, 100, 15, 30], dtype=float),
                "f_id": 1,
                "precursor_mz": 300.0,
            },
            intensity_from=0.0,
        ),
    )
    features = Repository()
    features.add(1, feature1)
    stats = Stats(active_features={1})
    params = ParameterManager()
    params.MsmsParameters = MsmsParameters(
        filepath=Path("example_data/case_study_MSMS.mgf"),
        format="mgf",
        rel_int_from=0.0,
    )
    params.PeaktableParameters = PeaktableParameters(
        filepath=Path("example_data/case_study_peak_table_quant_full.csv"),
        format="mzmine3",
        polarity="negative",
    )
    params.NeutralLossParameters = NeutralLossParameters(nonbiological=True)
    return NeutralLossAnnotator(
        features=features, samples=Repository(), params=params, stats=stats
    )


def test_run_analysis_valid(annotator_pos):
    annotator_pos.run_analysis()
    assert len(annotator_pos.features.entries[1].Annotations.losses) == 6


def test_annotate_feature_pos_valid(annotator_pos):
    annotator_pos.annotate_feature_pos(1)
    assert len(annotator_pos.features.entries[1].Annotations.losses) == 6


def test_validate_ribosomal_losses_valid(annotator_pos):
    feature = annotator_pos.features.get(1)
    feature = annotator_pos.validate_ribosomal_losses(feature)
    assert feature.Annotations.losses[0].id == "Glycine"
    assert feature.Annotations.classes["ribosomal"].aa_tags[0] == "G"


def test_validate_nonribosomal_losses_valid(annotator_pos):
    feature = annotator_pos.features.get(1)
    feature = annotator_pos.validate_nonribosomal_losses(feature)
    assert feature.Annotations.losses[0].id == "Ethanolamine"
    assert feature.Annotations.classes["nonribosomal"].monomer_tags[0] == "Eta"


def test_validate_glycosidic_losses_valid(annotator_pos):
    feature = annotator_pos.features.get(1)
    feature = annotator_pos.validate_glycoside_losses(feature)
    assert feature.Annotations.losses[0].id == "D-arabinose(C5H10O5)"
    assert feature.Annotations.classes["glycoside"].monomer_tags[0] == "D-arabinose"


def test_validate_gen_bio_pos_losses_valid(annotator_pos):
    feature = annotator_pos.features.get(1)
    feature = annotator_pos.validate_gen_bio_pos_losses(feature)
    assert feature.Annotations.losses[0].id == "Water(H2O)"


def test_validate_gen_other_pos_losses_valid(annotator_pos):
    feature = annotator_pos.features.get(1)
    feature = annotator_pos.validate_gen_other_pos_losses(feature)
    assert feature.Annotations.losses[0].id == "Methyl-radical(*CH3)"


def test_collect_evidence_ribosomal_pos_valid(annotator_pos):
    annotator_pos.annotate_feature_pos(1)
    annotator_pos.features.entries[1].Annotations.adducts = []
    annotator_pos.features.entries[1].Annotations.adducts.append(
        Adduct(
            adduct_type="[M+2H]2+",
            partner_adduct="[2M+H]+",
            partner_id=2,
            partner_mz=123.23,
            diff_ppm=10,
            sample="s_name",
        )
    )
    annotator_pos.collect_evidence_ribosomal_pos(1)
    feature = annotator_pos.features.entries[1]
    assert len(feature.Annotations.classes.get("ribosomal").evidence) == 2


def test_collect_evidence_nonribosomal_pos_valid(annotator_pos):
    annotator_pos.annotate_feature_pos(1)
    annotator_pos.features.entries[1].Annotations.adducts = []
    annotator_pos.features.entries[1].Annotations.adducts.append(
        Adduct(
            adduct_type="[M+2H]2+",
            partner_adduct="[2M+H]+",
            partner_id=2,
            partner_mz=123.23,
            diff_ppm=10,
            sample="s_name",
        )
    )
    annotator_pos.collect_evidence_nonribosomal_pos(1)
    feature = annotator_pos.features.entries[1]
    assert len(feature.Annotations.classes.get("nonribosomal").evidence) == 2


def test_collect_evidence_glycoside_pos_valid(annotator_pos):
    annotator_pos.annotate_feature_pos(1)
    annotator_pos.collect_evidence_glycoside_pos(1)
    feature = annotator_pos.features.entries[1]
    assert len(feature.Annotations.classes.get("glycoside").evidence) == 1


def test_run_analysis_neg_valid(annotator_neg):
    annotator_neg.run_analysis()
    assert len(annotator_neg.features.entries[1].Annotations.losses) == 2


def test_annotate_feature_neg(annotator_neg):
    annotator_neg.annotate_feature_neg(1)
    assert len(annotator_neg.features.entries[1].Annotations.losses) == 2


def test_validate_gen_other_neg_losses_valid(annotator_neg):
    feature = annotator_neg.features.get(1)
    feature = annotator_neg.validate_gen_other_neg_losses(feature)
    assert feature.Annotations.losses[0].id == "Methyl-radical(*CH3)"
