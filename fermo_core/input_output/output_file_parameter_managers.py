"""Organizes classes to handle and validate output file parameters.

Copyright (c) 2022-2023 Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pathlib import Path
from typing import Self

from pydantic import BaseModel, model_validator


class OutputParameters(BaseModel):
    """A Pydantic-based class for representing and validating output parameters.

    Attributes:
        default_filepath: a pathlib Path reference in case filepath is corrupted
        filepath: a pathlib Path object pointing toward the output file
        format: the format of the output file

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    default_filepath: Path = Path(__file__).parent.parent.parent.joinpath(
        "example_data/fermo_session"
    )
    filepath: Path = Path(__file__).parent.parent.parent.joinpath(
        "example_data/fermo_session"
    )
    format: str = "all"

    @model_validator(mode="after")
    def validate_format(self):
        match self.format:
            case "json":
                pass
            case "csv":
                pass
            case "all":
                pass
            case _:
                raise ValueError(
                    f"Unsupported spectral library format: " f"'{self.format}'."
                )
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
        }
