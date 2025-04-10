from fermo_core.data_processing.parser.spec_library_parser.class_spec_lib_mgf_parser import (
    SpecLibMgfParser,
)


def test_instantiate_parser_valid(parameter_instance, stats_instance):
    i = SpecLibMgfParser(stats=stats_instance, params=parameter_instance)
    assert isinstance(i, SpecLibMgfParser)
    assert len(i.stats.spectral_library) == 17
