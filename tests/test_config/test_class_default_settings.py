from fermo_core.config.class_default_settings import DefaultSettings


def test_init_class():
    assert isinstance(DefaultSettings(), DefaultSettings)


def test_dirpath_ms2deepscore():
    default_settings = DefaultSettings()
    assert default_settings.dirpath_ms2deepscore.exists()


def test_dirpath_ms2query():
    default_settings = DefaultSettings()
    assert default_settings.dirpath_ms2query.exists()
