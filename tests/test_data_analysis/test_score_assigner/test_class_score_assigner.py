import pytest

from fermo_core.data_analysis.score_assigner.class_score_assigner import ScoreAssigner
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Feature,
    Match,
    Phenotype,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import SpecSimNet, Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def score_assigner():
    score_assigner = ScoreAssigner(
        stats=Stats(
            samples=("s1", "s2", "s3"),
            networks={
                "modified_cosine": SpecSimNet(
                    algorithm="modified_cosine",
                    network={},
                    subnetworks={},
                    summary={"1": {1}, "2": {2}, "3": {3}, "4": {4}},
                )
            },
        ),
        features=Repository(),
        params=ParameterManager(),
        samples=Repository(),
    )
    f1 = Feature(
        f_id=1,
        samples={
            "s1",
        },
        Annotations=Annotations(
            matches=[
                Match(
                    score=0.9,
                    id="fakeomycin-A",
                    library="user-lib",
                    algorithm="modified cosine",
                    mz=123.456,
                    diff_mz=0.011,
                    module="library-annotation",
                ),
                Match(
                    score=0.7,
                    id="fakeomycin-B",
                    library="user-lib",
                    algorithm="modified cosine",
                    mz=123.456,
                    diff_mz=0.011,
                    module="library-annotation",
                ),
            ],
            phenotypes=[
                Phenotype(
                    format="quantitative-concentration",
                    category="assay:assay1",
                    score=0.9,
                    p_value=0.000005,
                    p_value_corr=0.0005,
                )
            ],
        ),
    )
    score_assigner.features.add(1, f1)
    f2 = Feature(
        f_id=2,
        samples={"s2"},
    )
    score_assigner.features.add(2, f2)
    f3 = Feature(
        f_id=3,
        samples={"s3"},
    )
    score_assigner.features.add(3, f3)
    s1 = Sample(feature_ids={1, 2})
    score_assigner.samples.add("s1", s1)
    s2 = Sample(feature_ids={2, 3})
    score_assigner.samples.add("s2", s2)
    s3 = Sample(feature_ids={2, 3})
    score_assigner.samples.add("s3", s3)
    score_assigner.stats.active_features = {1}
    return score_assigner


def test_assign_feature_scores_valid(score_assigner):
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype == 0.9
    assert round(score_assigner.features.entries[1].Scores.novelty, 1) == 0.1


def test_assign_feature_scores_phenotype_invalid(score_assigner):
    score_assigner.features.entries[1].Annotations.phenotypes = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype is None
    assert round(score_assigner.features.entries[1].Scores.novelty, 1) == 0.1


def test_assign_feature_scores_novelty_invalid(score_assigner):
    score_assigner.features.entries[1].Annotations.matches = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype == 0.9
    assert score_assigner.features.entries[1].Scores.novelty is None


def test_assign_feature_scores_invalid(score_assigner):
    score_assigner.features.entries[1].Annotations = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype is None


def test_collect_sample_spec_networks_valid(score_assigner):
    score_assigner.collect_sample_spec_networks()
    assert score_assigner.networks["modified_cosine"]["s1"] == {1, 2}
    assert score_assigner.samples.entries["s1"].networks["modified_cosine"] == {1, 2}


def test_collect_assign_sample_scores_valid(score_assigner):
    score_assigner.assign_feature_scores()
    score_assigner.collect_sample_spec_networks()
    score_assigner.assign_sample_scores()
    assert score_assigner.samples.entries["s1"].Scores.diversity == 0.5
    assert score_assigner.samples.entries["s1"].Scores.specificity == 0.25
    assert round(score_assigner.samples.entries["s1"].Scores.mean_novelty, 1) == 0.1
