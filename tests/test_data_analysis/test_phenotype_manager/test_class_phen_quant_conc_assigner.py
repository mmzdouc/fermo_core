import pytest

from fermo_core.data_analysis.phenotype_manager.class_phen_quant_conc_assigner import (
    PhenQuantConcAssigner,
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
def phen_quant_conc():
    phen_quant_conc = PhenQuantConcAssigner(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )
    f1 = Feature(
        f_id=1,
        samples={"s1", "s2", "s3", "s4", "s5"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=100),
            SampleInfo(s_id="s2", value=10),
            SampleInfo(s_id="s3", value=1000),
            SampleInfo(s_id="s4", value=50),
            SampleInfo(s_id="s5", value=300),
        ],
    )
    f2 = Feature(
        f_id=2,
        samples={"s1", "s2", "s3", "s4", "s5"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=0),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=40),
            SampleInfo(s_id="s4", value=80),
            SampleInfo(s_id="s5", value=160),
        ],
    )
    phen_quant_conc.features.add(1, f1)
    phen_quant_conc.features.add(2, f2)
    phen_quant_conc.samples.add("s1", Sample(s_id="s1", feature_ids={1, 2}))
    phen_quant_conc.samples.add("s2", Sample(s_id="s2", feature_ids={1, 2}))
    phen_quant_conc.samples.add("s3", Sample(s_id="s3", feature_ids={1, 2}))
    phen_quant_conc.samples.add("s4", Sample(s_id="s4", feature_ids={1, 2}))
    phen_quant_conc.samples.add("s5", Sample(s_id="s5", feature_ids={1, 2}))
    phen_quant_conc.stats.active_features = (1, 2)
    phen_quant_conc.stats.samples = ("s1", "s2", "s3", "s4", "s5")
    phen_quant_conc.stats.phenotypes = [
        PhenoData(
            datatype="quantitative-concentration",
            category="assay:assay1",
            s_phen_data=[
                SamplePhenotype(s_id="s1", value=0),
                SamplePhenotype(s_id="s2", value=256),
                SamplePhenotype(s_id="s3", value=128),
                SamplePhenotype(s_id="s4", value=32),
                SamplePhenotype(s_id="s5", value=8),
            ],
        )
    ]
    return phen_quant_conc


def test_find_relevant_f_ids(phen_quant_conc):
    phen_quant_conc.find_relevant_f_ids()
    assert len(phen_quant_conc.relevant_f_ids) == 2


def test_calculate_correlation_valid(phen_quant_conc):
    phen_quant_conc.find_relevant_f_ids()
    phen_quant_conc.calculate_correlation()
    assert phen_quant_conc.features.entries[2].phenotypes[0] is not None


def test_calculate_correlation_0_cutoffs_valid(phen_quant_conc):
    phen_quant_conc.params.PhenoQuantConcAssgnParams.p_val_cutoff = 0
    phen_quant_conc.find_relevant_f_ids()
    phen_quant_conc.calculate_correlation()
    assert phen_quant_conc.features.entries[1].phenotypes[0] is not None


def test_calculate_correlation_invalid(phen_quant_conc):
    with pytest.raises(RuntimeError):
        phen_quant_conc.calculate_correlation()


def test_run_analysis_valid(phen_quant_conc):
    phen_quant_conc.run_analysis()
    assert phen_quant_conc.features.entries[2].phenotypes[0] is not None


def test_run_analysis_invalid(phen_quant_conc):
    phen_quant_conc.stats.phenotypes = None
    with pytest.raises(RuntimeError):
        phen_quant_conc.run_analysis()
