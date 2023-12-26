import json
import jsonschema
from pathlib import Path


def test_case_study_parameters_json_valid():
    with open(Path("example_data/case_study_parameters.json")) as infile:
        example_json = json.load(infile)
    with open(Path("fermo_core/config/schema.json")) as infile:
        schema = json.load(infile)
    assert jsonschema.validate(instance=example_json, schema=schema) is None
