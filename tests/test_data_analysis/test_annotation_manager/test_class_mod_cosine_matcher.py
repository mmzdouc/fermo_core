import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_mod_cosine_matcher import (
    ModCosineMatcher,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats, SpecLibEntry
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
        spectral_library={
            0: SpecLibEntry(
                name="fakeomycin",
                exact_mass=100.0,
                Spectrum=Utils.create_spectrum_object(
                    {
                        "mz": np.array([10, 40, 60], dtype=float),
                        "intens": np.array([10, 20, 100], dtype=float),
                        "f_id": 0,
                        "precursor_mz": 105.0,
                    }
                ),
            )
        },
    )
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array([10, 40, 60], dtype=float),
                "intens": np.array([10, 20, 100], dtype=float),
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


def test_subset_spectral_library_valid(mod_cosine_matcher):
    subset = mod_cosine_matcher.subset_spectral_library(Feature(mz=100.0))
    assert subset == {0}


def test_subset_spectral_library_invalid(mod_cosine_matcher):
    subset = mod_cosine_matcher.subset_spectral_library(Feature(mz=1000.0))
    assert subset == set()


def test_assign_matches_valid(mod_cosine_matcher):
    feature = mod_cosine_matcher.features.get(1)
    scores = matchms.calculate_scores(
        references=[mod_cosine_matcher.stats.spectral_library[0].Spectrum],
        queries=[feature.Spectrum],
        similarity_function=matchms.similarity.ModifiedCosine(tolerance=0.7),
    )
    feature = mod_cosine_matcher.assign_matches(feature, scores)
    assert feature.Annotations.matches[0].score == 1.0
