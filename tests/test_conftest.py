import pytest


def test_no_marker():
    assert True


@pytest.mark.slow
def test_run_slow():
    assert True
