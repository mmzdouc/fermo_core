"""Organizes data export methods for dumping on disk.

Copyright (c) 2022-2024 Mitja Maximilian Zdouc, PhD

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
from typing import Self

from pydantic import BaseModel

from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class ExportManager(BaseModel):
    """A Pydantic-based class for methods on exporting data.

    Attributes:
        params: a Parameter object with specified user parameters
        stats: a Stats object containing general information
        features: a Repository object containing feature and general information
        samples: a Repository object containing sample information
        json_dict: a dict for collecting data for json dump

    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    json_dict: dict = dict()

    def write_to_fermo_json(self: Self):
        """Write collected data in json_dict into a json file on disk

        Raises:
            FileNotFoundError: Could not write or find written json file.
        """
        if not self.params.OutputParameters.filepath.parent.exists():
            logger.warning(
                f"'ExportManager': Could not find the output directory "
                f"'{self.params.OutputParameters.filepath.parent.resolve()}'. "
                f"Fallback to default directory "
                f"'{self.params.OutputParameters.default_filepath.parent.resolve()}' "
                f"and default filename "
                f"'{self.params.OutputParameters.default_filepath.name}'."
            )
            self.params.OutputParameters.filepath = (
                self.params.OutputParameters.default_filepath
            )

        with open(self.params.OutputParameters.filepath, "w", encoding="utf-8") as outf:
            outf.write(json.dumps(self.json_dict, indent=4, ensure_ascii=False))

        if self.params.OutputParameters.filepath.exists():
            logger.info(
                f"'ExportManager': Successfully wrote file "
                f"'{self.params.OutputParameters.filepath}'."
            )
        else:
            logger.fatal(
                f"'ExportManager': Could not write file "
                f"'{self.params.OutputParameters.filepath}' - ABORT"
            )
            raise FileNotFoundError

    def build_json_dict(self: Self):
        """Driver method to assemble data for json dump"""
        self.export_stats()
        self.export_params()
        self.export_features_repo()
        self.export_samples_repo()

    def export_params(self: Self):
        """Export data from params"""
        self.json_dict["parameters"] = self.params.to_json()

    def export_stats(self: Self):
        """Export data from stats"""
        self.json_dict["stats"] = self.stats.to_json()

    def export_features_repo(self: Self):
        """Export data from features repository"""
        self.json_dict["general_features"] = dict()
        for feature_id in self.stats.active_features:
            feature = self.features.get(feature_id)
            self.json_dict["general_features"][feature_id] = feature.to_json()

    def export_samples_repo(self: Self):
        """Export data from samples repository"""
        self.json_dict["samples"] = dict()
        for sample_id in self.stats.samples:
            sample = self.samples.get(sample_id)
            self.json_dict["samples"][sample_id] = sample.to_json()
