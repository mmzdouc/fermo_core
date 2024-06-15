import pytest

from fermo_core.data_analysis.class_analysis_manager import AnalysisManager


@pytest.fixture
def analysis_manager_instance(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return AnalysisManager(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


def test_init_valid(analysis_manager_instance):
    assert isinstance(analysis_manager_instance, AnalysisManager)


def test_return_valid(analysis_manager_instance):
    stats, features, samples, params = analysis_manager_instance.return_attributes()
    assert stats is not None


@pytest.mark.slow
def test_analyze_valid(analysis_manager_instance):
    analysis_manager_instance.analyze()
    value = (
        analysis_manager_instance.samples.get("5440_5439_mod.mzXML")
        .features.get(1)
        .trace_rt
    )
    assert isinstance(value, tuple)


@pytest.mark.slow
def test_run_blank_assignment_valid(analysis_manager_instance):
    analysis_manager_instance.run_blank_assignment()
    assert len(analysis_manager_instance.stats.GroupMData.blank_f_ids) != 0


def test_run_blank_assignment_invalid_file(analysis_manager_instance):
    analysis_manager_instance.params.GroupMetadataParameters = None
    analysis_manager_instance.run_blank_assignment()
    assert len(analysis_manager_instance.stats.GroupMData.blank_f_ids) == 0


def test_run_blank_assignment_invalid_blanks(analysis_manager_instance):
    analysis_manager_instance.stats.GroupMData.blank_s_ids = set()
    analysis_manager_instance.run_blank_assignment()
    assert len(analysis_manager_instance.stats.GroupMData.blank_f_ids) == 0


def test_run_blank_assignment_invalid_nonblanks(analysis_manager_instance):
    analysis_manager_instance.stats.GroupMData.nonblank_s_ids = set()
    analysis_manager_instance.run_blank_assignment()
    assert len(analysis_manager_instance.stats.GroupMData.blank_f_ids) == 0


def test_run_blank_assignment_invalid_switched_off(analysis_manager_instance):
    analysis_manager_instance.params.BlankAssignmentParameters.activate_module = False
    analysis_manager_instance.run_blank_assignment()
    assert len(analysis_manager_instance.stats.GroupMData.blank_f_ids) == 0


def test_run_group_assignment_invalid_file(analysis_manager_instance):
    analysis_manager_instance.params.GroupMetadataParameters = None
    analysis_manager_instance.run_group_assignment()
    assert (
        len(analysis_manager_instance.stats.GroupMData.ctgrs["phylogroup"]["A2"].f_ids)
        == 0
    )


def test_run_group_factor_assignment_invalid(analysis_manager_instance):
    analysis_manager_instance.run_group_factor_assignment()
    assert analysis_manager_instance.features.entries[13].group_factors is None


def test_run_phenotype_manager_valid(analysis_manager_instance):
    analysis_manager_instance.run_phenotype_manager()
    assert 82 in analysis_manager_instance.stats.phenotypes[0].f_ids_positive


def test_run_score_assignment_valid(analysis_manager_instance):
    analysis_manager_instance.run_score_assignment()
    assert analysis_manager_instance.features.entries[13].Scores is not None
