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
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def annotator():
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array([10, 42.978, 56.9275, 80, 100], dtype=float),
                "intens": np.array([10, 20, 100, 15, 55], dtype=float),
                "f_id": 1,
                "precursor_mz": 100.0,
            }
        ),
    )
    features = Repository()
    features.add(1, feature1)
    stats = Stats(active_features={1})
    params = ParameterManager()
    params.MsmsParameters = MsmsParameters(
        filepath=Path("example_data/case_study_MSMS.mgf"), format="mgf"
    )
    return NeutralLossAnnotator(
        features=features, samples=Repository(), params=params, stats=stats
    )


def test_run_analysis_valid(annotator):
    annotator.run_analysis()
    assert len(annotator.features.entries[1].Annotations.losses) == 2


def test_annotate_feature_valid(annotator):
    annotator.annotate_feature(1)
    assert len(annotator.features.entries[1].Annotations.losses) == 2


def test_validate_ribosomal_losses_valid(annotator):
    feature = annotator.features.get(1)
    feature = annotator.setup_storage(feature)
    feature = annotator.validate_ribosomal_losses(feature)
    assert feature.Annotations.losses[0].id == "Glycine"
    assert feature.Annotations.classes["ribosomal"].aa_tags[0] == "G"
    # assert isinstance(feature.Annotations.classes["ribosomal"].evidence[0], str)


def test_validate_nonribosomal_losses_valid(annotator):
    feature = annotator.features.get(1)
    feature = annotator.setup_storage(feature)
    feature = annotator.validate_nonribosomal_losses(feature)
    assert feature.Annotations.losses[0].id == "Ethanolamine"
    assert feature.Annotations.classes["nonribosomal"].monomer_tags[0] == "Eta"


def test_collect_evidence(annotator):
    annotator.annotate_feature(1)
    annotator.features.entries[1].Annotations.adducts.append(
        Adduct(
            adduct_type="[M+2H]2+",
            partner_adduct="[2M+H]+",
            partner_id=2,
            partner_mz=123.23,
            diff_ppm=1,
            sample="s_name",
        )
    )
    annotator.collect_evidence(1)
    assert (
        len(annotator.features.entries[1].Annotations.classes.get("ribosomal").evidence)
        == 2
    )
