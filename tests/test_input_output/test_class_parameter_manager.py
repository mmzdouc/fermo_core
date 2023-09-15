from pathlib import Path

from fermo_core.input_output.class_parameter_manager import ParameterManager


def test_instantiate_object():
    assert isinstance(
        ParameterManager("0.1.0", Path("my/path/here")), ParameterManager
    ), "Could not instantiate ParameterManager object"
