import pytest

from fermo_core.data_processing.builder_sample.class_sample_builder import SampleBuilder
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


def test_success_init_sample_builder():
    assert isinstance(
        SampleBuilder().get_result(), Sample
    ), "Could not initialize the object Sample."


@pytest.mark.parametrize(
    "attr",
    (
        "s_id",
        "features",
        "groups",
        "cliques",
        "phenotypes",
        "max_intensity",
    ),
)
def test_success_sample_builder_default_values(attr):
    sample = SampleBuilder().get_result()
    match attr:
        case "groups":
            assert getattr(sample, attr) == {
                "DEFAULT"
            }, "Sample attribute 'groups' is not the expected 'DEFAULT'."
        case _:
            assert (
                getattr(sample, attr) is None
            ), f"Sample attribute '{attr}' is not the default 'None'."


def test_success_set_attributes_sample_builder():
    sample = SampleBuilder().set_s_id("sample1").get_result()
    assert sample.s_id == "sample1", "Builder could not set value when building object."


def test_success_assign_new_attributes_sample_builder():
    sample = SampleBuilder().set_s_id("sample1").get_result()
    sample.s_id = "sample2"
    assert sample.s_id == "sample2", "Could not assign new value to Sample."


def test_fail_init_with_invalid_values_sample_builder():
    with pytest.raises(ValueError):
        SampleBuilder().set_s_id(10)


def test_success_init_multiple_instances_sample_builder():
    sample1 = SampleBuilder().set_s_id("sample1").get_result()
    sample2 = SampleBuilder().set_s_id("sample2").get_result()
    assert sample1.s_id != sample2.s_id, (
        "Could not build multiple instances with different attributes using the same "
        "builder."
    )
