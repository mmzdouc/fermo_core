import pandas as pd
import pytest

from fermo_core.data_processing.parser.group_metadata_parser.class_fermo_metadata_parser import (
    MetadataFermoParser,
)
from fermo_core.data_processing.class_stats import Stats


@pytest.fixture
def fermo_meta_parser():
    parser = MetadataFermoParser(
        stats=Stats(),
        df=pd.DataFrame(
            {
                "sample_name": ["s1", "s2", "s3"],
                "phenotype": ["A", "B", "BLANK"],
                "medium": ["med1", "med2", "med3"],
            }
        ),
    )
    parser.stats.GroupMData.default_s_ids.update({"s1", "s2", "s3", "s4"})
    parser.stats.samples = ("s1", "s2", "s3", "s4")
    return parser


def test_validate_sample_names_valid(fermo_meta_parser):
    assert fermo_meta_parser.validate_sample_names() is None


def test_validate_sample_names_invalid(fermo_meta_parser):
    fermo_meta_parser.stats.samples = tuple("s5")
    with pytest.raises(RuntimeError):
        fermo_meta_parser.validate_sample_names()


def test_unassign_default_set_valid(fermo_meta_parser):
    fermo_meta_parser.unassign_default_set()
    assert fermo_meta_parser.stats.GroupMData.default_s_ids == {"s4"}


def test_extract_blanks_valid(fermo_meta_parser):
    fermo_meta_parser.extract_blanks()
    assert fermo_meta_parser.stats.GroupMData.blank_s_ids == {"s3"}
    assert len(fermo_meta_parser.stats.GroupMData.nonblank_s_ids) == 2


def test_extract_blanks_invalid(fermo_meta_parser):
    fermo_meta_parser.df.loc[2, "phenotype"] = "C"
    fermo_meta_parser.extract_blanks()
    assert fermo_meta_parser.stats.GroupMData.blank_s_ids == set()


def test_prepare_ctgrs_valid(fermo_meta_parser):
    fermo_meta_parser.prepare_ctgrs()
    assert len(fermo_meta_parser.stats.GroupMData.ctgrs) == 2


def test_run_parser_valid(fermo_meta_parser):
    fermo_meta_parser.run_parser()
    assert fermo_meta_parser.stats.GroupMData.default_s_ids == {"s4"}
    assert fermo_meta_parser.stats.GroupMData.blank_s_ids == {"s3"}
    assert len(fermo_meta_parser.stats.GroupMData.ctgrs) == 2
    assert len(fermo_meta_parser.stats.GroupMData.ctgrs["phenotype"]) == 2
    assert len(fermo_meta_parser.stats.GroupMData.ctgrs["medium"]) == 2
