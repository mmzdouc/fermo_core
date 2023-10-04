import pytest
from fermo_core.data_analysis.class_chrom_trace_calculator import ChromTraceData
from fermo_core.data_analysis.class_chrom_trace_calculator import ChromTraceCalculator
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


@pytest.fixture
def stats():
    stats = Stats()
    stats.samples = tuple(["sample1"])
    return stats


@pytest.fixture
def samples():
    feature1 = Feature()
    feature1.f_id = 1
    feature1.rt = 0.5
    feature1.rt_start = 0.0
    feature1.rt_stop = 1.0
    feature1.rt_range = 1.0
    feature1.fwhm = 0.5
    feature1.rel_intensity = 1.0
    feature1.intensity = 100

    sample1 = Sample()
    sample1.s_id = "sample1"
    sample1.feature_ids = tuple([1])
    sample1.max_intensity = 100
    sample1.features = {1: feature1}

    samples = Repository()
    samples.entries["sample1"] = sample1
    return samples


@pytest.fixture
def trace_rt():
    return 0.0, 0.12, 0.25, 0.5, 0.75, 0.88, 1.0


@pytest.fixture
def trace_int():
    return 0.0, 0.15, 0.5, 1.0, 0.5, 0.15, 0.0


def test_init_chrom_trace_data():
    assert isinstance(ChromTraceData(1, "sample1", 0.5, 0.0, 1.0), ChromTraceData)


def test_init_chrom_trace_calculator():
    assert isinstance(ChromTraceCalculator(), ChromTraceCalculator)


# test presence/absence of ChromTraceData attributes

# test negative examples


def test_modify_samples(samples, stats, trace_rt, trace_int):
    samples_mod = ChromTraceCalculator().modify_samples(samples, stats)
    assert samples_mod.entries["sample1"].features[1].trace_rt == trace_rt
    assert samples_mod.entries["sample1"].features[1].trace_int == trace_int


def test_modify_features_in_sample(samples, trace_rt, trace_int):
    sample1_mod = ChromTraceCalculator().modify_features_in_sample(
        samples.entries["sample1"]
    )
    assert sample1_mod.features[1].trace_rt == trace_rt
    assert sample1_mod.features[1].trace_int == trace_int
