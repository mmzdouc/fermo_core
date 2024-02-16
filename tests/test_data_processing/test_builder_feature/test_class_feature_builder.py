import pandas as pd
import pytest

from fermo_core.data_processing.builder_feature.class_feature_builder import (
    FeatureBuilder,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


def test_set_attributes_valid():
    feature = FeatureBuilder().set_f_id(10).get_result()
    assert feature.f_id == 10, "Builder could not set value when building object."


def test_re_set_attributes_valid():
    feature = FeatureBuilder().set_f_id(10).get_result()
    feature.f_id = 5
    assert feature.f_id == 5, "Could not assign new value to Feature."


def test_multiple_init_valid():
    feature1 = FeatureBuilder().set_f_id(1).get_result()
    feature2 = FeatureBuilder().set_f_id(2).get_result()
    assert feature1.f_id is not feature2.f_id, (
        "Could not build multiple instances with different attributes using the same "
        "builder."
    )


def test_set_f_id_valid():
    feature1 = FeatureBuilder().set_f_id(1).get_result()
    assert feature1.f_id == 1


def test_set_mz_valid():
    feature1 = FeatureBuilder().set_mz(123.456).get_result()
    assert feature1.mz == 123.456


def test_set_rt_valid():
    feature1 = FeatureBuilder().set_rt(12.34).get_result()
    assert feature1.rt == 12.34


def test_set_rt_start_valid():
    feature1 = FeatureBuilder().set_rt_start(12.34).get_result()
    assert feature1.rt_start == 12.34


def test_set_rt_stop_valid():
    feature1 = FeatureBuilder().set_rt_stop(12.34).get_result()
    assert feature1.rt_stop == 12.34


def test_set_rt_range_valid():
    feature1 = (
        FeatureBuilder()
        .set_rt_stop(12.00)
        .set_rt_start(10.00)
        .set_rt_range()
        .get_result()
    )
    assert feature1.rt_range == 2.00


def test_set_rt_range_invalid():
    with pytest.raises(ValueError):
        FeatureBuilder().set_rt_range()


def test_set_fwhm_valid():
    feature1 = FeatureBuilder().set_fwhm(12.34).get_result()
    assert feature1.fwhm == 12.34


def test_set_intensity_valid():
    feature1 = FeatureBuilder().set_intensity(1234).get_result()
    assert feature1.intensity == 1234


def test_set_rel_intensity_valid():
    feature1 = FeatureBuilder().set_rel_intensity(1, 10).get_result()
    assert feature1.rel_intensity == 0.1


def test_set_area_valid():
    feature1 = FeatureBuilder().set_area(10).get_result()
    assert feature1.area == 10


def test_set_rel_area_valid():
    feature1 = FeatureBuilder().set_rel_area(1, 10).get_result()
    assert feature1.rel_area == 0.1


def test_set_samples_valid():
    series = pd.Series(
        {
            "datafile:5440_5439_mod.mzXML:feature_state": "DETECTED",
            "datafile:5432_5431_mod2.mzXML:feature_state": "DETECTED",
            "datafile:5434_5433_mod.mzXML:feature_state": "UNKNOWN",
        }
    )
    feature1 = FeatureBuilder().set_samples(series).get_result()
    assert feature1.samples == ("5440_5439_mod.mzXML", "5432_5431_mod2.mzXML")


def test_get_result_valid():
    feature1 = FeatureBuilder().get_result()
    assert isinstance(feature1, Feature)
