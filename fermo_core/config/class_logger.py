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
import platform
import sys
from pathlib import Path

import coloredlogs


class LoggerSetup:
    """Organize settings for process logging"""

    @staticmethod
    def setup_custom_logger(name: str) -> logging.Logger:
        """Set logging parameters.

        Arguments:
            name: the logger name

        Returns:
            A Logger object
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        log_file_path = Path(__file__).parent.parent.joinpath("fermo_core.log")

        file_handler = logging.FileHandler(log_file_path, mode="w")
        file_handler.setLevel(logging.DEBUG)

        formatter = coloredlogs.ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def log_system_settings(logger: logging.Logger):
        """Log the system settings

        Attributes:
            logger: the previously initialized logger
        """
        logger.debug(
            f"Python version: {platform.python_version()}; "
            f"System: {platform.system()}; "
            f"System version: {platform.version()};"
            f"System architecture: {platform.python_version()}"
        )
