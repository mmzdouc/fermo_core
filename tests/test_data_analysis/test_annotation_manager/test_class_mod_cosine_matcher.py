import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_mod_cosine_matcher import (
    ModCosineMatcher,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import SpecLibParameters
from fermo_core.input_output.additional_module_parameter_managers import (
    SpectralLibMatchingCosineParameters,
)
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def mod_cosine_matcher():
    stats = Stats(
        active_features={1},
        spectral_library=[
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
        ],
    )
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
    params = ParameterManager()
    params.SpectralLibMatchingCosineParameters = SpectralLibMatchingCosineParameters(
        activate_module=True, min_nr_matched_peaks=3
    )
    params.SpecLibParameters = SpecLibParameters(
        filepath="example_data/case_study_spectral_library.mgf", format="mgf"
    )
    return ModCosineMatcher(params=params, stats=stats, features=features)


def test_run_analysis(mod_cosine_matcher):
    features = mod_cosine_matcher.run_analysis()
    assert features.get(1).Annotations.matches[0].id == "fakeomycin"


def test_prepare_query_spectra_valid(mod_cosine_matcher):
    query_spectra = mod_cosine_matcher.prepare_query_spectra()
    assert query_spectra[0].metadata.get("id") == 1


def test_annotate_feature_valid(mod_cosine_matcher):
    feature = mod_cosine_matcher.features.get(1)
    scores = matchms.calculate_scores(
        references=[mod_cosine_matcher.stats.spectral_library[0]],
        queries=[feature.Spectrum],
        similarity_function=matchms.similarity.ModifiedCosine(tolerance=0.1),
    )
    sorted_matches = scores.scores_by_query(
        feature.Spectrum, name="ModifiedCosine_score", sort=True
    )
    feature = mod_cosine_matcher.annotate_feature(feature, sorted_matches[0])
    assert feature.Annotations.matches[0].id == "fakeomycin"


def test_annotate_feature_invalid(mod_cosine_matcher):
    feature = mod_cosine_matcher.features.get(1)
    scores = matchms.calculate_scores(
        references=[mod_cosine_matcher.stats.spectral_library[0]],
        queries=[feature.Spectrum],
        similarity_function=matchms.similarity.ModifiedCosine(tolerance=0.1),
    )
    sorted_matches = scores.scores_by_query(
        feature.Spectrum, name="ModifiedCosine_score", sort=True
    )
    mod_cosine_matcher.params.SpectralLibMatchingCosineParameters.score_cutoff = 1.0
    feature = mod_cosine_matcher.annotate_feature(feature, sorted_matches[0])
    assert feature.Annotations is None
