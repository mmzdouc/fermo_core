"""Assign scores for Feature and Sample object instances.

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
from statistics import mean
from typing import Self

from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Scores as FeatureScores,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import (
    Scores as SampleScores,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class ScoreAssigner(BaseModel):
    """Pydantic-based class to organize assignment of scores to Features and Samples

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
        networks: intermediate storage of sample:set of network ids
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    networks: dict = {}

    def return_attributes(self: Self) -> tuple[Repository, Repository]:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing Feature Repository and Sample Repository objects.
        """
        return self.features, self.samples

    def assign_feature_scores(self: Self):
        """Assign scores to feature objects"""
        for f_id in self.stats.active_features:
            feature = self.features.get(f_id)
            feature.Scores = FeatureScores()

            if (
                feature.Annotations is not None
                and feature.Annotations.phenotypes is not None
                and len(feature.Annotations.phenotypes) != 0
            ):
                phen_scores = [assay.score for assay in feature.Annotations.phenotypes]
                feature.Scores.phenotype = max(phen_scores)

            if (
                feature.Annotations is not None
                and feature.Annotations.matches is not None
                and len(feature.Annotations.matches) != 0
            ):
                annot_scores = [match.score for match in feature.Annotations.matches]
                feature.Scores.novelty = 1 - max(annot_scores)

            self.features.modify(f_id, feature)

    def collect_sample_spec_networks(self: Self):
        """Collect sample:set of network ids for each used algorithm

        Raises:
            RuntimeError: no networks detected
        """
        if self.stats.networks is None or len(self.stats.networks) == 0:
            RuntimeError(
                "'ScoreAssigner': no networks detected - cannot assign Sample "
                "scores - SKIP"
            )

        for algorithm, network in self.stats.networks.items():
            if len(network.summary) == 0:
                continue

            self.networks[algorithm] = {}
            for s_id in self.stats.samples:
                self.networks[algorithm][s_id] = set()

                sample = self.samples.get(s_id)
                for cluster_id, f_id_set in network.summary.items():
                    if not f_id_set.isdisjoint(sample.feature_ids):
                        self.networks[algorithm][s_id].add(cluster_id)

                        if sample.networks is None:
                            sample.networks = {}
                        if sample.networks.get(algorithm) is None:
                            sample.networks[algorithm] = {cluster_id}
                        else:
                            sample.networks[algorithm].add(cluster_id)
                        self.samples.modify(s_id, sample)

    def assign_sample_scores(self: Self):
        """Assign scores to sample objects"""
        self.collect_sample_spec_networks()

        for s_id in self.stats.samples:
            sample = self.samples.get(s_id)
            sample.Scores = SampleScores()

            nw_diversity = {}
            for algorithm, network in self.networks.items():
                nw_diversity[algorithm] = len(network[s_id]) / len(
                    self.stats.networks[algorithm].summary
                )
            sample.Scores.diversity = max([val for key, val in nw_diversity.items()])

            nm_specificity = {}
            for algorithm, network in self.networks.items():
                nws_other_samples = set()
                for sample_id, nw_set in network.items():
                    if sample_id != s_id:
                        nws_other_samples.update(nw_set)
                nm_specificity[algorithm] = len(
                    network[s_id].difference(nws_other_samples)
                ) / len(self.stats.networks[algorithm].summary)
            sample.Scores.specificity = max(
                [val for key, val in nm_specificity.items()]
            )

            novelty_scores = []
            for f_id in sample.feature_ids:
                feature = self.features.get(f_id)
                if feature.Scores is not None and feature.Scores.novelty is not None:
                    novelty_scores.append(feature.Scores.novelty)
            if len(novelty_scores) != 0:
                sample.Scores.mean_novelty = mean(novelty_scores)

            self.samples.modify(s_id, sample)

    def run_analysis(self: Self):
        """Run analysis steps to assign scores to Feature and Sample instances."""
        logger.info("'ScoreAssigner': started score assignment.")
        self.assign_feature_scores()
        self.assign_sample_scores()
        logger.info("'ScoreAssigner': completed score assignment.")
