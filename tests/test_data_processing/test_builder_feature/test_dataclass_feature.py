import matchms
import numpy as np

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_feature.dataclass_feature import SimNetworks


def test_init_feature_valid():
    assert isinstance(Feature(), Feature)


def test_init_sim_networks_valid():
    assert isinstance(SimNetworks(algorithm="mod_cosine", network_id=0), SimNetworks)


def test_to_json_f_id_valid():
    feature = Feature()
    feature.f_id = 1
    f_dict = feature.to_json()
    assert f_dict.get("f_id") == 1


def test_to_json_spectrum_valid():
    feature = Feature()
    feature.Spectrum = matchms.Spectrum(
        mz=np.array([1, 2, 3], dtype=float),
        intensities=np.array([10, 10, 10], dtype=float),
        metadata={"precursor_mz": 100.01, "id": 1},
        metadata_harmonization=False,
    )
    feature.Spectrum = matchms.filtering.add_precursor_mz(feature.Spectrum)
    feature.Spectrum = matchms.filtering.normalize_intensities(feature.Spectrum)
    f_dict = feature.to_json()
    assert isinstance(f_dict.get("spectrum"), dict)


def test_to_json_networks_valid():
    feature = Feature()
    feature.networks = {0: SimNetworks(algorithm="xyz", network_id=0)}
    f_dict = feature.to_json()
    assert f_dict.get("networks").get(0).get("algorithm") == "xyz"
