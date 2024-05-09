from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


def test_init_sample_valid():
    assert isinstance(Sample(), Sample), (
        "Could not initialize instance of object " "Sample"
    )


def test_multiple_instances_valid():
    sample1 = Sample()
    sample2 = Sample()
    assert sample1 is not sample2


# TODO(MMZ 9.5.24): turn back on once scores are implemented
# def test_to_json_empty_valid():
#     sample = Sample()
#     json_dict = sample.to_json()
#     assert json_dict == {}


def test_to_json_s_id_valid():
    sample = Sample()
    sample.s_id = "sample1"
    json_dict = sample.to_json()
    assert json_dict.get("s_id") == "sample1"


def test_to_json_features_valid():
    sample = Sample()
    feature = Feature()
    feature.f_id = 1
    feature.mz = 101.1
    sample.features = {1: feature}
    sample.feature_ids = {1}
    json_dict = sample.to_json()
    assert json_dict["sample_spec_features"][1]["f_id"] == 1


def test_to_json_networks_valid():
    sample = Sample()
    sample.networks = {"mod_cos": {0, 1, 2}, "ms2deep": {0, 1}}
    json_dict = sample.to_json()
    assert isinstance(json_dict["networks"]["mod_cos"], list)
