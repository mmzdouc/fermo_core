"""Runs the neutral loss annotation module.

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
from typing import Self

from pydantic import BaseModel

from fermo_core.config.class_default_settings import NeutralLosses
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Feature,
    NeutralLoss,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils

logger = logging.getLogger("fermo_core")


class NeutralLossAnnotator(BaseModel):
    """Pydantic-based class for calling and logging of neutral loss annotation

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
        mass: NeutralMasses object storing hardcoded values
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    mass: NeutralLosses = NeutralLosses()

    def return_features(self: Self) -> Repository:
        """Returns modified Feature objects in Repository object instance

        Returns:
            Modified Feature Repository object.
        """
        return self.features

    def annotate_feature_neg(self: Self, f_id: int):
        """Annotate neutral losses of feature and store data in General Feature

        Arguments:
            f_id: the feature ID
        """
        feature = self.features.get(f_id)

        if feature.Spectrum is None or len(feature.Spectrum.peaks.mz) == 0:
            logger.debug(
                f"'AnnotationManager/NeutralLossAnnotator': feature ID '{f_id}' has "
                f"no associated MS/MS spectrum - SKIP "
            )
            return
        else:
            feature = self.validate_gen_other_neg_losses(feature)
            self.features.modify(f_id, feature)

    @staticmethod
    def add_annotation(feature: Feature) -> Feature:
        """Adds annotation data storage to feature

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        if feature.Annotations is None:
            feature.Annotations = Annotations()
        if feature.Annotations.losses is None:
            feature.Annotations.losses = []
        return feature

    def validate_gen_other_neg_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of generic losses of biol/synth origin

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.gen_other_neg:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=f"{ref_loss.descr}({ref_loss.abbr})",
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def annotate_feature_pos(self: Self, f_id: int):
        """Annotate neutral losses of feature and store data in General Feature

        Arguments:
            f_id: the feature ID
        """
        feature = self.features.get(f_id)

        if feature.Spectrum is None or len(feature.Spectrum.peaks.mz) == 0:
            logger.debug(
                f"'AnnotationManager/NeutralLossAnnotator': feature ID '{f_id}' has "
                f"no associated MS/MS spectrum - SKIP "
            )
            return

        feature = self.validate_ribosomal_losses(feature)
        feature = self.validate_nonribosomal_losses(feature)
        feature = self.validate_glycoside_losses(feature)
        feature = self.validate_gen_bio_pos_losses(feature)
        if self.params.NeutralLossParameters.nonbiological is True:
            feature = self.validate_gen_other_pos_losses(feature)

        self.features.modify(f_id, feature)

    def validate_ribosomal_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of losses derived from ribosomal peptides

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.ribosomal:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=(
                                f"{ref_loss.descr}(ribosomal, putatively from AAs "
                                f"{ref_loss.abbr})"
                            ),
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def validate_nonribosomal_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of losses derived from nonribosomal peptides

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.nonribo:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=(
                                f"{ref_loss.descr}({ref_loss.abbr}, putatively from "
                                f"nonribosomal peptide)"
                            ),
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def validate_glycoside_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of glycoside losses

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.glycoside:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=(
                                f"{ref_loss.descr}({ref_loss.abbr}, putatively from "
                                f"glycoside)"
                            ),
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def validate_gen_bio_pos_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of generic losses of biological origin

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.gen_bio_pos:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=(
                                f"{ref_loss.descr}({ref_loss.abbr}, putatively from "
                                f"metabolite)"
                            ),
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def validate_gen_other_pos_losses(self: Self, feature: Feature) -> Feature:
        """Validate losses against a list of generic losses of biol/synth origin

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for loss in feature.Spectrum.losses.mz:
            for ref_loss in self.mass.gen_other_pos:
                ppm = Utils().mass_deviation(
                    m1=loss, m2=ref_loss.loss, f_id_m2=ref_loss.descr
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=f"{ref_loss.descr}({ref_loss.abbr})",
                            loss_det=loss,
                            loss_ex=ref_loss.loss,
                            mz_frag=(feature.mz - loss),
                            diff=ppm,
                        )
                    )
        return feature

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""

        if self.params.MsmsParameters is None:
            logger.warning(
                "'AnnotationManager/NeutralLossAnnotator': no MS2 file provided - SKIP"
            )
            return

        if len(self.stats.active_features) == 0:
            logger.warning(
                "'AnnotationManager/NeutralLossAnnotator': no active features - SKIP"
            )
            return

        if self.params.PeaktableParameters.polarity == "positive":
            logger.info(
                "'AnnotationManager/NeutralLossAnnotator': positive ion mode detected. "
                "Attempt to annotate for positive ion mode neutral losses."
            )
            for f_id in self.stats.active_features:
                self.annotate_feature_pos(f_id)
        else:
            logger.info(
                "'AnnotationManager/NeutralLossAnnotator': negative ion mode detected. "
                "Attempt to annotate for negative ion mode neutral losses."
            )
            for f_id in self.stats.active_features:
                self.annotate_feature_neg(f_id)
