"""Organize the calling of data analysis modules.

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
from typing import Self

from pydantic import BaseModel

from fermo_core.data_analysis.annotation_manager.class_annotation_manager import (
    AnnotationManager,
)
from fermo_core.data_analysis.blank_assigner.class_blank_assigner import BlankAssigner
from fermo_core.data_analysis.chrom_trace_calculator.class_chrom_trace_calculator import (
    ChromTraceCalculator,
)
from fermo_core.data_analysis.feature_filter.class_feature_filter import FeatureFilter
from fermo_core.data_analysis.group_assigner.class_group_assigner import GroupAssigner
from fermo_core.data_analysis.group_factor_assigner.class_group_factor_assigner import (
    GroupFactorAssigner,
)
from fermo_core.data_analysis.phenotype_manager.class_phenotype_manager import (
    PhenotypeManager,
)
from fermo_core.data_analysis.score_assigner.class_score_assigner import ScoreAssigner
from fermo_core.data_analysis.sim_networks_manager.class_sim_networks_manager import (
    SimNetworksManager,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class AnalysisManager(BaseModel):
    """Pydantic-based class to organize calling and logging of analysis methods

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository

    def return_attributes(
        self: Self,
    ) -> tuple[Stats, Repository, Repository, ParameterManager]:
        """Returns modified attributes to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples, self.params

    def analyze(self: Self):
        """Organizes calling of data analysis steps."""
        logger.info("'AnalysisManager': started analysis steps.")

        self.run_feature_filter()
        self.run_sample_group_analysis()
        self.run_phenotype_manager()
        self.run_sim_networks_manager()
        self.run_annotation_manager()
        self.run_score_assignment()
        self.run_chrom_trace_calculator()

        logger.info("'AnalysisManager': completed analysis steps.")

    def run_feature_filter(self: Self):
        """Run optional FeatureFilter analysis step"""
        if not (
            self.params.FeatureFilteringParameters
            and self.params.FeatureFilteringParameters.activate_module
        ):
            logger.info("'FeatureFilter': not activated - SKIP.")
            return

        try:
            feature_filter = FeatureFilter(
                params=self.params,
                stats=self.stats,
                features=self.features,
                samples=self.samples,
            )
            feature_filter.filter()
            self.stats, self.features, self.samples = feature_filter.return_values()
            self.params.FeatureFilteringParameters.module_passed = True
        except Exception as e:
            logger.error(f"FeatureFilter failed: {e}")
            logger.error("FeatureFilter terminated prematurely - SKIP")
            return

    def run_sample_group_analysis(self):
        """Orchestrates functions"""
        self.run_blank_assignment()
        self.run_group_assignment()
        self.run_group_factor_assignment()

    def run_blank_assignment(self: Self):
        """Run optional blank_assignment analysis step"""
        if not self.params.GroupMetadataParameters:
            logger.info("'BlankAssigner': no group metadata file provided - SKIP")
            return

        if not (
            self.params.BlankAssignmentParameters
            and self.params.BlankAssignmentParameters.activate_module
        ):
            logger.info("'BlankAssigner': not activated - SKIP.")
            return

        if len(self.stats.GroupMData.blank_s_ids) == 0:
            logger.info("'BlankAssigner': no sample marked as 'BLANK' - SKIP")
            return

        if len(self.stats.GroupMData.nonblank_s_ids) == 0:
            logger.info("'BlankAssigner': all sample marked as 'BLANK' - SKIP")
            return

        try:
            blank_assigner = BlankAssigner(
                params=self.params, features=self.features, stats=self.stats
            )
            blank_assigner.run_analysis()
            self.stats, self.features = blank_assigner.return_attrs()
            self.params.BlankAssignmentParameters.module_passed = True
        except Exception as e:
            logger.error(f"BlankAssigner failed: {e}")
            logger.error("BlankAssigner terminated prematurely - SKIP")
            return

    def run_group_assignment(self: Self):
        """Run optional group_assignment analysis step

        Notes: must be called after BlankAssigner
        """
        if not self.params.GroupMetadataParameters:
            logger.info("'GroupAssigner': no group metadata file provided - SKIP")
            return

        try:
            group_assigner = GroupAssigner(features=self.features, stats=self.stats)
            group_assigner.run_analysis()
            self.stats, self.features = group_assigner.return_attrs()
        except Exception as e:
            logger.error(f"GroupAssigner failed: {e}")
            logger.error("GroupAssigner terminated prematurely - SKIP")
            return

    def run_group_factor_assignment(self: Self):
        """Run optional group_assignment analysis step

        Notes: must be called after BlankAssigner and GroupAssigner
        """

        if not self.params.GroupMetadataParameters:
            logger.info("'GroupFactorAssigner': no group metadata file provided - SKIP")
            return

        if not (
            self.params.GroupFactAssignmentParameters
            and self.params.GroupFactAssignmentParameters.activate_module
        ):
            logger.info(
                "'GroupFactorAssigner': "
                "'group_factor_assignment/activate_module' disabled - SKIP"
            )
            return

        try:
            group_fact_ass = GroupFactorAssigner(
                features=self.features, stats=self.stats, params=self.params
            )
            group_fact_ass.run_analysis()
            self.features = group_fact_ass.return_features()
            self.params.GroupFactAssignmentParameters.module_passed = True
        except Exception as e:
            logger.error(f"GroupFactorAssigner failed: {e}")
            logger.error("GroupFactorAssigner terminated prematurely - SKIP")
            return

    def run_phenotype_manager(self: Self):
        """Run optional PhenotypeManager analysis step"""
        if not self.params.PhenotypeParameters:
            logger.info("'PhenotypeManager': no phenotype data provided - SKIP.")
            return

        if not any(
            getattr(p, "activate_module", False)
            for p in [
                self.params.PhenoQualAssgnParams,
                self.params.PhenoQuantPercentAssgnParams,
                self.params.PhenoQuantConcAssgnParams,
            ]
        ):
            logger.info(
                "'PhenotypeManager': no modules in 'phenotype_assignment' activated - SKIP."
            )
            return

        try:
            phenotype_manager = PhenotypeManager(
                params=self.params,
                features=self.features,
                stats=self.stats,
                samples=self.samples,
            )
            phenotype_manager.run_analysis()
            self.stats, self.features, self.params = phenotype_manager.return_attrs()
        except Exception as e:
            logger.error(f"PhenotypeManager failed: {e}")
            logger.error("PhenotypeManager terminated prematurely - SKIP")
            return

    def run_sim_networks_manager(self: Self):
        """Run optional SimNetworksManager analysis step"""
        if not self.params.MsmsParameters:
            logger.info("'SimNetworksManager': no MS/MS data provided - SKIP.")
            return

        if not any(
            getattr(p, "activate_module", False)
            for p in [
                self.params.SpecSimNetworkCosineParameters,
                self.params.SpecSimNetworkDeepscoreParameters,
            ]
        ):
            logger.info(
                "'SimNetworksManager': no modules in 'spec_sim_networking' activated - SKIP."
            )
            return

        try:
            sim_networks_manager = SimNetworksManager(
                params=self.params,
                stats=self.stats,
                features=self.features,
                samples=self.samples,
            )
            sim_networks_manager.run_analysis()
            (self.stats, self.features, self.samples, self.params) = (
                sim_networks_manager.return_attrs()
            )
        except Exception as e:
            logger.error(f"SimNetworksManager failed: {e}")
            logger.error("SimNetworksManager terminated prematurely - SKIP")
            return

    def run_annotation_manager(self: Self):
        """Run optional AnnotationManager analysis step"""

        try:
            annotation_manager = AnnotationManager(
                params=self.params,
                stats=self.stats,
                features=self.features,
                samples=self.samples,
            )
            annotation_manager.run_analysis()
            self.stats, self.features, self.samples, self.params = (
                annotation_manager.return_attrs()
            )
        except Exception as e:
            logger.error(f"AnnotationManager failed: {e}")
            logger.error("AnnotationManager terminated prematurely - SKIP")
            return

    def run_score_assignment(self: Self):
        """Run mandatory score annotation analysis step"""
        try:
            score_assigner = ScoreAssigner(
                params=self.params,
                stats=self.stats,
                features=self.features,
                samples=self.samples,
            )
            score_assigner.run_analysis()
            self.features, self.samples = score_assigner.return_attributes()
        except Exception as e:
            logger.error(f"ScoreAssigner failed: {e}")
            logger.error("ScoreAssigner terminated prematurely - SKIP")
            return

    def run_chrom_trace_calculator(self: Self):
        """Run mandatory ChromTraceCalculator analysis step."""
        try:
            self.samples = ChromTraceCalculator().modify_samples(
                self.samples, self.stats
            )
        except Exception as e:
            logger.error(f"ChromTraceCalculator failed: {e}")
            logger.error("ChromTraceCalculator terminated prematurely - SKIP")
            return
