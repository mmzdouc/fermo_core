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

from datetime import datetime
import json
import logging
import pandas as pd
from pathlib import Path
import platform
from typing import Self, Optional, Any

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
        df: a Pandas dataframe to dump modified peaktable as csv
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    json_dict: dict = dict()
    df: Optional[Any] = None

    def run(self: Self, version: str, starttime: datetime):
        """Call export methods based on user-input

        Arguments:
            version: a str indicating the currently running version of fermo_core
            starttime: the date and time at start of fermo_core processing
        """
        self.validate_output_filepath()

        match self.params.OutputParameters.format:
            case "json":
                self.build_json_dict(version, starttime)
                self.write_fermo_json()
            case "csv":
                self.build_csv_output()
                self.write_csv_output()
            case _:
                self.build_json_dict(version, starttime)
                self.write_fermo_json()
                self.build_csv_output()
                self.write_csv_output()

    def validate_output_filepath(self: Self):
        """Validate user input filepath and change to default if necessary"""

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

        if not self.params.OutputParameters.filepath.suffix == '':
            self.params.OutputParameters.filepath = (
                self.params.OutputParameters.filepath.with_suffix('')
            )

    @staticmethod
    def validate_output_created(filepath: Path):
        """Validate that output file was created and log if not

        Arguments:
            filepath: a Path object pointing to created output file

        Raises:
            FileNotFoundError: file should have been created but can't be found
        """
        if filepath.exists():
            logger.info(
                f"'ExportManager': Successfully wrote file "
                f"'{filepath.resolve()}'."
            )
        else:
            logger.fatal(
                f"'ExportManager': File '{filepath}' should have been written but "
                f"cannot be found - ABORT"
            )
            raise FileNotFoundError

    def write_fermo_json(self: Self):
        """Write collected data in json_dict into a json file on disk

        Raises:
            FileNotFoundError: Could not write or find written json file.
        """
        filepath = self.params.OutputParameters.filepath.with_suffix('.json')

        with open(filepath, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(self.json_dict, indent=4, ensure_ascii=False))

        self.validate_output_created(filepath)

    def build_json_dict(self: Self, version: str, starttime: datetime):
        """Driver method to assemble data for json dump

        Arguments:
            version: a str indicating the currently running version of fermo_core
            starttime: the date and time at start of fermo_core processing

        """
        self.export_metadata_json(version, starttime)
        self.export_stats_json()
        self.export_params_json()
        self.export_features_json()
        self.export_samples_json()

    def export_metadata_json(self: Self, version: str, starttime: datetime):
        """Export metadata on analysis run.

        Arguments:
            version: a str indicating the currently running version of fermo_core
            starttime: the date and time at start of fermo_core processing

        """
        self.json_dict["metadata"] = {
            "fermo_core_version": version,
            "file_created_isoformat": datetime.now().isoformat(),
            "runtime_seconds": (datetime.now() - starttime).total_seconds(),
            "system": platform.system(),
            "version": platform.version(),
            "architecture": platform.architecture(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }

    def export_params_json(self: Self):
        """Export data from params"""
        self.json_dict["parameters"] = self.params.to_json()

    def export_stats_json(self: Self):
        """Export data from stats"""
        self.json_dict["stats"] = self.stats.to_json()

    def export_features_json(self: Self):
        """Export data from features repository"""
        self.json_dict["general_features"] = dict()
        if self.stats.active_features is not None:
            for feature_id in self.stats.active_features:
                feature = self.features.get(feature_id)
                self.json_dict["general_features"][feature_id] = feature.to_json()

    def export_samples_json(self: Self):
        """Export data from samples repository"""
        self.json_dict["samples"] = dict()
        if self.stats.samples is not None:
            for sample_id in self.stats.samples:
                sample = self.samples.get(sample_id)
                self.json_dict["samples"][sample_id] = sample.to_json()

    def build_csv_output(self: Self):
        """Driver method to assemble data for csv output"""
        self.df = pd.read_csv(self.params.PeaktableParameters.filepath)

        attributes = []
        if self.stats.networks is not None:
            for network in self.stats.networks:
                attributes.append(f"fermo:networks:{network}:network_id")

        if len(attributes) == 0:
            return

        for attribute in attributes:
            self.df[attribute] = self.df["id"].map(
                lambda x: self.get_attribute_value(x, attribute)
            )

    def get_attribute_value(self: Self, feature_id: int, attribute: str):
        """Retrieve attribute of feature id

        Arguments:
            feature_id: an integer feature id
            attribute: a string allowing to retrieve the feature information
        """
        attrs = attribute.split(":")
        try:
            feature = self.features.get(feature_id)
            return getattr(getattr(feature, attrs[1])[attrs[2]], attrs[3])
        except (TypeError, AttributeError, KeyError):
            return None

    def write_csv_output(self: Self):
        """Write modified peaktable as csv on disk

        Raises:
            FileNotFoundError: Could not write or find written csv output file.
        """
        filepath = self.params.OutputParameters.filepath.with_suffix('.csv')

        self.df.to_csv(filepath, encoding='utf-8', index=False, sep=',')

        self.validate_output_created(filepath)
