import json

import jsonschema
import pytest


def test_schema_valid():
    with open("fermo_core/config/schema.json") as infile:
        schema = json.load(infile)
    with open("example_data/case_study_parameters.json") as infile:
        params = json.load(infile)
    assert jsonschema.validate(instance=params, schema=schema) is None


def test_schema_invalid():
    with open("fermo_core/config/schema.json") as infile:
        schema = json.load(infile)
    with open("example_data/fermo.session.json") as infile:
        params = json.load(infile)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=params, schema=schema)
