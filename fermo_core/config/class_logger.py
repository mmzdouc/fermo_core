"""Organize logging for fermo_core.

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

import coloredlogs


class LoggerSetup:
    """Organize settings for process logging"""

    @staticmethod
    def init_logger_cli(root: Path) -> logging.Logger:
        """Set logging parameters.

        Arguments:
            root: the root file directory

        Returns:
            A Logger object
        """
        logger = logging.getLogger()

        filehandle = logging.FileHandler(root.joinpath("fermo_core.log"), mode="w")
        filehandle.setLevel(logging.DEBUG)

        formatter = coloredlogs.ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        filehandle.setFormatter(formatter)
        logger.addHandler(filehandle)

        coloredlogs.install(level="DEBUG")

        return logger