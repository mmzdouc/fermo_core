from pathlib import Path

import numpy as np
import pytest

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.data_analysis.annotation_manager.class_ms2query_annotator import (
    MS2QueryAnnotator,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import (
    Ms2QueryAnnotationParameters,
    ParameterManager,
    PeaktableParameters,
)
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
        filepath="tests/test_data/test.peak_table_quant_full.csv",
    )
    ms2query_p = Ms2QueryAnnotationParameters(activate_module=True, maximum_runtime=200)
    params = ParameterManager()
    params.PeaktableParameters = peaktable_p
    params.OutputParameters.validate_output_dir(peaktable_dir=Path("tests/test_data/"))
    params.Ms2QueryAnnotationParameters = ms2query_p
    return MS2QueryAnnotator(
        features=features, params=params, active_features={20}, cutoff=0.7
    )


def test_prepare_queries_valid(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    assert ms2query_annotator.queries is not None


def test_estimate_calc_time_valid(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    assert ms2query_annotator.estimate_calc_time() is None


def test_estimate_calc_time_skip(ms2query_annotator):
    ms2query_annotator.params.Ms2QueryAnnotationParameters.maximum_runtime = 0
    ms2query_annotator.prepare_queries()
    assert ms2query_annotator.estimate_calc_time() is None


def test_estimate_calc_time_no_queries(ms2query_annotator):
    with pytest.raises(RuntimeError):
        ms2query_annotator.estimate_calc_time()


def test_estimate_calc_time_timeout(ms2query_annotator):
    ms2query_annotator.params.Ms2QueryAnnotationParameters.maximum_runtime = 1
    ms2query_annotator.prepare_queries()
    with pytest.raises(RuntimeError):
        ms2query_annotator.estimate_calc_time()


def test_create_ms2query_dirs(ms2query_annotator):
    ms2query_annotator.create_ms2query_dirs()
    assert Path("tests/test_data/results/temp_ms2query_queries").exists()
    ms2query_annotator.remove_temp_ms2query_dirs()


def test_remove_ms2query_temp_files(ms2query_annotator):
    ms2query_annotator.create_ms2query_dirs()
    ms2query_annotator.params.OutputParameters.directory_path.joinpath(
        "temp_ms2query_queries/f_queries.mgf"
    ).touch(exist_ok=True)
    ms2query_annotator.params.OutputParameters.directory_path.joinpath(
        "temp_ms2query_queries/f_queries.csv"
    ).touch(exist_ok=True)
    ms2query_annotator.remove_ms2query_temp_files()
    assert not ms2query_annotator.params.OutputParameters.directory_path.joinpath(
        "temp_ms2query_queries/f_queries.mgf"
    ).exists()
    assert not ms2query_annotator.params.OutputParameters.directory_path.joinpath(
        "temp_ms2query_queries/f_queries.csv"
    ).exists()
    ms2query_annotator.remove_temp_ms2query_dirs()


def test_assign_feature_info_results_invalid(ms2query_annotator):
    ms2query_annotator.cutoff = 0.4
    ms2query_annotator.active_features = {99}
    ms2query_annotator.assign_feature_info(
        "tests/test_data_analysis/test_annotation_manager/dummy_results_ms2query.csv"
    )
    assert ms2query_annotator.features.entries[20].Annotations is None


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


def test_run_ms2query_over_timeout(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    ms2query_annotator.params.Ms2QueryAnnotationParameters.maximum_runtime = 0.01
    with pytest.raises(RuntimeError):
        ms2query_annotator.run_ms2query()
    ms2query_annotator.remove_temp_ms2query_dirs()


@pytest.mark.high_cpu
def test_run_ms2query_valid(ms2query_annotator):
    ms2query_annotator.prepare_queries()
    ms2query_annotator.cutoff = 0.4
    ms2query_annotator.run_ms2query()
    assert (
        ms2query_annotator.features.entries[20].Annotations.matches[0].id
        == "Cer(d18:0/16:0)"
    )
