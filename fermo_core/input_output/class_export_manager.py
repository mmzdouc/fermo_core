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
import platform
import shutil
from typing import Self, Optional, Any

import networkx as nx
import pandas as pd
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_validation_manager import ValidationManager

logger = logging.getLogger("fermo_core")


class ExportManager(BaseModel):
    """A Pydantic-based class for methods on exporting data.

    Attributes:
        params: a Parameter object with specified user parameters
        stats: a Stats object containing general information
        features: a Repository object containing feature and general information
        samples: a Repository object containing sample information
        filename_base: the export filename derived from peaktable
        session: a dict for collecting data for json dump
        df: a Pandas dataframe acting as aggregator for data
        df_full: a Pandas dataframe to dump modified full peaktable as csv
        df_full: a Pandas dataframe to dump modified abbreviated peaktable as csv
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    filename_base: Optional[str] = None
    session: dict = dict()
    df: Optional[Any] = None
    df_full: Optional[Any] = None
    df_abbrev: Optional[Any] = None

    @staticmethod
    def log_start_module(file: str):
        """Log the start of the export of the corresponding file"""
        logger.debug(f"'ExportManager': started export of '{file}'.")

    @staticmethod
    def log_complete_module(file: str):
        """Log the completion of the export of the corresponding file"""
        logger.debug(f"'ExportManager': completed export of '{file}'.")

    def run(self: Self, version: str, starttime: datetime):
        """Call export methods based on user-input

        Arguments:
            version: a str indicating the currently running version of fermo_core
            starttime: the date and time at start of fermo_core processing
        """
        self.define_filename()
        self.write_fermo_json(version, starttime)
        self.write_csv_output()
        self.write_cytoscape_output()
        self.write_raw_ms2query_results()

    def define_filename(self: Self):
        """Derive output filename base from peaktable"""
        self.filename_base = self.params.PeaktableParameters.filepath.stem

    def write_cytoscape_output(self: Self):
        """Write cytoscape output if networking was performed"""

        # check the network files and log it
        self.log_start_module(".cytoscape.json")

        if self.stats.networks is None:
            logger.warning(
                "'ExportManager': no spectral similarity networks generated - SKIP"
            )
            return

        for network in self.stats.networks:
            path_graphml = self.params.OutputParameters.dir_path.joinpath(
                self.filename_base
            ).with_suffix(f".fermo.{network}.graphml")
            nx.write_graphml(self.stats.networks[network].network, path_graphml)
            ValidationManager().validate_output_created(path_graphml)

        self.log_complete_module(".cytoscape.json")

    def write_fermo_json(self: Self, version: str, starttime: datetime):
        """Write collected data in session dict into a json file on disk

        Arguments:
            version: a str indicating the currently running version of fermo_core
            starttime: the date and time at start of fermo_core processing

        Raises:
            FileNotFoundError: Could not write or find written json file.
        """
        self.log_start_module("fermo.session.json")

        self.build_json_dict(version, starttime)

        filepath = self.params.OutputParameters.dir_path.joinpath(
            self.filename_base
        ).with_suffix(".fermo.session.json")
        with open(filepath, "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(self.session, indent=2, ensure_ascii=False))

        ValidationManager().validate_output_created(filepath)

        self.log_complete_module("fermo.session.json")

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
        self.session["metadata"] = {
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
        self.session["parameters"] = self.params.to_json()

    def export_stats_json(self: Self):
        """Export data from stats"""
        self.session["stats"] = self.stats.to_json()

    def export_features_json(self: Self):
        """Export data from features repository"""
        if self.stats.active_features is not None:
            self.session["general_features"] = dict()
            for feature_id in self.stats.active_features:
                feature = self.features.get(feature_id)
                self.session["general_features"][feature_id] = feature.to_json()

    def export_samples_json(self: Self):
        """Export data from samples repository"""
        if self.stats.samples is not None:
            self.session["samples"] = dict()
            for sample_id in self.stats.samples:
                sample = self.samples.get(sample_id)
                self.session["samples"][sample_id] = sample.to_json()

    def write_csv_output(self: Self):
        """Write modified peaktable as csv on disk

        Raises:
            FileNotFoundError: Could not write or find written csv output file.
        """
        self.log_start_module("fermo.full.csv/fermo.abbrev.csv")

        self.build_csv_output()

        filepath_df_full = self.params.OutputParameters.dir_path.joinpath(
            self.filename_base
        ).with_suffix(".fermo.full.csv")
        self.df_full.to_csv(filepath_df_full, encoding="utf-8", index=False, sep=",")
        ValidationManager().validate_output_created(filepath_df_full)

        filepath_df_abbrev = self.params.OutputParameters.dir_path.joinpath(
            self.filename_base
        ).with_suffix(".fermo.abbrev.csv")
        self.df_abbrev.to_csv(
            filepath_df_abbrev, encoding="utf-8", index=False, sep=","
        )
        ValidationManager().validate_output_created(filepath_df_abbrev)

        self.log_complete_module("fermo.full.csv/fermo.abbrev.csv")

    def build_csv_output(self: Self):
        """Driver method to assemble data for csv output"""
        self.df = pd.read_csv(self.params.PeaktableParameters.filepath)

        self.add_sample_info_csv()

        if self.stats.networks is not None:
            self.add_networks_info_csv()

        if self.params.NeutralLossParameters.activate_module:
            self.add_class_evidence_csv()

        self.df_full = self.df.copy(deep=True)

        abbr_cols = ["id", "height", "area", "mz", "rt"]
        abbr_cols.extend([col for col in self.df if col.startswith("fermo")])
        self.df_abbrev = self.df[abbr_cols].copy(deep=True)

    def add_sample_info_csv(self: Self):
        """Iterate through feature sample information and prepare for export"""

        def _add_sample_info(f_id: int) -> str | None:
            try:
                feature = self.features.get(f_id)
                return "|".join([s for s in feature.samples])
            except KeyError:
                return None

        self.df["fermo:samples"] = self.df["id"].map(lambda x: _add_sample_info(f_id=x))

    def add_networks_info_csv(self: Self):
        """Iterate through network information and prepare for export"""
        networks = []
        for network in self.stats.networks:
            networks.append(f"fermo:networks:{network}:network_id")

        if len(networks) == 0:
            return

        for network in networks:
            self.df[network] = self.df["id"].map(
                lambda x: self.get_network_value(x, network)
            )

    def get_network_value(self: Self, feature_id: int, attribute: str):
        """Retrieve network value attribute of feature id

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

    def add_class_evidence_csv(self: Self):
        """Iterate through evidence information and prepare for export"""
        tags = {"ribosomal": {}, "nonribosomal": {}, "glycoside": {}}
        for f_id in self.stats.active_features:
            try:
                feature = self.features.get(f_id)
            except KeyError:
                continue

            try:
                tags["ribosomal"][f_id] = "|".join(
                    feature.Annotations.classes["ribosomal"].evidence
                )
            except (TypeError, AttributeError, KeyError):
                pass
            try:
                tags["nonribosomal"][f_id] = "|".join(
                    feature.Annotations.classes["nonribosomal"].evidence
                )
            except (TypeError, AttributeError, KeyError):
                pass
            try:
                tags["glycoside"][f_id] = "|".join(
                    feature.Annotations.classes["glycoside"].evidence
                )
            except (TypeError, AttributeError, KeyError):
                pass

        for key, val in tags.items():
            self.df[f"fermo:annotation:{key}:monomers"] = self.df["id"].map(
                lambda x: val.get(x)
            )

    def write_raw_ms2query_results(self: Self) -> bool:
        """If raw MS2Query results exist, write to output directory

        Returns:
            A bool indicating the outcome of the operation
        """
        if (
            DefaultPaths().dirpath_ms2query_base.joinpath("results").exists()
            and DefaultPaths()
            .dirpath_ms2query_base.joinpath("results/f_queries.csv")
            .exists()
        ):
            shutil.move(
                src=DefaultPaths().dirpath_ms2query_base.joinpath(
                    "results/f_queries.csv"
                ),
                dst=self.params.OutputParameters.dir_path.joinpath(
                    self.filename_base
                ).with_suffix(".ms2query_results.csv"),
            )
            return True
        else:
            return False
