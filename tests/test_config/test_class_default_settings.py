from fermo_core.config.class_default_settings import DefaultPaths


def test_init_class():
    assert isinstance(DefaultPaths(), DefaultPaths)


def test_dirpath_ms2deepscore():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2deepscore.exists()


def test_dirpath_ms2query():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2query.exists()
