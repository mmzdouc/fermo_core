import matchms
import numpy as np

from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Adduct,
    Annotations,
    CharFrag,
    Feature,
    GroupFactor,
    Match,
    NeutralLoss,
    Phenotype,
    SampleInfo,
    Scores,
    SimNetworks,
)


def test_init_feature_valid():
    assert isinstance(Feature(), Feature)


def test_init_sim_networks_valid():
    assert isinstance(SimNetworks(algorithm="mod_cosine", network_id=0), SimNetworks)


def test_init_sample_info_valid():
    assert isinstance(SampleInfo(s_id="s1", value=100), SampleInfo)


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
            partner_id=2,
            partner_mz=123.4,
            partner_adduct="[M+H]+",
            diff_ppm=5.5,
            sample="sample1",
            sample_set={"sample1"},
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


def test_to_json_neural_loss_valid():
    feature = Feature()
    feature.Annotations = Annotations()
    feature.Annotations.losses = [
        NeutralLoss(
            id="alanine", loss_det=100.0, loss_ex=100.01, mz_frag=80.0, diff=12.0
        )
    ]
    f_dict = feature.to_json()
    assert f_dict["annotations"]["losses"][0]["id"] == "alanine"


def test_to_json_fragments_valid():
    feature = Feature()
    feature.Annotations = Annotations()
    feature.Annotations.fragments = [
        CharFrag(id="Ala-Ala", frag_det=100.0, frag_ex=100.01, diff=12.0)
    ]
    f_dict = feature.to_json()
    assert f_dict["annotations"]["fragments"][0]["id"] == "Ala-Ala"


def test_to_json_phenotype_valid():
    feature = Feature()
    feature.Annotations = Annotations()
    feature.Annotations.phenotypes = [
        Phenotype(score=0.1, format="qualitative", descr="asdf")
    ]
    f_dict = feature.to_json()
    assert f_dict["annotations"]["phenotypes"][0]["score"] == 0.1


def test_to_json_area_per_sample_valid():
    feature = Feature()
    feature.area_per_sample = [
        SampleInfo(s_id="s1", value=100),
        SampleInfo(s_id="s2", value=200),
    ]
    f_dict = feature.to_json()
    assert f_dict["area_per_sample"][0]["value"] == 100


def test_to_json_height_per_sample_valid():
    feature = Feature()
    feature.height_per_sample = [
        SampleInfo(s_id="s1", value=100),
        SampleInfo(s_id="s2", value=200),
    ]
    f_dict = feature.to_json()
    assert f_dict["height_per_sample"][0]["value"] == 100


def test_to_json_group_factor_valid():
    feature = Feature()
    feature.group_factors = {
        "cat1": [
            GroupFactor(group1="s1", group2="s2", factor=10),
            GroupFactor(group1="s2", group2="s1", factor=0.1),
        ]
    }
    f_dict = feature.to_json()
    assert f_dict["group_factors"] is not None


def test_to_json_groups_valid():
    feature = Feature()
    feature.groups = {"cat1": {"gr1", "gr2", "gr3"}, "cat2": {"m1", "m2"}}
    f_dict = feature.to_json()
    assert len(f_dict["groups"]["cat1"]) == 3


def test_to_json_scores_valid():
    feature = Feature()
    feature.Scores = Scores(novelty=1.0, phenotype=0.88)
    f_dict = feature.to_json()
    assert f_dict["scores"]["novelty"] == 1.0


def test_sort_entries_adducts_invalid():
    annotation = Annotations()
    annotation.sort_entries(attr="adducts", score="diff_ppm", direction=True)
    assert annotation.adducts is None


def test_sort_entries_adducts_valid():
    annotation = Annotations(
        adducts=[
            Adduct(
                partner_adduct="A",
                partner_mz=12,
                diff_ppm=11.0,
                partner_id=12,
                adduct_type="B",
            ),
            Adduct(
                partner_adduct="A",
                partner_mz=12,
                diff_ppm=1.0,
                partner_id=12,
                adduct_type="B",
            ),
        ]
    )
    annotation.sort_entries(attr="adducts", score="diff_ppm", direction=False)
    assert annotation.adducts[0].diff_ppm == 1.0


def test_sort_entries_matches_invalid():
    annotation = Annotations()
    annotation.sort_entries(attr="matches", score="score", direction=True)
    assert annotation.matches is None


def test_sort_entries_matches_valid():
    annotation = Annotations()
    annotation.matches = [
        Match(
            id="fakeomycin",
            library="default_library",
            algorithm="modified cosine",
            score=0.1,
            mz=1234.5,
            diff_mz=300.2,
            module="user-library-matching",
        ),
        Match(
            id="fakeomycin",
            library="default_library",
            algorithm="modified cosine",
            score=0.99,
            mz=1234.5,
            diff_mz=300.2,
            module="user-library-matching",
        ),
    ]
    annotation.sort_entries(attr="matches", score="score", direction=True)
    assert annotation.matches[0].score == 0.99


def test_sort_entries_losses_invalid():
    annotation = Annotations()
    annotation.sort_entries(attr="losses", score="diff", direction=False)
    assert annotation.losses is None


def test_sort_entries_losses_valid():
    annotation = Annotations(
        losses=[
            NeutralLoss(
                id="alanine", loss_det=100.0, loss_ex=100.01, mz_frag=80.0, diff=12.0
            ),
            NeutralLoss(
                id="non-ala", loss_det=100.0, loss_ex=100.01, mz_frag=80.0, diff=1.0
            ),
        ]
    )
    annotation.sort_entries(attr="losses", score="diff", direction=False)
    assert annotation.losses[0].diff == 1.0


def test_sort_entries_fragments_invalid():
    annotation = Annotations()
    annotation.sort_entries(attr="fragments", score="diff", direction=False)
    assert annotation.fragments is None


def test_sort_entries_fragments_valid():
    annotation = Annotations()
    annotation.fragments = [
        CharFrag(id="Ala-Ala", frag_det=100.0, frag_ex=100.01, diff=12.0),
        CharFrag(id="yalla-yalla", frag_det=100.0, frag_ex=100.01, diff=1.0),
    ]
    annotation.sort_entries(attr="fragments", score="diff", direction=False)
    assert annotation.fragments[0].diff == 1.0


def test_sort_entries_phenotypes_invalid():
    annotation = Annotations()
    annotation.sort_entries(attr="phenotypes", score="score", direction=True)
    assert annotation.phenotypes is None


def test_sort_entries_phenotypes_valid():
    annotation = Annotations()
    annotation.phenotypes = [
        Phenotype(score=0.1, format="qualitative", descr="asdf"),
        Phenotype(score=1.0, format="qualitative", descr="qwertz"),
    ]
    annotation.sort_entries(attr="phenotypes", score="score", direction=True)
    assert annotation.phenotypes[0].score == 1.0
