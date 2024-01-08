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
import pandas as pd
from pydantic import BaseModel
from typing import Self, Tuple, Optional, Set, Dict

from fermo_core.input_output.class_parameter_manager import ParameterManager


class SpecLibEntry(BaseModel):
    """Pydantic-based class to organize information on a spectral library entry

    Attributes:
        name: the name of the entry
        exact_mass: the exact mass of the entry
        msms: a tuple of two tuples: [1] fragments, [2] intensities
    """

    name: str
    exact_mass: float
    msms: Tuple[Tuple[float, ...], Tuple[float, ...]]


class Stats(BaseModel):
    """Pydantic-based class to organize stats and general info.

    Attributes:
        rt_min: retention time start of the first feature peak, in minutes
        rt_max: retention time stop of the last feature peak, in minutes
        rt_range: range in minutes between rt_min and rt_max
        area_min: area under the curve for smallest peak across all features/samples
        area_max: area under the curve for biggest peak across all features/samples.
        samples: tuple of all sample ids in analysis run
        features: tuple of all feature ids in analysis run
        active_features: not filtered from analysis run
        inactive_features: filtered from analysis run
        groups: dict of sets of sample IDs repr. group membership (default in DEFAULT)
        cliques: all similarity cliques in analysis run
        phenotypes: dict of tuples of active sample IDs
        blank: all blank-associated features in analysis run
        spectral_library: a dict of SpecLibEntry instances
    """

    rt_min: Optional[float] = None
    rt_max: Optional[float] = None
    rt_range: Optional[float] = None
    area_min: Optional[int] = None
    area_max: Optional[int] = None
    samples: Optional[Tuple] = None
    features: Optional[Tuple] = None
    active_features: set = set()
    inactive_features: set = set()
    groups: Optional[Dict[str, Set]] = {"DEFAULT": set()}
    cliques: Optional[Tuple] = None
    phenotypes: Optional[Dict[str, Tuple[str, ...]]] = None
    blank: Optional[Tuple] = None
    spectral_library: Optional[Dict[int, SpecLibEntry]] = None

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
        self.groups["DEFAULT"] = set(self.samples)
        self.features = tuple(df["id"].tolist())
        self.active_features = set(self.features)
