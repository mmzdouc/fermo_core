import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_mod_cos_annotator import (
    ModCosAnnotator,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def mod_cos_annotator():
    library = [
        matchms.Spectrum(
            mz=np.array([10, 45, 60], dtype=float),
            intensities=np.array([10, 30, 100], dtype=float),
            metadata={
                "precursor_mz": 105.0,
                "id": 0,
                "compound_name": "fakeomycin",
            },
            metadata_harmonization=True,
        )
    ]
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array([10, 40, 60, 80, 100], dtype=float),
                "intens": np.array([10, 20, 100, 15, 55], dtype=float),
                "f_id": 1,
                "precursor_mz": 100.0,
            }
        ),
    )
    features = Repository()
    features.add(1, feature1)
    return ModCosAnnotator(
        features=features,
        active_features={1},
        library=library,
        max_time=100,
        fragment_tol=0.1,
        score_cutoff=0.7,
        min_nr_matched_peaks=3,
        max_precursor_mass_diff=600,
    )


@pytest.mark.slow
def test_prepare_queries_valid(mod_cos_annotator):
    mod_cos_annotator.prepare_queries()
    assert mod_cos_annotator.queries is not None


@pytest.mark.slow
def test_prepare_queries_invalid(mod_cos_annotator):
    mod_cos_annotator.active_features = set()
    with pytest.raises(RuntimeError):
        mod_cos_annotator.prepare_queries()


@pytest.mark.slow
def test_calculate_scores_mod_cosine_runtimeerror(mod_cos_annotator):
    with pytest.raises(RuntimeError):
        mod_cos_annotator.calculate_scores_mod_cosine()


@pytest.mark.slow
def test_calculate_scores_mod_cosine_valid(mod_cos_annotator):
    mod_cos_annotator.prepare_queries()
    mod_cos_annotator.calculate_scores_mod_cosine()
    assert mod_cos_annotator.scores is not None


@pytest.mark.slow
def test_filter_match_valid(mod_cos_annotator):
    mod_cos_annotator.prepare_queries()
    mod_cos_annotator.calculate_scores_mod_cosine()
    scores = mod_cos_annotator.return_scores()
    sorted_matches = scores.scores_by_query(
        mod_cos_annotator.queries[0], name="ModifiedCosine_score", sort=True
    )
    assert mod_cos_annotator.filter_match(sorted_matches[0], 100.0)


@pytest.mark.slow
def test_filter_match_invalid(mod_cos_annotator):
    mod_cos_annotator.prepare_queries()
    mod_cos_annotator.score_cutoff = 1.0
    mod_cos_annotator.calculate_scores_mod_cosine()
    scores = mod_cos_annotator.return_scores()
    sorted_matches = scores.scores_by_query(
        mod_cos_annotator.queries[0], name="ModifiedCosine_score", sort=True
    )
    assert mod_cos_annotator.filter_match(sorted_matches[0], 100.0) is False
