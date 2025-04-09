import json

import jsonschema
import pytest


def test_schema_valid():
    with open("fermo_core/config/schema.json") as infile:
        schema = json.load(infile)
    with open("tests/test_data/test.parameters.json") as infile:
        params = json.load(infile)
    assert jsonschema.validate(instance=params, schema=schema) is None

