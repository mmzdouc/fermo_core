import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_ms2deepscore_annotator import (
    Ms2deepscoreAnnotator,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def ms2deepscore_annotator():
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
            },
            intensity_from=0.0,
        ),
    )
    features = Repository()
    features.add(1, feature1)
    return Ms2deepscoreAnnotator(
        features=features,
        active_features={1},
        polarity="positive",
        library=library,
        library_name="dummy_library",
        max_time=100,
        score_cutoff=0.5,
        max_precursor_mass_diff=600,
    )


def test_prepare_queries_valid(ms2deepscore_annotator):
    ms2deepscore_annotator.prepare_queries()
    assert ms2deepscore_annotator.queries is not None


def test_prepare_queries_invalid(ms2deepscore_annotator):
    ms2deepscore_annotator.active_features = set()
    with pytest.raises(RuntimeError):
        ms2deepscore_annotator.prepare_queries()


def test_calculate_ms2deepscore_runtimeerror(ms2deepscore_annotator):
    with pytest.raises(RuntimeError):
        ms2deepscore_annotator.calculate_scores_ms2deepscore()


@pytest.mark.slow
def test_calculate_ms2deepscore_valid(ms2deepscore_annotator):
    ms2deepscore_annotator.prepare_queries()
    ms2deepscore_annotator.calculate_scores_ms2deepscore()
    assert ms2deepscore_annotator.scores is not None


@pytest.mark.slow
def test_filter_match_valid(ms2deepscore_annotator):
    ms2deepscore_annotator.prepare_queries()
    ms2deepscore_annotator.calculate_scores_ms2deepscore()
    sorted_matches = ms2deepscore_annotator.scores.scores_by_query(
        ms2deepscore_annotator.queries[0], name="MS2DeepScore", sort=True
    )
    assert ms2deepscore_annotator.filter_match(sorted_matches[0], 100.0)


@pytest.mark.slow
def test_filter_match_invalid(ms2deepscore_annotator):
    ms2deepscore_annotator.prepare_queries()
    ms2deepscore_annotator.score_cutoff = 1.0
    ms2deepscore_annotator.calculate_scores_ms2deepscore()
    sorted_matches = ms2deepscore_annotator.scores.scores_by_query(
        ms2deepscore_annotator.queries[0], name="MS2DeepScore", sort=True
    )
    assert ms2deepscore_annotator.filter_match(sorted_matches[0], 100.0) is False


def test_extract_userlib_scores_invalid(ms2deepscore_annotator):
    with pytest.raises(RuntimeError):
        ms2deepscore_annotator.extract_userlib_scores()


@pytest.mark.slow
def test_extract_userlib_scores_valid(ms2deepscore_annotator):
    ms2deepscore_annotator.prepare_queries()
    ms2deepscore_annotator.calculate_scores_ms2deepscore()
    ms2deepscore_annotator.extract_userlib_scores()
    features = ms2deepscore_annotator.return_features()
    assert features.entries[1].Annotations is not None
