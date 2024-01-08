from fermo_core.data_processing.builder_sample.class_samples_director import (
    SamplesDirector,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


def test_construct_sample(df_mzmine3):
    assert isinstance(
        SamplesDirector.construct_mzmine3("5440_5439_mod.mzXML", df_mzmine3), Sample
    ), "Could not build an instance of object Sample using SamplesDirector."
