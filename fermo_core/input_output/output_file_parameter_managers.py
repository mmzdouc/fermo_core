"""Organizes classes to handle and validate output file parameters.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

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
from typing import Optional, Self

from pydantic import BaseModel

logger = logging.getLogger("fermo_core")


class OutputParameters(BaseModel):
    """A Pydantic-based class for representing and validating output parameters.

    Attributes:
        directory_path: the output directory path
    """

    directory_path: Optional[Path] = None

    def validate_output_dir(self: Self, peaktable_dir: Path):
        """Check output dir and set to default if None or non-existing

        Arguments:
            peaktable_dir: the path to the directory where the peaktable resides
        """

        def _create_output_dir():
            self.directory_path = peaktable_dir.joinpath("results")
            if not self.directory_path.exists():
                self.directory_path.mkdir(exist_ok=True)
                logger.warning(
                    f"'ParameterManager/OutputParameters': create the default output "
                    f"directory '{self.directory_path}'."
                )

        if self.directory_path is None:
            logger.info(
                f"'ParameterManager/OutputParameters': "
                f"all results will be written to "
                f"'{peaktable_dir.joinpath('results')}'."
            )
            _create_output_dir()
        elif not self.directory_path.exists():
            logger.warning(
                f"'ParameterManager/OutputParameters': output directory "
                f"'{self.directory_path}' "
                f"not found. Results will be written to fallback directory "
                f"'{peaktable_dir.joinpath('results')}'."
            )
            _create_output_dir()

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        try:
            return {"directory_path": str(self.directory_path.resolve())}
        except AttributeError:
            return {"directory_path": "not specified"}
