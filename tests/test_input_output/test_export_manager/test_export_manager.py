from pathlib import Path

import pytest

from fermo_core.input_output.class_export_manager import ExportManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_stats import Stats
from fermo_core.data_processing.class_repository import Repository


@pytest.fixture
def export_manager():
    return ExportManager(
        params=ParameterManager(),
        stats=Stats(),
        features=Repository(),
        samples=Repository(),
    )


def test_write_to_fermo_json_invalid(export_manager):
    export_manager.json_dict = {"asdfasdfa": "sdtaesrawe"}
    export_manager.params.OutputParameters.filepath = Path("dsa/asdas/sdasd")
    export_manager.params.OutputParameters.default_filepath = Path("dsa/asdas/sdasd")
    with pytest.raises(FileNotFoundError):
        export_manager.write_to_fermo_json()
