import json
import pytest

from fermo_core.input_output.class_file_manager import FileManager


def test_file_manager_instance():
    assert isinstance(FileManager(), FileManager)


def test_load_json_file_valid():
    assert isinstance(
        FileManager.load_json_file(
            "tests/test_input_output/test_file_manager/file.json"
        ),
        dict,
    )


def test_load_json_file_filenotfound_invalid():
    with pytest.raises(FileNotFoundError):
        FileManager.load_json_file("file/does/not/exist")


def test_load_json_file_typeerror_invalid():
    with pytest.raises(TypeError):
        FileManager.load_json_file("tests/test_input_output/test_file_manager/file")


def test_load_json_file_wrong_json_invalid():
    with pytest.raises(json.JSONDecodeError):
        FileManager.load_json_file(
            "tests/test_input_output/test_file_manager/invalid_json.json"
        )
