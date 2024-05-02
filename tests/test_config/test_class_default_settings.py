from fermo_core.config.class_default_settings import (
    DefaultPaths,
    NeutralLosses,
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


def test_class_loss_valid():
    assert isinstance(Loss(descr="example", loss=123.456, abbr="ex"), Loss)


def test_neutralmasses_valid():
    neutral_masses = NeutralLosses()
    assert len(neutral_masses.ribosomal) != 0
    assert len(neutral_masses.nonribo) != 0
    assert len(neutral_masses.glycoside) != 0
    assert len(neutral_masses.gen_bio_pos) != 0
    assert len(neutral_masses.gen_other_pos) != 0
    assert len(neutral_masses.gen_other_neg) != 0
