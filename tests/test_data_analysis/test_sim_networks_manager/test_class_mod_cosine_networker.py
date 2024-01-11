import func_timeout
import matchms
import numpy as np
import pytest

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)


@pytest.fixture
def mock_feature_repo():
    feature1 = Feature()
    feature1.Spectrum = matchms.Spectrum(
        mz=np.array([1, 2, 3, 4, 5], dtype=float),
        intensities=np.array([1, 3, 5, 7, 9], dtype=float),
        metadata={"precursor_mz": 100.01, "id": 1},
    )
    feature2 = Feature()
    feature2.Spectrum = matchms.Spectrum(
        mz=np.array([1, 2, 3, 4, 5, 6], dtype=float),
        intensities=np.array([1, 3, 5, 7, 9, 11], dtype=float),
        metadata={"precursor_mz": 200.01, "id": 2},
    )
    feature_repo = Repository()
    feature_repo.add(1, feature1)
    feature_repo.add(2, feature2)
    return feature_repo


def test_init_mod_cosine_networker_valid():
    assert isinstance(ModCosineNetworker(), ModCosineNetworker)


def test_filter_input_spectra_valid(mock_feature_repo):
    params = SpecSimNetworkCosineParameters()
    mod_cosine_networker = ModCosineNetworker()
    output = mod_cosine_networker.filter_input_spectra(
        tuple([1, 2]), mock_feature_repo, params
    )
    assert output["included"] == {1, 2}


def test_filter_input_spectra_6_peaks_valid(mock_feature_repo):
    params = SpecSimNetworkCosineParameters()
    params.msms_min_frag_nr = 6
    mod_cosine_networker = ModCosineNetworker()
    output = mod_cosine_networker.filter_input_spectra(
        tuple([1, 2]), mock_feature_repo, params
    )
    assert output["excluded"] == {1}


def test_spec_sim_networking_valid(mock_feature_repo):
    params = SpecSimNetworkCosineParameters()
    mod_cosine_networker = ModCosineNetworker()
    scores = mod_cosine_networker.spec_sim_networking(
        tuple([1, 2]), mock_feature_repo, params
    )
    assert scores is not None


def test_spec_sim_networking_invalid(mock_feature_repo):
    params = SpecSimNetworkCosineParameters()
    mod_cosine_networker = ModCosineNetworker()

    params.maximum_runtime = 0.00000001

    with pytest.raises(func_timeout.FunctionTimedOut):
        mod_cosine_networker.spec_sim_networking(
            tuple([1, 2]), mock_feature_repo, params
        )


def test_create_network_valid(mock_feature_repo):
    params = SpecSimNetworkCosineParameters()
    mod_cosine_networker = ModCosineNetworker()
    scores = mod_cosine_networker.spec_sim_networking(
        tuple([1, 2]), mock_feature_repo, params
    )
    network = mod_cosine_networker.create_network(scores, params)
    assert network is not None
