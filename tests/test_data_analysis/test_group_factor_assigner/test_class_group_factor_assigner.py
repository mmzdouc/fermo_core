import pytest

from fermo_core.data_analysis.group_factor_assigner.class_group_factor_assigner import (
    GroupFactorAssigner,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Group, Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.param_handlers import (
    GroupFactAssignmentParameters,
    GroupMetadataParameters,
)


@pytest.fixture
def gfact_assigner():
    gfact_assigner = GroupFactorAssigner(
        params=ParameterManager(), stats=Stats(), features=Repository()
    )
    f1 = Feature(
        f_id=1,
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=30),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=10),
            SampleInfo(s_id="s2", value=10),
            SampleInfo(s_id="s3", value=100),
        ],
        groups={"cat1": {"gr1", "gr2"}},
        samples={"s1", "s2", "s3"},
    )
    gfact_assigner.stats.GroupMData.ctgrs = {
        "cat1": {
            "gr1": Group(s_ids={"s1", "s2"}),
            "gr2": Group(
                s_ids={
                    "s3",
                }
            ),
        }
    }
    gfact_assigner.params.GroupMetadataParameters = GroupMetadataParameters(
        **{"filepath": "tests/test_data/test.group_metadata.csv", "format": "fermo"}
    )
    gfact_assigner.params.GroupFactAssignmentParameters = GroupFactAssignmentParameters(
        **{"activate_module": True, "algorithm": "mean", "value": "area"}
    )
    gfact_assigner.features.add(1, f1)
    gfact_assigner.stats.active_features = {1}
    return gfact_assigner


def test_calc_rprsnt_mean_valid(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.algorithm = "mean"
    assert gfact_assigner.calc_rprsnt([10, 20, 30]) == 20


def test_calc_rprsnt_median_valid(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.algorithm = "median"
    assert gfact_assigner.calc_rprsnt([10, 30, 50]) == 30


def test_calc_rprsnt_maximum_valid(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.algorithm = "maximum"
    assert gfact_assigner.calc_rprsnt([10, 20, 50]) == 50


def test_calc_rprsnt_invalid(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.algorithm = "aaasdasdf"
    with pytest.raises(RuntimeError):
        gfact_assigner.calc_rprsnt([10, 20, 50])


def test_get_value(gfact_assigner):
    value = gfact_assigner.get_value(1, {"s1", "s2", "s3"})
    assert value == [10, 20, 30]


def test_get_value_height(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.value = "height"
    value = gfact_assigner.get_value(1, {"s1", "s2", "s3"})
    assert value == [10, 10, 100]


def test_assign_group_factors_valid(gfact_assigner):
    gfact_assigner.assign_group_factors()
    assert gfact_assigner.features.entries[1].group_factors["cat1"][0].factor == 2.0


def test_assign_group_factors_height_valid(gfact_assigner):
    gfact_assigner.params.GroupFactAssignmentParameters.value = "height"
    gfact_assigner.assign_group_factors()
    assert gfact_assigner.features.entries[1].group_factors["cat1"][0].factor == 10


def test_run_analysis_valid(gfact_assigner):
    gfact_assigner.run_analysis()
    assert gfact_assigner.features.entries[1].group_factors["cat1"][0].factor == 2.0


def test_run_analysis_invalid(gfact_assigner):
    gfact_assigner.stats.active_features = set()
    gfact_assigner.run_analysis()
    assert gfact_assigner.features.entries[1].group_factors is None
