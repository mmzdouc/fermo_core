import pytest

from fermo_core.data_analysis.annotation_manager.class_adduct_annotator import (
    AdductAnnotator,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.core_module_parameter_managers import (
    AdductAnnotationParameters,
)


@pytest.fixture
def adduct_annotator(
    parameter_instance, stats_instance, feature_instance, sample_instance
):
    return AdductAnnotator(
        params=parameter_instance,
        stats=stats_instance,
        features=feature_instance,
        samples=sample_instance,
    )


@pytest.fixture
def adduct_annotator_min():
    params = ParameterManager(AdductAnnotationParameters=AdductAnnotationParameters())
    features = Repository()
    feature1 = Feature(f_id=1, mz=100.0)
    features.add(1, feature1)
    feature2 = Feature(f_id=1, mz=100.0)
    features.add(2, feature2)
    return AdductAnnotator(
        params=params, stats=Stats(), features=features, samples=Repository()
    )


def test_return_features_valid(adduct_annotator_min):
    assert adduct_annotator_min.return_features() is not None


def test_run_analysis_valid(adduct_annotator):
    adduct_annotator.run_analysis()
    features = adduct_annotator.return_features()
    assert features.entries[131].Annotations.adducts[0] is not None


def test_mass_deviation_valid(adduct_annotator_min):
    assert adduct_annotator_min.mass_deviation(100.0, 100.001, 1) == 10.0


def test_mass_deviation_invalid(adduct_annotator_min):
    with pytest.raises(ZeroDivisionError):
        adduct_annotator_min.mass_deviation(100.0, 0, 1)


def test_add_adduct_info_valid(adduct_annotator_min):
    feature = adduct_annotator_min.add_adduct_info(Feature())
    assert feature.Annotations is not None


def test_annotate_spec_features_valid(adduct_annotator):
    adduct_annotator.annotate_spec_features("5458_5457_mod.mzXML")
    features = adduct_annotator.return_features()
    assert features.entries[131].Annotations.adducts[0] is not None


def test_sodium_adduct_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 415.2098
    adduct_annotator_min.features.entries[2].mz = 437.1912
    assert adduct_annotator_min.sodium_adduct(1, 2, "sample1")


def test_dimer_sodium_adduct_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 415.2098
    adduct_annotator_min.features.entries[2].mz = 851.39487
    assert adduct_annotator_min.dimer_sodium_adduct(1, 2, "sample1")


def test_triple_h_adduct_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1510.4198
    adduct_annotator_min.features.entries[2].mz = 504.1447
    assert adduct_annotator_min.triple_h_adduct(1, 2, "sample1")


def test_plus1_isotope_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 1649.4578
    assert adduct_annotator_min.plus1_isotope(1, 2, "sample1")


def test_plus2_isotope_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 1650.4653
    assert adduct_annotator_min.plus2_isotope(1, 2, "sample1")


def test_plus3_isotope_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 1651.4547
    assert adduct_annotator_min.plus3_isotope(1, 2, "sample1")


def test_plus4_isotope_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 1652.4539
    assert adduct_annotator_min.plus4_isotope(1, 2, "sample1")


def test_plus5_isotope_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 1653.4754
    assert adduct_annotator_min.plus5_isotope(1, 2, "sample1")


def test_double_plus1_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 825.2326
    assert adduct_annotator_min.double_plus1(1, 2, "sample1")


def test_double_plus2_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 825.7343
    assert adduct_annotator_min.double_plus2(1, 2, "sample1")


def test_double_plus3_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 826.2360
    assert adduct_annotator_min.double_plus3(1, 2, "sample1")


def test_double_plus4_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 826.7377
    assert adduct_annotator_min.double_plus4(1, 2, "sample1")


def test_double_plus5_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1648.4547
    adduct_annotator_min.features.entries[2].mz = 827.2393
    assert adduct_annotator_min.double_plus5(1, 2, "sample1")


def test_iron56_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 843.4772
    adduct_annotator_min.features.entries[2].mz = 896.3883
    assert adduct_annotator_min.iron56(1, 2, "sample1")


def test_dimer_double_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 1510.4198
    adduct_annotator_min.features.entries[2].mz = 755.7153
    assert adduct_annotator_min.dimer_double(1, 2, "sample1")


def test_ammonium_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 409.29477
    adduct_annotator_min.features.entries[2].mz = 426.321
    assert adduct_annotator_min.ammonium(1, 2, "sample1")


def test_potassium_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 409.29477
    adduct_annotator_min.features.entries[2].mz = 447.251
    assert adduct_annotator_min.potassium(1, 2, "sample1")


def test_water_add_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 409.29477
    adduct_annotator_min.features.entries[2].mz = 427.30588
    assert adduct_annotator_min.water_add(1, 2, "sample1")


def test_water_loss_valid(adduct_annotator_min):
    adduct_annotator_min.features.entries[1].mz = 409.29477
    adduct_annotator_min.features.entries[2].mz = 391.284
    assert adduct_annotator_min.water_loss(1, 2, "sample1")
