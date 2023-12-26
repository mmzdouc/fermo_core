from fermo_core.config.class_logger import LoggerSetup


def test_init_valid():
    assert isinstance(LoggerSetup(), LoggerSetup)
