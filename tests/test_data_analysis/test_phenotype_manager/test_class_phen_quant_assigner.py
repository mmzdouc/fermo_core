import pytest

from fermo_core.data_analysis.phenotype_manager.class_phen_quant_assigner import (
    PhenQuantAssigner,
)
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    Phenotype,
    SampleInfo,
)
from fermo_core.input_output.class_parameter_manager import ParameterManager


@pytest.fixture
def phen_quant():
    phen_quant = PhenQuantAssigner(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )
    f1 = Feature(
        f_id=1,
        area_per_sample=[
            SampleInfo(s_id="s1", value=1),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=30),
        ],
        height_per_sample=[
            SampleInfo(s_id="s1", value=300),
            SampleInfo(s_id="s2", value=20),
            SampleInfo(s_id="s3", value=10),
        ],
    )
    phen_quant.features.add(1, f1)
    phen_quant.stats.active_features = {1}
    # phen_quant.stats.phenotypes TODO: continue here with testing
    return phen_quant
