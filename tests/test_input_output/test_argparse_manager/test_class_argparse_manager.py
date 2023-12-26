import argparse
import pytest

from fermo_core.input_output.class_argparse_manager import ArgparseManager


def test_argparse_manager_instance():
    assert isinstance(ArgparseManager(), ArgparseManager)


def test_run_argparse_valid():
    assert isinstance(
        ArgparseManager().run_argparse("version", ["-p", "path/to/file"]),
        argparse.Namespace,
    )


def test_run_argparse_invalid():
    with pytest.raises(SystemExit) as e:
        ArgparseManager().run_argparse("version", [])
    assert e.type == SystemExit
    assert e.value.code == 2


def test_define_argparse_args_valid():
    assert isinstance(
        ArgparseManager().define_argparse_args("version"), argparse.ArgumentParser
    )


def test_define_argparse_args_invalid():
    with pytest.raises(TypeError):
        ArgparseManager().define_argparse_args()
