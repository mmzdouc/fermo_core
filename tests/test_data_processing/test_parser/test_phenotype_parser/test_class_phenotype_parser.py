import pandas as pd
import pytest

from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.parser.phenotype_parser.class_phenotype_parser import (
    PhenotypeParser,
)


@pytest.fixture
def qualitative_p():
    stats = Stats(samples=("s1", "s2", "s3", "s4"))
    df = pd.DataFrame({"sample_name": ["s1", "s2", "s3"]})
    return PhenotypeParser(stats=stats, df=df)


@pytest.fixture
def quant_percent_p():
    stats = Stats(samples=("s1", "s2"))
    df = pd.DataFrame(
        {
            "sample_name": ["s1", "s1", "s2", "s2", "s2"],
            "well": [1, 2, 3, 4, 5],
            "assay:assay1": [6, -6, 80, 85, 88],
            "assay:assay2": [80, 70, -20, 5, 2],
        }
    )
    return PhenotypeParser(stats=stats, df=df)


def test_parse_quantitative_percentage_mean(quant_percent_p):
    quant_percent_p.parse_quantitative_percentage("mean")
    assert round(quant_percent_p.stats.phenotypes[0].s_phen_data[1].value, 0) == 84


def test_parse_quantitative_percentage_median(quant_percent_p):
    quant_percent_p.parse_quantitative_percentage("median")
    assert quant_percent_p.stats.phenotypes[0].s_phen_data[1].value == 85


def test_validate_sample_names_valid(qualitative_p):
    assert qualitative_p.validate_sample_names() is None


def test_validate_sample_names_invalid(qualitative_p):
    qualitative_p.df = pd.DataFrame({"sample_name": ["1", "2", "3"]})
    with pytest.raises(RuntimeError):
        qualitative_p.validate_sample_names()


def test_parse_qualitative_valid(qualitative_p):
    qualitative_p.parse_qualitative()
    assert qualitative_p.stats.phenotypes[0].s_negative == {
        "s4",
    }


def test_parse_qualitative_invalid(qualitative_p):
    qualitative_p.stats.samples = ("s1", "s2", "s3")
    with pytest.raises(RuntimeError):
        qualitative_p.parse_qualitative()
