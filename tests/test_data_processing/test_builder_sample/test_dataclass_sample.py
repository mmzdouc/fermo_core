from pydantic import ValidationError
import pytest

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
