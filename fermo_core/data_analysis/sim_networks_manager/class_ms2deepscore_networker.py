"""Organize ms2deepscore spectral similarity networking methods.

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
import networkx
from pathlib import Path
import shutil
from typing import Dict, Self, Optional, Union
import urllib.request

import matchms
import func_timeout

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkDeepscoreParameters,
)

logger = logging.getLogger("fermo_core")


class Ms2deepscoreNetworker:
    """Class for calling and logging ms2deepscore spectral similarity networking"""

    # must have MS2
    # load in the data
    # what if data not available? Download at beginning

    @staticmethod
    def download_file(url: str, filename_path: Union[Path, str]):
        """Downloads the required file from the given URL."""
        with urllib.request.urlopen(url) as response, open(filename_path, "wb") as out:
            data = response.read()
            out.write(data)

    def verify_presence_ms2deepscore_file(
        self: Self, settings: SpecSimNetworkDeepscoreParameters
    ):
        """Verify existence of file and download if not present

        Arguments:
            settings: holds the directory path, filename, and url
        """
        filepath = settings.directory_path.joinpath(settings.filename)

        if not filepath.exists():
            self.download_file(settings.url, filepath)

        # TODO(MMZ 15.1.24): add a timeout for download, add logging that download
        #  needs to be performed, add logging that download was completed, add a try
        #  except to check if URL download fails (needs to befrom network manager class