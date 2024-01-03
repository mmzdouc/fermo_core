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
from typing import Self, Tuple, Optional, Set, Dict, List

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


class Stats:
    """Extract analysis run stats and organize them.

    Ad method nomenclature: each type of supported peaktable should have a separate
    parser method attributed to it that has the name of the peaktable in it.
    All methods addressing a peaktable format should mention it in method name.

    Attributes:
        rt_min: overall lowest retention time start across all samples, in minutes
        rt_max: overall highest retention time stop across all samples, in minutes
        rt_range: range in minutes between min and max rt.
        samples: all sample ids in analysis run
        features: all feature ids in analysis run in a tuple
        groups: a dict of lists containing sample ID strings to indicate membership in
                groups (if no explicit information, all samples in group "DEFAULT")
        cliques: all similarity cliques in analysis run
        phenotypes: a dict of tuples of experiments, with associated active samples
        blank: all blank-associated features in analysis run
        int_removed: all features that were removed due to intensity range
        annot_removed: all features that were removed due to annotation range
        ms2_removed: feature IDs of which MS2 was removed
        spectral_library: a dict of SpecLibEntry instances
    """

    def __init__(self: Self):
        self.rt_min: Optional[float] = None
        self.rt_max: Optional[float] = None
        self.rt_range: Optional[float] = None
        self.samples: Optional[Tuple] = None
        self.features: Optional[Tuple] = None
        self.groups: Optional[Dict[str, Set[str | int]]] = {"DEFAULT": set()}
        self.cliques: Optional[Tuple] = None
        self.phenotypes: Optional[Dict[str, Tuple[str, ...]]] = None
        self.blank: Optional[Tuple] = None
        self.int_removed: Optional[Tuple] = None
        self.annot_removed: Optional[Tuple] = None
        self.ms2_removed: Optional[List] = None
        self.spectral_library: Optional[Dict[int, SpecLibEntry]] = None

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
        self.samples = tuple(
            sample.split(":")[1] for sample in df.filter(regex=":feature_state").columns
        )
        self.groups["DEFAULT"] = set(self.samples)
        self.features = tuple(df["id"].tolist())

        # TODO(MMZ 3.1.24): move to FeatureFilter class
        # self.features, self.int_removed = self._get_features_in_range_mzmine3(
        #     df, params.PeaktableFilteringParameters.filter_rel_int_range
        # )
        # _, self.annot_removed = self._get_features_in_range_mzmine3(
        #     df, params.Ms2QueryAnnotationParameters.filter_rel_int_range
        # )
