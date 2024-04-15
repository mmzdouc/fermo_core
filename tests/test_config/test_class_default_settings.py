from fermo_core.config.class_default_settings import DefaultPaths, NeutralMasses


def test_init_class():
    assert isinstance(DefaultPaths(), DefaultPaths)


def test_dirpath_ms2deepscore():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2deepscore.exists()


def test_dirpath_ms2query():
    default_settings = DefaultPaths()
    assert default_settings.dirpath_ms2query.exists()


def test_neutralmasses_valid():
    neutral_masses = NeutralMasses()
    assert len(neutral_masses.ribosomal) != 0
    assert len(neutral_masses.nonribo) != 0
    assert neutral_masses.nonribo[0].nribo_mon == "Eta"
    assert neutral_masses.ribosomal[0].id == "Glycine"
