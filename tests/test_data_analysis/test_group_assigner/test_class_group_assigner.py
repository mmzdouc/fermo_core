import pytest

from fermo_core.data_analysis.group_assigner.class_group_assigner import GroupAssigner
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats, Group, GroupMData


@pytest.fixture
def group_assigner():
    group_assigner = GroupAssigner(stats=Stats(), features=Repository())
    f1 = Feature(
        f_id=1,
        samples={
            "s1",
        },
    )
    group_assigner.stats.GroupMData = GroupMData(
        ctgrs={"phenotype": {"G": Group(s_ids={"s1", "s2"}, f_ids=set())}},
    )
    group_assigner.features.add(1, f1)
    group_assigner.stats.active_features = {1}
    return group_assigner


def test_assign_groups_valid(group_assigner):
    group_assigner.assign_groups()
    assert group_assigner.stats.GroupMData.ctgrs["phenotype"]["G"].f_ids == {
        1,
    }
    assert group_assigner.features.entries[1].groups["phenotype"] == {
        "G",
    }


def test_assign_groups_invalid(group_assigner):
    group_assigner.features.entries[1].samples = {
        "different_sample",
    }
    group_assigner.assign_groups()
    assert group_assigner.features.entries[1].groups == {}
