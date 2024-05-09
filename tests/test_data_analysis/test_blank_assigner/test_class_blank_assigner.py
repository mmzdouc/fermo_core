import pytest

from fermo_core.data_analysis.blank_assigner.class_blank_assigner import BlankAssigner
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def blank_assigner():
    blank_assigner = BlankAssigner(
        params=ParameterManager(), stats=Stats(), features=Repository()
    )
    f1 = Feature(
        f_id=1,
        area_per_sample=[
            SampleInfo(s_id="s1", value=1),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=30),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=300),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=10),
        ],
    )
    blank_assigner.features.add(1, f1)
    blank_assigner.stats.active_features = {1}
    return blank_assigner


def test_calc_rprsnt_mean_valid(blank_assigner):
    blank_assigner.params.BlankAssignmentParameters.algorithm = "mean"
    assert blank_assigner.calc_rprsnt([10, 20, 30]) == 20


def test_calc_rprsnt_median_valid(blank_assigner):
    blank_assigner.params.BlankAssignmentParameters.algorithm = "median"
    assert blank_assigner.calc_rprsnt([10, 30, 50]) == 30


def test_calc_rprsnt_maximum_valid(blank_assigner):
    blank_assigner.params.BlankAssignmentParameters.algorithm = "maximum"
    assert blank_assigner.calc_rprsnt([10, 20, 50]) == 50


def test_calc_rprsnt_invalid(blank_assigner):
    blank_assigner.params.BlankAssignmentParameters.algorithm = "aaasdasdf"
    with pytest.raises(RuntimeError):
        blank_assigner.calc_rprsnt([10, 20, 50])


def test_collect_area_valid(blank_assigner):
    blank_assigner.stats.GroupMData.blank_s_ids = {"s1"}
    non_blk, blk = blank_assigner.collect_area(1)
    assert len(non_blk) == 2
    assert len(blk) == 1


def test_collect_area_invalid(blank_assigner):
    with pytest.raises(RuntimeError):
        blank_assigner.collect_area(1)


def test_collect_height_valid(blank_assigner):
    blank_assigner.stats.GroupMData.blank_s_ids = {"s1"}
    non_blk, blk = blank_assigner.collect_height(1)
    assert len(non_blk) == 2
    assert len(blk) == 1


def test_collect_height_invalid(blank_assigner):
    with pytest.raises(RuntimeError):
        blank_assigner.collect_height(1)


def test_determine_blank_nonblank(blank_assigner):
    blank_assigner.features.entries[1].samples = {"s1", "s2"}
    blank_assigner.stats.GroupMData.nonblank_s_ids.update({"s1", "s2"})
    blank_assigner.stats.GroupMData.blank_s_ids.add("s3")
    blank_assigner.determine_blank()
    assert blank_assigner.stats.GroupMData.nonblank_f_ids == {1}
    assert blank_assigner.features.entries[1].blank is False


def test_determine_blank_blank(blank_assigner):
    blank_assigner.features.entries[1].samples = {"s1", "s2"}
    blank_assigner.stats.GroupMData.blank_s_ids.update({"s1", "s2"})
    blank_assigner.stats.GroupMData.nonblank_s_ids.add("s3")
    blank_assigner.determine_blank()
    assert blank_assigner.stats.GroupMData.blank_f_ids == {1}
    assert blank_assigner.features.entries[1].blank is True


def test_determine_blank_comparison_nonblank(blank_assigner):
    blank_assigner.features.entries[1].samples = {"s1", "s2", "s3"}
    blank_assigner.stats.GroupMData.blank_s_ids.add("s1")
    blank_assigner.stats.GroupMData.nonblank_s_ids.update({"s2", "s3"})
    blank_assigner.params.BlankAssignmentParameters.algorithm = "mean"
    blank_assigner.params.BlankAssignmentParameters.value = "area"
    blank_assigner.determine_blank()
    assert blank_assigner.stats.GroupMData.nonblank_f_ids == {1}
    assert blank_assigner.features.entries[1].blank is False


def test_determine_blank_comparison_blank(blank_assigner):
    blank_assigner.features.entries[1].samples = {"s1", "s2", "s3"}
    blank_assigner.stats.GroupMData.blank_s_ids.add("s1")
    blank_assigner.stats.GroupMData.nonblank_s_ids.update({"s2", "s3"})
    blank_assigner.params.BlankAssignmentParameters.algorithm = "mean"
    blank_assigner.params.BlankAssignmentParameters.value = "height"
    blank_assigner.determine_blank()
    assert blank_assigner.stats.GroupMData.blank_f_ids == {1}
    assert blank_assigner.features.entries[1].blank is True


def test_validate_assignment_valid(blank_assigner):
    blank_assigner.stats.GroupMData.blank_f_ids.add(1)
    assert blank_assigner.validate_assignment() is None


def test_validate_assignment_invalid(blank_assigner):
    with pytest.raises(RuntimeError):
        blank_assigner.validate_assignment()


def test_run_analysis_invalid(blank_assigner):
    blank_assigner.stats.active_features = set()
    blank_assigner.run_analysis()
    assert len(blank_assigner.stats.GroupMData.blank_f_ids) == 0
