import numpy as np
from pathlib import Path
import pytest

from fermo_core.data_analysis.annotation_manager.class_fragment_annotator import (
    FragmentAnnotator,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
)
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import MsmsParameters
from fermo_core.input_output.core_module_parameter_managers import FragmentAnnParameters
from fermo_core.input_output.input_file_parameter_managers import PeaktableParameters
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils


@pytest.fixture
def frag_annotator_pos():
    feature1 = Feature(
        f_id=1,
        mz=100.0,
        Spectrum=Utils.create_spectrum_object(
            {
                "mz": np.array([100, 229.16588, 247.176441], dtype=float),
                "intens": np.array([10, 20, 100], dtype=float),
                "f_id": 1,
                "precursor_mz": 300.0,
            },
            intensity_from=0.0,
        ),
    )
    features = Repository()
    features.add(1, feature1)
    stats = Stats(active_features={1})
    params = ParameterManager()
    params.MsmsParameters = MsmsParameters(
        filepath=Path("example_data/case_study_MSMS.mgf"),
        format="mgf",
        rel_int_from=0.0,
    )
    params.PeaktableParameters = PeaktableParameters(
        filepath=Path("example_data/case_study_peak_table_quant_full.csv"),
        format="mzmine3",
        polarity="positive",
    )
    params.FragmentAnnParameters = FragmentAnnParameters()
    return FragmentAnnotator(
        features=features, samples=Repository(), params=params, stats=stats
    )


def test_run_analysis_valid(frag_annotator_pos):
    frag_annotator_pos.run_analysis()
    assert len(frag_annotator_pos.features.entries[1].Annotations.fragments) == 2


def test_annotate_feature_pos_valid(frag_annotator_pos):
    frag_annotator_pos.annotate_feature_pos(1)
    assert len(frag_annotator_pos.features.entries[1].Annotations.fragments) == 2


def test_annotate_feature_pos_invalid(frag_annotator_pos):
    frag_annotator_pos.features.entries[1].Spectrum = None
    frag_annotator_pos.annotate_feature_pos(1)
    assert frag_annotator_pos.features.entries[1].Annotations is None


def test_validate_pos_aa_fragments_valid(frag_annotator_pos):
    feature = frag_annotator_pos.features.get(1)
    feature = frag_annotator_pos.validate_pos_aa_fragments(feature)
    assert len(feature.Annotations.fragments) == 2


def test_validate_pos_aa_fragments_invalid(frag_annotator_pos):
    frag_annotator_pos.features.entries[1].Spectrum = None
    feature = frag_annotator_pos.features.get(1)
    with pytest.raises(AttributeError):
        frag_annotator_pos.validate_pos_aa_fragments(feature)
