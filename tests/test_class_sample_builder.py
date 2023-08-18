from fermo_core.data_processing.builder.class_sample_builder import SampleBuilder
from fermo_core.data_processing.builder.dataclass_sample import Sample


def test_success_sample_builder():
    assert isinstance(SampleBuilder().set_s_id("s").get_result(), Sample)
