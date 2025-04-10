from fermo_core.data_processing.parser.msms_parser.class_mgf_parser import MgfParser


def test_parse_mgf_valid(parameter_instance, feature_instance):
    i = MgfParser(params=parameter_instance, features=feature_instance)
    assert isinstance(i, MgfParser)
    i.modify_features()
    feature_repo = i.return_features()
    assert feature_repo.entries.get(126).Spectrum is not None
