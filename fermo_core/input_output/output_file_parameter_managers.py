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
import logging
from pathlib import Path
from typing import Self

from pydantic import BaseModel, model_validator

from fermo_core.config.class_default_settings import DefaultPaths

logger = logging.getLogger("fermo_core")


class OutputParameters(BaseModel):
    """A Pydantic-based class for representing and validating output parameters.

    Attributes:
        dir_path: the output directory path

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    dir_path: Path = DefaultPaths().dirpath_output

    @model_validator(mode="after")
    def validate_output_dir(self):
        if not self.dir_path.exists():
            logger.warning(
                f"'ParameterManager/OutputParameters': specified output directory '"
                f"{self.dir_path}' cannot be found. Fall back to default output "
                f"directory '{DefaultPaths().dirpath_output}'."
            )
            self.dir_path = DefaultPaths().dirpath_output
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "dir_path": str(self.dir_path.resolve()),
        }
