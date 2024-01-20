from pydantic import ValidationError
import pytest

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample, Phenotype


def test_init_sample_valid():
    assert isinstance(Sample(), Sample), (
        "Could not initialize instance of object " "Sample"
    )


def test_multiple_instances_valid():
    sample1 = Sample()
    sample2 = Sample()
    assert sample1 is not sample2


def test_init_phenotype_valid():
    assert isinstance(
        Phenotype(**{"value": 10.0, "conc": 1}), Phenotype
    ), "Could not initialize instance of object Phenotype"


def test_init_phenotype_invalid():
    with pytest.raises(ValidationError):
        Phenotype(**{"value": "", "conc": 1})


def test_phenotype_values_valid():
    phenotype = Phenotype(**{"value": 10.0, "conc": 1})
    assert isinstance(phenotype.value, float)
    assert isinstance(phenotype.conc, int)


def test_phenotype_assignment_valid():
    assert Phenotype(value=10.0, conc=1) is not None


def test_to_json_empty_valid():
    sample = Sample()
    json_dict = sample.to_json()
    assert json_dict == {"groups": ["DEFAULT"]}


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


def test_to_json_phenotypes_valid():
    sample = Sample()
    sample.phenotypes = {"test1": Phenotype(value=10, conc=1)}
    json_dict = sample.to_json()
    assert json_dict["phenotypes"]["test1"]["value"] == 10.0
