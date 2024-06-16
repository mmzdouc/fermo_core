from fermo_core.config.class_default_settings import (
    CharFragments,
    DefaultPaths,
    Fragment,
    Loss,
    NeutralLosses,
)


def test_init_class():
    assert isinstance(DefaultPaths(), DefaultPaths)


def test_dirpath_ms2deepscore():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2deepscore_pos.exists()


def test_class_loss_valid():
    assert isinstance(Loss(descr="example", loss=123.456, abbr="ex"), Loss)


def test_neutral_losses_valid():
    neutral_losses = NeutralLosses()
    assert len(neutral_losses.ribosomal) != 0
    assert len(neutral_losses.nonribo) != 0
    assert len(neutral_losses.glycoside) != 0
    assert len(neutral_losses.gen_bio_pos) != 0
    assert len(neutral_losses.gen_other_pos) != 0
    assert len(neutral_losses.gen_other_neg) != 0


def test_init_fragment():
    assert isinstance(Fragment(mass=123.456, descr="abcde"), Fragment)


def test_char_fragments_valid():
    char_frags = CharFragments()
    assert len(char_frags.aa_frags) != 0
