import numpy as np
import pytest

from fermo_core.data_analysis.annotation_manager.class_ms2query_annotator import (
    MS2QueryAnnotator,
)
from fermo_core.input_output.class_parameter_manager import (
    ParameterManager,
    PeaktableParameters,
    Ms2QueryAnnotationParameters,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def ms2query_annotator():
    feature1 = Feature(
        f_id=20,
        mz=610.3346,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array(
                    [127.0951, 153.0754, 169.0942, 240.1807, 427.2433, 610.3336],
                    dtype=float,
                ),
                "intens": np.array([49, 190, 62, 3200, 2300, 5300], dtype=float),
                "f_id": 20,
                "precursor_mz": 610.3346,
            },
            intensity_from=0.0,
        ),
    )
    features = Repository()
    features.add(20, feature1)
    peaktable_p = PeaktableParameters(
        polarity="positive",
        format="mzmine3",
        filepath="example_data/case_study_peak_table_quant_full.csv",
    )
    ms2query_p = Ms2QueryAnnotationParameters(
        activate_module=True, exclude_blank=False, maximum_runtime=200
    )
    params = ParameterManager()
    params.PeaktableParameters = peaktable_p
    params.Ms2QueryAnnotationParameters = ms2query_p
    return MS2QueryAnnotator(
        features=features, params=params, active_features={20}, cutoff=0.7
    )


def test_prepare_queries_valid(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    assert ms2query_annotator.queries is not None


def test_prepare_queries_invalid(ms2query_annotator):
    ms2query_annotator.params.Ms2QueryAnnotationParameters.exclude_blank = True
    ms2query_annotator.features.entries.get(20).blank = True
    with pytest.raises(RuntimeError):
        ms2query_annotator.prepare_queries()


def test_assign_feature_info_valid(ms2query_annotator):
    ms2query_annotator.cutoff = 0.4
    ms2query_annotator.assign_feature_info(
        "tests/test_data_analysis/test_annotation_manager/dummy_results_ms2query.csv"
    )
    assert (
        ms2query_annotator.features.entries[20].Annotations.matches[0].npc_class
        == "unknown"
    )


def test_assign_feature_info_invalid(ms2query_annotator):
    ms2query_annotator.assign_feature_info(
        "tests/test_data_analysis/test_annotation_manager/dummy_results_ms2query.csv"
    )
    assert ms2query_annotator.features.entries[20].Annotations is None


@pytest.mark.high_cpu
def test_run_ms2query_over_timeout(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    ms2query_annotator.params.Ms2QueryAnnotationParameters.maximum_runtime = 0.01
    with pytest.raises(RuntimeError):
        ms2query_annotator.run_ms2query()
    ms2query_annotator.remove_ms2query_temp_files()


@pytest.mark.high_cpu
def test_run_ms2query_valid(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    ms2query_annotator.cutoff = 0.4
    ms2query_annotator.run_ms2query()
    assert (
        ms2query_annotator.features.entries[20].Annotations.matches[0].id
        == "Cer(d18:0/16:0)"
    )
    ms2query_annotator.remove_ms2query_temp_files()
