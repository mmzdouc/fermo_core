from fermo_core.data_processing.parser.peaktable_parser.class_mzmine3_parser import (
    PeakMzmine3Parser,
)


def test_parse_mgf_valid(parameter_instance):
    i = PeakMzmine3Parser()
    assert isinstance(i, PeakMzmine3Parser)
    stats, features, samples = i.parse(params=parameter_instance)
    assert stats.features == 143
    assert len(features.entries) == 143
    assert len(samples.entries) == 11
