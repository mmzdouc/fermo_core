import json
import pytest

from fermo_core.input_output.class_file_manager import FileManager


def test_file_manager_instance():
    assert isinstance(FileManager(), FileManager)


def test_load_json_file_valid():
    assert isinstance(
        FileManager.load_json_file("example_data/case_study_parameters.json"),
        dict,
    )


@pytest.mark.parametrize(
    "infile",
    [
        "",
        "tests/example_files/example_duplicate_entries.csv",
        "tests/example_files/invalid_json.json",
    ],
)
def test_load_json_file_invalid(infile):
    with pytest.raises((TypeError, FileNotFoundError, json.JSONDecodeError)):
        FileManager.load_json_file(infile)
