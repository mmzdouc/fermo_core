"""Storage and handling of general stats of analysis run.

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

from typing import Any, Optional, Self

import networkx as nx
import pandas as pd
from pydantic import BaseModel

from fermo_core.input_output.class_parameter_manager import ParameterManager


class Group(BaseModel):
    """Pydantic-based class to organize group info belonging to a metadata category

    Attributes:
        name: group identifier
        s_ids: a set of sample ids belonging to group
        f_ids: a set of feature ids detected in samples of group
    """

    s_ids: set = set()
    f_ids: set = set()

    def to_json(self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {"s_ids": list(self.s_ids), "f_ids": list(self.f_ids)}


class GroupMData(BaseModel):
    """Pydantic-based class to organize group metadata information

    Attributes:
        default_s_ids: containing ungrouped samples ("DEFAULT")
        nonblank_s_ids: containing nonblank sample ids
        nonblank_f_ids:containing ids of nonblank sample-associated features
        blank_s_ids: containing sample blank ids
        blank_f_ids: containing ids of sample blank-associated features
        ctgrs: dict containing category:{group-id: Group}, key-value pairs
    """

    default_s_ids: set = set()
    nonblank_s_ids: set = set()
    nonblank_f_ids: set = set()
    blank_s_ids: set = set()
    blank_f_ids: set = set()
    ctgrs: dict = {}

    def to_json(self) -> dict:
        """Convert attributes to json-compatible ones."""
        json_dict = {
            "default_s_ids": list(self.default_s_ids),
            "nonblank_s_ids": list(self.nonblank_s_ids),
            "nonblank_f_ids": list(self.nonblank_f_ids),
            "blank_s_ids": list(self.blank_s_ids),
            "blank_f_ids": list(self.blank_f_ids),
            "categories": {},
        }

        if len(self.ctgrs) != 0:
            for key, val in self.ctgrs.items():
                json_dict["categories"][key] = {}
                for name, obj in val.items():
                    json_dict["categories"][key][name] = obj.to_json()

        return json_dict


class SamplePhenotype(BaseModel):
    """Pydantic-based class to organize phenotype data per sample

    Attributes:
        s_id: the sample identifier
        value: the corresponding value if any
    """

    s_id: str
    value: Optional[float] = None

    def to_json(self: Self):
        return {
            "s_id": str(self.s_id),
            "value": self.value if self.value is not None else "N/A",
        }


class PhenoData(BaseModel):
    """Pydantic-based class to organize phenotype data from file

    Attributes:
        datatype: a string indicating the data type and the algorithm to use
        category: identifier assay
        s_phen_data: a list of SamplePhenotype instances of positive (active) samples
        s_negative: a list of sample IDs with no data - inactive (negative) samples
        f_ids_positive: a set of ids determined to be phenotype-associated
    """

    datatype: str
    category: str
    s_phen_data: list = []
    s_negative: set = set()
    f_ids_positive: set = set()

    def to_json(self: Self):
        return {
            "category": self.category,
            "datatype": self.datatype,
            "s_phen_data": [obj.to_json() for obj in self.s_phen_data],
            "s_negative": list(self.s_negative),
            "f_ids_positive": list(self.f_ids_positive),
        }


class SpecSimNet(BaseModel):
    """Pydantic-based class to organize info on a spectral similarity analysis run

    Attributes:
        algorithm: the identifier of the algorithm
        network: the full network as networkx Graph object for later cytoscape export
        subnetworks: a dict of subnetwork Graph objects with subnetwork int id as keys
        summary: a dict of clusters and associated features
    """

    algorithm: str
    network: Any
    subnetworks: dict
    summary: dict[int, set]

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "algorithm": self.algorithm,
            "subnetworks": {
                key: nx.cytoscape_data(value)
                for (key, value) in self.subnetworks.items()
            },
            "summary": {key: list(value) for (key, value) in self.summary.items()},
        }


class Stats(BaseModel):
    """Pydantic-based class to organize stats and general info.

    Attributes:
        rt_min: retention time start of the first feature peak, in minutes
        rt_max: retention time stop of the last feature peak, in minutes
        rt_range: range in minutes between rt_min and rt_max
        area_min: area under the curve for smallest peak across all features/samples
        area_max: area under the curve for biggest peak across all features/samples.
        samples: tuple of all sample ids in analysis run
        features: total number of features
        active_features: retained in analysis run
        inactive_features: filtered out during analysis run by FeatureFilter module
        GroupMData: instance of the GroupMData object containing group metadata
        networks: all similarity networks in analysis run
        phenotypes: list of PhenoData objects containing phenotype data
        spectral_library: a list of matchms.Spectrum instances
    """

    rt_min: Optional[float] = None
    rt_max: Optional[float] = None
    rt_range: Optional[float] = None
    area_min: Optional[int] = None
    area_max: Optional[int] = None
    samples: Optional[tuple] = None
    features: Optional[int] = None
    active_features: set = set()
    inactive_features: set = set()
    GroupMData: GroupMData = GroupMData()
    networks: Optional[dict[str, SpecSimNet]] = None
    phenotypes: Optional[list] = None
    spectral_library: Optional[list] = None

    def parse_mzmine3(self: Self, params: ParameterManager):
        """Parse a mzmine3 peaktable for general stats on analysis run.

        Arguments:
            params: instance of ParameterManager object holding user input data

        Notes:
            By default, all samples are grouped in group "DEFAULT".
        """
        df = pd.read_csv(params.PeaktableParameters.filepath)

        self.rt_min = df.loc[:, "rt_range:min"].min()
        self.rt_max = df.loc[:, "rt_range:max"].max()
        self.rt_range = self.rt_max - self.rt_min
        self.area_min = df.loc[:, "area"].min()
        self.area_max = df.loc[:, "area"].max()
        self.samples = tuple(
            sample.split(":")[1] for sample in df.filter(regex=":feature_state").columns
        )
        self.GroupMData.default_s_ids = set(self.samples)
        self.features = len(df["id"].tolist())
        self.active_features = set(df["id"].tolist())

    def to_json(self: Self) -> dict:
        """Export class attributes to json-dump compatible dict.

        Returns:
            A dictionary with class attributes as keys

        Notes:
            Attribute spectral library is not exported - matches are stored in
            feature annotation.
        """
        attributes = (
            ("rt_min", self.rt_min, float),
            ("rt_max", self.rt_max, float),
            ("rt_range", self.rt_range, float),
            ("area_min", self.area_min, int),
            ("area_max", self.area_max, int),
            ("samples", self.samples, list),
            ("features", self.features, int),
            ("nr_active_features", len(self.active_features), int),
            ("nr_inactive_features", len(self.inactive_features), int),
            ("active_features", self.active_features, list),
            ("inactive_features", self.inactive_features, list),
        )

        json_dict = {}

        for attribute in attributes:
            if attribute[1] is not None:
                json_dict[attribute[0]] = attribute[2](attribute[1])

        json_dict["nr_samples"] = len(self.samples) if self.samples is not None else []
        json_dict["groups"] = self.GroupMData.to_json()
        json_dict["networks"] = (
            {key: val.to_json() for key, val in self.networks.items()}
            if self.networks is not None
            else {}
        )
        json_dict["phenotypes"] = (
            [val.to_json() for val in self.phenotypes]
            if self.phenotypes is not None
            else []
        )

        return json_dict
