from pydantic import ValidationError
import pytest

from fermo_core.config.class_default_settings import (
    DefaultPaths,
    NeutralMasses,
    PeptideHintAdducts,
    Loss,
)


def test_init_class():
    assert isinstance(DefaultPaths(), DefaultPaths)


def test_dirpath_ms2deepscore():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2deepscore_pos.exists()


def test_dirpath_ms2query():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2query_base.exists()
    assert default_settings.dirpath_ms2query_pos.exists()
    assert default_settings.dirpath_ms2query_neg.exists()


def test_peptidehint_adducts_valid():
    default_settings = PeptideHintAdducts()
    assert default_settings.adducts is not None


def test_peptidehint_adducts_invalid():
    with pytest.raises(ValidationError):
        PeptideHintAdducts(adducts=None)


def test_class_loss_valid():
    assert isinstance(Loss(id="example", mass=123.456), Loss)


def test_neutralmasses_valid():
    neutral_masses = NeutralMasses()
    assert len(neutral_masses.ribosomal) != 0
    assert len(neutral_masses.nonribo) != 0
    assert len(neutral_masses.glycoside) != 0
    assert len(neutral_masses.gen_bio_pos) != 0
    assert len(neutral_masses.gen_other_pos) != 0
    assert len(neutral_masses.gen_other_neg) != 0
