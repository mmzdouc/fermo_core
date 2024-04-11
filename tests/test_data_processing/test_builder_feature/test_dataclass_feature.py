import matchms
import numpy as np

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_feature.dataclass_feature import SimNetworks
from fermo_core.data_processing.builder_feature.dataclass_feature import Annotations
from fermo_core.data_processing.builder_feature.dataclass_feature import Adduct
from fermo_core.data_processing.builder_feature.dataclass_feature import Match


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


def test_to_json_adducts_valid():
    feature = Feature()
    feature.Annotations = Annotations()
    feature.Annotations.adducts = [
        Adduct(
            adduct_type="[M+Na]+",
            partner=2,
            diff_expected=100.01,
            diff_observed=100.5,
            diff_ppm=5.5,
        )
    ]
    f_dict = feature.to_json()
    assert f_dict["annotations"]["adducts"][0]["adduct_type"] == "[M+Na]+"


def test_to_json_matches_valid():
    feature = Feature()
    feature.Annotations = Annotations()
    feature.Annotations.matches = [
        Match(
            id="fakeomycin",
            library="default_library",
            algorithm="modified cosine",
            score=0.99,
            mz=1234.5,
            diff_mz=300.2,
            module="user-library-matching",
        )
    ]
    f_dict = feature.to_json()
    assert f_dict["annotations"]["matches"][0]["id"] == "fakeomycin"
