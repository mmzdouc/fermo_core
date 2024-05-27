import pytest

from fermo_core.data_analysis.phenotype_manager.class_phen_quant_perc_assigner import (
    PhenQuantPercAssigner,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import PhenoData, SamplePhenotype, Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def phen_quant_perc():
    phen_quant_perc = PhenQuantPercAssigner(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )
    f1 = Feature(
        f_id=1,
        samples={"s1", "s2", "s3", "s4"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=100),
            SampleInfo(s_id="s2", value=10),
            SampleInfo(s_id="s3", value=1000),
            SampleInfo(s_id="s4", value=50),
        ],
    )
    f2 = Feature(
        f_id=2,
        samples={"s1", "s2", "s3", "s4"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
            SampleInfo(s_id="s2", value=100),
            SampleInfo(s_id="s3", value=1000),
            SampleInfo(s_id="s4", value=10000),
        ],
    )
    phen_quant_perc.features.add(1, f1)
    phen_quant_perc.features.add(2, f2)
    s1 = Sample(s_id="s1", feature_ids={1, 2})
    s2 = Sample(s_id="s2", feature_ids={1, 2})
    s3 = Sample(s_id="s3", feature_ids={1, 2})
    s4 = Sample(s_id="s4", feature_ids={1, 2})
    phen_quant_perc.samples.add("s1", s1)
    phen_quant_perc.samples.add("s2", s2)
    phen_quant_perc.samples.add("s3", s3)
    phen_quant_perc.samples.add("s4", s4)
    phen_quant_perc.stats.active_features = {1, 2}
    phen_quant_perc.stats.samples = ("s1", "s2", "s3", "s4")
    phen_quant_perc.stats.phenotypes = [
        PhenoData(
            datatype="quantitative-percentage",
            category="assay:assay1",
            s_phen_data=[
                SamplePhenotype(s_id="s1", value=0),
                SamplePhenotype(s_id="s2", value=1),
                SamplePhenotype(s_id="s3", value=10),
                SamplePhenotype(s_id="s4", value=100),
            ],
        )
    ]
    return phen_quant_perc


def test_find_relevant_f_ids(phen_quant_perc):
    phen_quant_perc.find_relevant_f_ids()
    assert len(phen_quant_perc.relevant_f_ids) == 2


def test_calculate_correlation_valid(phen_quant_perc):
    phen_quant_perc.find_relevant_f_ids()
    phen_quant_perc.calculate_correlation()
    assert phen_quant_perc.features.entries[2].Annotations.phenotypes[0] is not None


def test_calculate_correlation_invalid(phen_quant_perc):
    with pytest.raises(RuntimeError):
        phen_quant_perc.calculate_correlation()


def test_run_analysis_valid(phen_quant_perc):
    phen_quant_perc.run_analysis()
    assert phen_quant_perc.features.entries[2].Annotations.phenotypes[0] is not None


def test_run_analysis_invalid(phen_quant_perc):
    phen_quant_perc.stats.phenotypes = None
    with pytest.raises(RuntimeError):
        phen_quant_perc.run_analysis()
