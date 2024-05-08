"""Run the phenotype quantitative data assignment.

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
import logging
from statistics import mean, median
from typing import Self, Tuple, Optional

from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import Phenotype
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class PhenQuantAssigner(BaseModel):
    """Pydantic-based class to run quantitative phenotype assignment

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object holding Sample objects
        f_ids_intersect: the intersection of positive and negative feature IDs
    """

    # TODO(MMZ 08.05): TEST THIS CLASS
    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    f_ids_intersect: Optional[set] = None

    def return_values(self: Self) -> Tuple[Stats, Repository]:
        """Return the modified objects to the calling function

        Returns:
            The modified Stats and Repository objects
        """
        return self.stats, self.features

    def collect_sets(self: Self):
        """Collect sets of active and inactive features and assign actives"""
        f_ids_in_inactives = set()
        for s_id in set(self.stats.phenotypes[0].s_negative):
            sample = self.samples.get(s_id)
            f_ids_in_inactives.update(set(sample.feature_ids))

        f_ids_in_actives = set()
        for s_id in set(self.stats.samples).difference(
            set(self.stats.phenotypes[0].s_negative)
        ):
            sample = self.samples.get(s_id)
            f_ids_in_actives.update(set(sample.feature_ids))

        f_ids_in_actives = f_ids_in_actives.difference(
            self.stats.GroupMData.blank_f_ids
        )
        f_ids_in_inactives = f_ids_in_inactives.difference(
            self.stats.GroupMData.blank_f_ids
        )

        self.f_ids_intersect = f_ids_in_actives.intersection(f_ids_in_inactives)

        for f_id in f_ids_in_actives.difference(f_ids_in_inactives):
            feature = self.features.get(f_id)
            feature.phenotypes = [
                Phenotype(
                    score=0, format="qualitative", descr="only in positive samples"
                )
            ]
            self.features.modify(f_id, feature)

    def get_value(self: Self, f_id: int, sample_ids: set) -> list:
        """Retrieve values based on area or height

        Arguments:
            f_id: a feature ID
            sample_ids: the sample Ids to retrieve

        Returns:
            A list of collected values
        """
        feature = self.features.get(f_id)
        values_s_ids = []

        if self.params.PhenoQuantAssgnParams.value == "area":
            for entry in feature.area_per_sample:
                if entry.s_id in sample_ids:
                    values_s_ids.append(entry.value)
        else:
            for entry in feature.height_per_sample:
                if entry.s_id in sample_ids:
                    values_s_ids.append(entry.value)

        return values_s_ids

    def bin_intersection(self):
        """Bin the intersection between positive and negative f_ids based on factor

        Raises:
            RuntimeError: unsupported algorithm
        """
        for f_id in self.f_ids_intersect:
            feature = self.features.get(f_id)

            s_actv = set(self.stats.samples).difference(
                set(self.stats.phenotypes[0].s_negative)
            )
            s_actv = s_actv.intersection(feature.samples)
            vals_act = self.get_value(f_id, s_actv)

            s_inactv = set(self.stats.phenotypes[0].s_negative)
            s_inactv = s_inactv.intersection(feature.samples)
            vals_inact = self.get_value(f_id, s_inactv)

            match self.params.PhenoQuantAssgnParams.algorithm:
                case "minmax":
                    factor = min(vals_act) / max(vals_inact)
                    if factor >= self.params.PhenoQuantAssgnParams.factor:
                        feature.phenotypes = [
                            Phenotype(score=factor, format="qualitative")
                        ]
                case "mean":
                    factor = mean(vals_act) / mean(vals_inact)
                    if factor >= self.params.PhenoQuantAssgnParams.factor:
                        feature.phenotypes = [
                            Phenotype(score=factor, format="qualitative")
                        ]
                case "median":
                    factor = median(vals_act) / median(vals_inact)
                    if factor >= self.params.PhenoQuantAssgnParams.factor:
                        feature.phenotypes = [
                            Phenotype(score=factor, format="qualitative")
                        ]
                case _:
                    raise RuntimeError("Unsupported algorithm.")

            self.features.modify(f_id, feature)

    def run_analysis(self: Self):
        """Run the phenotype annotation analysis

        Raise:
            RuntimeError: self.phenotypes not specified
        """
        if self.stats.phenotypes is None:
            raise RuntimeError(
                "'PhenQuantAssigner': self.phenotypes not specified - SKIP"
            )

        self.collect_sets()
        self.bin_intersection()
