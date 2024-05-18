import pytest

from fermo_core.data_analysis.phenotype_manager.class_phenotype_manager import (
    PhenotypeManager,
)
from fermo_core.data_processing.class_stats import Stats, PhenoData, SamplePhenotype
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.input_file_parameter_managers import PhenotypeParameters
from fermo_core.input_output.additional_module_parameter_managers import (
    PhenoQualAssgnParams,
)


@pytest.fixture
def phen_manag_qual():
    phen_manag_qual = PhenotypeManager(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )
    phen_manag_qual.params.PhenotypeParameters = PhenotypeParameters(
        filepath="tests/test_data_analysis/test_phenotype_manager/qualitative.csv",
        format="qualitative",
    )
    phen_manag_qual.params.PhenoQualAssgnParams = PhenoQualAssgnParams(
        activate_module=True
    )
    f1 = Feature(
        f_id=1,
        samples={
            "s1",
        },
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=100),
        ],
    )
    f2 = Feature(
        f_id=2,
        samples={"s1", "s2"},
        area_per_sample=[
            SampleInfo(s_id="s1", value=10),
            SampleInfo(s_id="s2", value=1),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=100),
            SampleInfo(s_id="s2", value=10),
        ],
    )
    f3 = Feature(
        f_id=3,
        samples={
            "s2",
        },
        area_per_sample=[
            SampleInfo(s_id="s2", value=10),
        ],
        height_per_sample=[
            SampleInfo(s_id="s2", value=100),
        ],
    )
    phen_manag_qual.features.add(1, f1)
    phen_manag_qual.features.add(2, f2)
    phen_manag_qual.features.add(3, f3)
    s1 = Sample(s_id="s1", feature_ids={1, 2})
    s2 = Sample(s_id="s2", feature_ids={2, 3})
    phen_manag_qual.samples.add("s1", s1)
    phen_manag_qual.samples.add("s2", s2)
    phen_manag_qual.stats.active_features = {1, 2, 3}
    phen_manag_qual.stats.samples = ("s1", "s2")
    phen_manag_qual.stats.phenotypes = [
        PhenoData(
            datatype="qualitative",
            category="qualitative",
            s_negative={
                "s2",
            },
            s_phen_data=[SamplePhenotype(s_id="s1")],
        )
    ]
    return phen_manag_qual


def test_run_assigner_qualitative(phen_manag_qual):
    phen_manag_qual.run_assigner_qualitative()
    assert len(phen_manag_qual.stats.phenotypes[0].f_ids_positive) == 2
