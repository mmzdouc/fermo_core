"""Manages methods for reading and writing files.

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

import json
import logging
from pathlib import Path

from fermo_core.input_output.class_validation_manager import ValidationManager

logger = logging.getLogger("fermo_core")


class FileManager:
    """Manages exclusively static methods for reading and writing of files."""

    @staticmethod
    def load_json_file(json_file: str) -> dict:
        """Validates json file and attempts to load it.

        Parameters:
            json_file: a filepath to a json file

        Returns:
            The loaded file as a dict.
        """
        try:
            ValidationManager.validate_file_exists(json_file)
            ValidationManager.validate_file_extension(Path(json_file), ".json")

            with open(Path(json_file)) as infile:
                return json.load(infile)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON file '{json_file}': wrong format.")
            raise e
        except FileNotFoundError as e:
            logger.error(str(e))
            raise e
        except TypeError as e:
            logger.error(str(e))
            raise e
