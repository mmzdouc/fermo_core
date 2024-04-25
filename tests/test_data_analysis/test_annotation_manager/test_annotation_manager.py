import pytest

from fermo_core.data_analysis.annotation_manager.class_annotation_manager import (
    AnnotationManager,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Match,
    Adduct,
    NeutralLoss,
)


@pytest.fixture
def annotation_manager_instance(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return AnnotationManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


@pytest.mark.slow
def test_init_valid(annotation_manager_instance):
    assert isinstance(annotation_manager_instance, AnnotationManager)


@pytest.mark.slow
def test_run_user_lib_mod_cosine_matching_valid(annotation_manager_instance):
    annotation_manager_instance.run_user_lib_mod_cosine_matching()
    assert isinstance(
        annotation_manager_instance.features.get(79).Annotations.matches[0], Match
    )


@pytest.mark.slow
def test_run_user_lib_ms2deepscore_matching_valid(annotation_manager_instance):
    annotation_manager_instance.run_user_lib_ms2deepscore_matching()
    assert isinstance(
        annotation_manager_instance.features.get(79).Annotations.matches[0], Match
    )


@pytest.mark.slow
def test_run_feature_adduct_annotation_valid(annotation_manager_instance):
    annotation_manager_instance.run_feature_adduct_annotation()
    assert isinstance(
        annotation_manager_instance.features.get(131).Annotations.adducts[0], Adduct
    )


@pytest.mark.slow
def test_run_neutral_loss_annotation_valid(annotation_manager_instance):
    annotation_manager_instance.run_neutral_loss_annotation()
    assert isinstance(
        annotation_manager_instance.features.get(83).Annotations.losses[0], NeutralLoss
    )


@pytest.mark.high_cpu
def test_run_ms2query_annotation_valid(annotation_manager_instance):
    annotation_manager_instance.run_ms2query_annotation()
    assert isinstance(
        annotation_manager_instance.features.get(13).Annotations.matches[0], Match
    )
    # TODO (MMZ 25.4.24): look which one is chymostatinol
