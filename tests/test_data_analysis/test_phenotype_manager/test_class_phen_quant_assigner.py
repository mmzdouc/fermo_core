import pytest

from fermo_core.data_analysis.phenotype_manager.class_phen_quant_assigner import (
    PhenQuantAssigner,
)
from fermo_core.data_processing.class_stats import Stats, PhenoData, SamplePhenotype
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def phen_quant():
    phen_quant = PhenQuantAssigner(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )
    f1 = Feature(
        f_id=1,
        samples={
            "s1",
        },
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=100),
        ],
    )
    f2 = Feature(
        f_id=2,
        samples={"s1", "s2"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
            SampleInfo(s_id="s2", value=1),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=100),
            SampleInfo(s_id="s2", value=10),
        ],
    )
    f3 = Feature(
        f_id=3,
        samples={
            "s2",
        },
        area_per_sample=[
            SampleInfo(s_id="s2", value=10),
        ],
        height_per_sample=[
            SampleInfo(s_id="s2", value=100),
        ],
    )
    phen_quant.features.add(1, f1)
    phen_quant.features.add(2, f2)
    phen_quant.features.add(3, f3)
    s1 = Sample(s_id="s1", feature_ids={1, 2})
    s2 = Sample(s_id="s2", feature_ids={2, 3})
    phen_quant.samples.add("s1", s1)
    phen_quant.samples.add("s2", s2)
    phen_quant.stats.active_features = {1, 2, 3}
    phen_quant.stats.samples = ("s1", "s2")
    phen_quant.stats.phenotypes = [
        PhenoData(
            datatype="qualitative",
            category="qualitative",
            s_negative={
                "s2",
            },
            s_phen_data=[SamplePhenotype(s_id="s1")],
        )
    ]
    return phen_quant


def test_collect_sets_valid(phen_quant):
    phen_quant.collect_sets()
    assert len(phen_quant.f_ids_intersect) == 1


def test_collect_sets_invalid(phen_quant):
    phen_quant.samples.entries["s1"].feature_ids = {
        1,
    }
    phen_quant.collect_sets()
    assert len(phen_quant.f_ids_intersect) == 0


def test_get_value_valid(phen_quant):
    vals = phen_quant.get_value(2, {"s1", "s2"})
    assert len(vals) == 2


def test_get_value_invalid(phen_quant):
    with pytest.raises(RuntimeError):
        phen_quant.get_value(1, {"s2"})


def test_bin_intersection_positive(phen_quant):
    phen_quant.f_ids_intersect = {
        2,
    }
    phen_quant.bin_intersection()
    assert len(phen_quant.stats.phenotypes[0].f_ids_positive) == 1


def test_bin_intersection_negative(phen_quant):
    phen_quant.f_ids_intersect = {
        2,
    }
    phen_quant.features.entries[2].area_per_sample = [
        SampleInfo(s_id="s1", value=10),
        SampleInfo(s_id="s2", value=10),
    ]
    phen_quant.bin_intersection()
    assert len(phen_quant.stats.phenotypes[0].f_ids_positive) == 0
