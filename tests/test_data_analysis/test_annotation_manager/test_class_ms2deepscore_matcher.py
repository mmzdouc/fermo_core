import func_timeout
import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_ms2deepscore_matcher import (
    Ms2deepscoreMatcher,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters
from fermo_core.input_output.input_file_parameter_managers import SpecLibParameters
from fermo_core.input_output.additional_module_parameter_managers import (
    SpectralLibMatchingDeepscoreParameters,
)
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def ms2deepscore_matcher():
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
    params.SpectralLibMatchingDeepscoreParameters = (
        SpectralLibMatchingDeepscoreParameters(activate_module=True)
    )
    params.PeaktableParameters = PeaktableParameters(
        filepath="example_data/case_study_peak_table_quant_full.csv",
        format="mzmine3",
        polarity="positive",
    )
    params.SpecLibParameters = SpecLibParameters(
        filepath="example_data/case_study_spectral_library.mgf", format="mgf"
    )
    return Ms2deepscoreMatcher(params=params, stats=stats, features=features)


@pytest.mark.slow
def test_run_analysis_valid(ms2deepscore_matcher):
    ms2deepscore_matcher.params.SpectralLibMatchingDeepscoreParameters.score_cutoff = (
        0.5
    )
    features = ms2deepscore_matcher.run_analysis()
    assert features.get(1).Annotations.matches[0].id == "fakeomycin"


def test_prepare_query_spectra_valid(ms2deepscore_matcher):
    query_spectra = ms2deepscore_matcher.prepare_query_spectra()
    assert query_spectra[0].metadata.get("id") == 1


@pytest.mark.slow
def test_calculate_scores_ms2deepscore_valid(ms2deepscore_matcher):
    query_spectra = ms2deepscore_matcher.prepare_query_spectra()
    scores = ms2deepscore_matcher.calculate_scores_ms2deepscore(query_spectra)
    assert isinstance(scores, matchms.Scores)


@pytest.mark.slow
def test_calculate_scores_ms2deepscore_timeout(ms2deepscore_matcher):
    query_spectra = ms2deepscore_matcher.prepare_query_spectra()
    ms2deepscore_matcher.params.SpectralLibMatchingDeepscoreParameters.maximum_runtime = (
        0.01
    )
    with pytest.raises(func_timeout.FunctionTimedOut):
        ms2deepscore_matcher.calculate_scores_ms2deepscore(query_spectra)


@pytest.mark.slow
def test_annotate_feature_valid(ms2deepscore_matcher):
    feature = ms2deepscore_matcher.features.get(1)
    query_spectra = ms2deepscore_matcher.prepare_query_spectra()
    ms2deepscore_matcher.params.SpectralLibMatchingDeepscoreParameters.score_cutoff = (
        0.5
    )
    scores = ms2deepscore_matcher.calculate_scores_ms2deepscore(query_spectra)
    sorted_matches = scores.scores_by_query(
        feature.Spectrum, name="MS2DeepScore", sort=True
    )
    feature = ms2deepscore_matcher.annotate_feature(feature, sorted_matches[0])
    assert feature.Annotations.matches[0].id == "fakeomycin"


@pytest.mark.slow
def test_annotate_feature_invalid(ms2deepscore_matcher):
    feature = ms2deepscore_matcher.features.get(1)
    query_spectra = ms2deepscore_matcher.prepare_query_spectra()
    ms2deepscore_matcher.params.SpectralLibMatchingDeepscoreParameters.score_cutoff = (
        1.0
    )
    scores = ms2deepscore_matcher.calculate_scores_ms2deepscore(query_spectra)
    sorted_matches = scores.scores_by_query(
        feature.Spectrum, name="MS2DeepScore", sort=True
    )
    feature = ms2deepscore_matcher.annotate_feature(feature, sorted_matches[0])
    assert feature.Annotations is None
