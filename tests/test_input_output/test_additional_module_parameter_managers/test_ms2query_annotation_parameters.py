import pytest

from fermo_core.input_output.additional_module_parameter_managers import (
    Ms2QueryAnnotationParameters,
)


def test_init_ms2query_annotation_parameters_valid():
    json_dict = {
        "activate_module": True,
        "directory_path": "fermo_core/libraries",
        "consider_blank": True,
        "filter_rel_int_range": [0.0, 1.0],
    }
    assert isinstance(
        Ms2QueryAnnotationParameters(**json_dict),
        Ms2QueryAnnotationParameters,
    )


def test_init_ms2query_annotation_parameters_fail():
    with pytest.raises(TypeError):
        Ms2QueryAnnotationParameters(None)


def test_default_libraries_folder_valid():
    instance = Ms2QueryAnnotationParameters()
    default_path = instance.directory_path.name
    assert default_path == "libraries"
    assert instance.directory_path.exists()


def test_rel_int_range_scrambled_valid():
    json_dict = {
        "activate_module": True,
        "directory_path": "fermo_core/libraries",
        "consider_blank": True,
        "filter_rel_int_range": [1.0, 0.0],
    }
    assert isinstance(
        Ms2QueryAnnotationParameters(**json_dict), Ms2QueryAnnotationParameters
    )


def test_rel_int_range_invalid():
    with pytest.raises(ValueError):
        json_dict = {"filter_rel_int_range": [0.0]}
        Ms2QueryAnnotationParameters(**json_dict)
