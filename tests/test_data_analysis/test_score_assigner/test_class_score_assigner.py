import pytest

from fermo_core.data_analysis.score_assigner.class_score_assigner import (
    ScoreAssigner,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    Phenotype,
    Annotations,
    Match,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats, SpecSimNet
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def score_assigner():
    score_assigner = ScoreAssigner(
        stats=Stats(
            samples=("s1",),
            networks={
                "modified_cosine": SpecSimNet(
                    algorithm="modified_cosine",
                    network={},
                    subnetworks={},
                    summary={"0": {1}, "1": {2}},
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
        phenotypes=[
            Phenotype(
                format="quantitative-concentration",
                category="assay:assay1",
                score=0.9,
                p_value=0.000005,
                p_value_corr=0.0005,
            )
        ],
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
            ]
        ),
    )
    score_assigner.features.add(1, f1)
    s1 = Sample(
        feature_ids={
            1,
        }
    )
    score_assigner.samples.add("s1", s1)
    score_assigner.stats.active_features = {1}
    return score_assigner


def test_assign_feature_scores_valid(score_assigner):
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype == 0.9
    assert round(score_assigner.features.entries[1].Scores.novelty, 1) == 0.1


def test_assign_feature_scores_phenotype_invalid(score_assigner):
    score_assigner.features.entries[1].phenotypes = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype is None
    assert round(score_assigner.features.entries[1].Scores.novelty, 1) == 0.1


def test_assign_feature_scores_novelty_invalid(score_assigner):
    score_assigner.features.entries[1].Annotations = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores.phenotype == 0.9
    assert score_assigner.features.entries[1].Scores.novelty is None


def test_assign_feature_scores_invalid(score_assigner):
    score_assigner.features.entries[1].Annotations = None
    score_assigner.features.entries[1].phenotypes = None
    score_assigner.assign_feature_scores()
    assert score_assigner.features.entries[1].Scores is None


def test_collect_sample_spec_networks_valid(score_assigner):
    score_assigner.collect_sample_spec_networks()
    assert score_assigner.networks["modified_cosine"]["s1"] == {0}


def test_collect_assign_sample_scores_valid(score_assigner):
    score_assigner.collect_sample_spec_networks()
    score_assigner.assign_sample_scores()
    assert score_assigner.networks["modified_cosine"]["s1"] == {0}
