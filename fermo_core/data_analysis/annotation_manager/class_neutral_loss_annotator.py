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

from fermo_core.config.class_default_settings import NeutralMasses, PeptideHintAdducts
from fermo_core.data_analysis.annotation_manager.class_adduct_annotator import (
    AdductAnnotator,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Ribosomal,
    NonRibosomal,
    NeutralLoss,
    Feature,
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
    mass: NeutralMasses = NeutralMasses()

    def return_features(self: Self) -> Repository:
        """Returns modified attributes from NeutralLossAnnotator to the calling function

        Returns:
            Modified Feature Repository objects.
        """
        return self.features

    def run_adduct_annotator(self: Self):
        """Run AdductAnnotator module - module switched off by user."""
        logger.info(
            "'AnnotationManager/NeutralLossAnnotator': needs adduct annotation "
            "to run, but module 'AdductAnnotator' is not activated. Attempt to "
            "run 'AdductAnnotator' module with default values."
        )
        adduct_annotator = AdductAnnotator(
            params=self.params,
            stats=self.stats,
            features=self.features,
            samples=self.samples,
        )
        try:
            adduct_annotator.run_analysis()
            self.features = adduct_annotator.return_features()
            logger.info("'AnnotationManager': completed feature adduct annotation.")
            return
        except ZeroDivisionError as e:
            logger.error(str(e))
            logger.error(
                "'AnnotationManager/AdductAnnotator': Attempted division through "
                "zero when calculating mass deviation - SKIP"
            )
            return

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""

        if self.params.MsmsParameters is None:
            logger.warning(
                "'AnnotationManager/NeutralLossAnnotator': no MS2 file provided - SKIP"
            )
            return

        if self.params.AdductAnnotationParameters.activate_module is False:
            self.run_adduct_annotator()

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
                self.collect_evidence_pos(f_id)
        else:
            logger.warning(
                "'AnnotationManager/NeutralLossAnnotator': negative ion mode detected. "
                "Negative ion mode neutral loss determination not yet implemented - "
                "SKIP"
            )
            return
            # TODO(MMZ 18.04.24): implement negative ion mode

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
        # TODO(MMZ 18.04.24): expand for other loss categories

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
                    m1=loss, m2=ref_loss.mass, f_id_m2=ref_loss.id
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.losses is None:
                        feature.Annotations.losses = []
                    if feature.Annotations.classes is None:
                        feature.Annotations.classes = {}
                    if feature.Annotations.classes.get("ribosomal") is None:
                        feature.Annotations.classes["ribosomal"] = Ribosomal()

                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=ref_loss.id, mz_det=loss, mz_ex=ref_loss.mass, diff=ppm
                        )
                    )
                    feature.Annotations.classes.get("ribosomal").aa_tags.append(
                        ref_loss.ribo_tag
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
                    m1=loss, m2=ref_loss.mass, f_id_m2=ref_loss.id
                )
                if ppm < self.params.NeutralLossParameters.mass_dev_ppm:
                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.losses is None:
                        feature.Annotations.losses = []
                    if feature.Annotations.classes is None:
                        feature.Annotations.classes = {}
                    if feature.Annotations.classes.get("nonribosomal") is None:
                        feature.Annotations.classes["nonribosomal"] = NonRibosomal()

                    feature.Annotations.losses.append(
                        NeutralLoss(
                            id=ref_loss.id, mz_det=loss, mz_ex=ref_loss.mass, diff=ppm
                        )
                    )
                    feature.Annotations.classes.get("nonribosomal").monomer_tags.append(
                        ref_loss.nribo_tag
                    )

        return feature

    def collect_evidence_pos(self: Self, f_id: int):
        """Collect available evidence for peptidic classes

        Arguments:
            f_id: the feature ID
        """
        # TODO(MMZ 18.04.24): rework this method - make nicer

        feature = self.features.get(f_id)

        if feature.Annotations is None:
            logger.debug(
                f"'AnnotationManager/NeutralLossAnnotator': feature ID '{f_id}' has "
                f"no Annotation - SKIP "
            )
            return

        if feature.Annotations.classes is not None:
            if feature.Annotations.classes.get("ribosomal") is not None:
                if len(feature.Annotations.classes.get("ribosomal").aa_tags) > 0:
                    feature.Annotations.classes.get("ribosomal").evidence.append(
                        f"Neutral losses: detected "
                        f"'{len(feature.Annotations.classes.get('ribosomal').aa_tags)}' "
                        f"typical loss(es)."
                    )

                if (
                    feature.Annotations.adducts is not None
                    and len(feature.Annotations.adducts) > 0
                ):
                    adduct_types = set()
                    for adduct in feature.Annotations.adducts:
                        adduct_types.add(adduct.adduct_type)
                    if not adduct_types.isdisjoint(PeptideHintAdducts().adducts):
                        feature.Annotations.classes.get("ribosomal").evidence.append(
                            "Adducts: typical multicharged adduct(s) detected."
                        )

                if feature.mz > 1500:
                    feature.Annotations.classes.get("ribosomal").evidence.append(
                        "Weight: typical for a ribosomal peptide."
                    )

            if feature.Annotations.classes.get("nonribosomal") is not None:
                if (
                    len(feature.Annotations.classes.get("nonribosomal").monomer_tags)
                    > 0
                ):
                    feature.Annotations.classes.get("nonribosomal").evidence.append(
                        f"Neutral losses: detected "
                        f"'{len(feature.Annotations.classes.get('nonribosomal').monomer_tags)}' "
                        f"typical loss(es)."
                    )

                if (
                    feature.Annotations.adducts is not None
                    and len(feature.Annotations.adducts) > 0
                ):
                    adduct_types = set()
                    for adduct in feature.Annotations.adducts:
                        adduct_types.add(adduct.adduct_type)
                    if not adduct_types.isdisjoint(PeptideHintAdducts().adducts):
                        feature.Annotations.classes.get("nonribosomal").evidence.append(
                            "Adducts: typical multicharged adduct(s) detected."
                        )

        self.features.modify(f_id, feature)
