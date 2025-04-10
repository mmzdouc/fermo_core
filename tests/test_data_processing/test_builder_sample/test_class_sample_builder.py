import pytest

from fermo_core.data_processing.builder_sample.class_sample_builder import SampleBuilder
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


def test_init_valid():
    assert isinstance(SampleBuilder().get_result(), Sample)


def test_set_attributes_valid():
    sample = SampleBuilder().set_s_id("sample1").get_result()
    assert sample.s_id == "sample1"


def test_re_set_attributes_valid():
    sample = SampleBuilder().set_s_id("sample1").get_result()
    sample.s_id = "sample2"
    assert sample.s_id == "sample2"


def test_multiple_inits_valid():
    sample1 = SampleBuilder().set_s_id("sample1").get_result()
    sample2 = SampleBuilder().set_s_id("sample2").get_result()
    assert sample1.s_id != sample2.s_id


def test_get_result_valid():
    sample1 = SampleBuilder().get_result()
    assert isinstance(sample1, Sample)


def test_set_s_id_valid():
    sample1 = SampleBuilder().set_s_id("sample1").get_result()
    assert sample1.s_id == "sample1"


def test_set_max_intensity_mzmine3_valid(df_mzmine3):
    sample1 = (
        SampleBuilder()
        .set_max_intensity_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .get_result()
    )
    assert sample1.max_intensity == 59000


def test_set_max_area_mzmine3_valid(df_mzmine3):
    sample1 = (
        SampleBuilder()
        .set_max_area_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .get_result()
    )
    assert sample1.max_area == 9600


def test_set_features_mzmine3_valid(df_mzmine3):
    sample1 = (
        SampleBuilder()
        .set_max_intensity_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .set_max_area_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .set_features_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .get_result()
    )
    assert len(sample1.features) == 23


def test_set_features_mzmine3_invalid(df_mzmine3):
    with pytest.raises(ValueError):
        SampleBuilder().set_features_mzmine3("5440_5439_mod.mzXML", df_mzmine3)


def test_set_feature_ids_valid(df_mzmine3):
    sample1 = (
        SampleBuilder()
        .set_max_intensity_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .set_max_area_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .set_features_mzmine3("5440_5439_mod.mzXML", df_mzmine3)
        .set_feature_ids()
        .get_result()
    )
    assert len(sample1.feature_ids) == 23


def test_set_feature_ids_invalid(df_mzmine3):
    with pytest.raises(ValueError):
        SampleBuilder().set_feature_ids()
