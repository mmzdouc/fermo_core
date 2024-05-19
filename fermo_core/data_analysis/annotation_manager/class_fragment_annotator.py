"""Runs the fragment annotation module.

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

from fermo_core.config.class_default_settings import CharFragments
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    CharFrag,
    Feature,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager as Utils

logger = logging.getLogger("fermo_core")


class FragmentAnnotator(BaseModel):
    """Pydantic-based class for calling and logging of fragment annotation

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
        frags: CharFragments object storing hardcoded values
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    frags: CharFragments = CharFragments()

    def return_features(self: Self) -> Repository:
        """Returns modified Feature objects in Repository object instance

        Returns:
            Modified Feature Repository object.
        """
        return self.features

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
        if feature.Annotations.fragments is None:
            feature.Annotations.fragments = []
        return feature

    def validate_pos_aa_fragments(self: Self, feature: Feature) -> Feature:
        """Validate frags against a list of amino acid y2 and b2 ions (positive mode)

        Arguments:
            feature: a feature object instance

        Returns:
            the modified feature object instance
        """
        for frag in feature.Spectrum.peaks.mz:
            for ref_frag in self.frags.aa_frags:
                ppm = Utils().mass_deviation(
                    m1=frag, m2=ref_frag.mass, f_id_m2=ref_frag.descr
                )
                if ppm < self.params.FragmentAnnParameters.mass_dev_ppm:
                    feature = self.add_annotation(feature)
                    feature.Annotations.fragments.append(
                        CharFrag(
                            id=ref_frag.descr,
                            frag_det=frag,
                            frag_ex=ref_frag.mass,
                            diff=ppm,
                        )
                    )
        return feature

    def annotate_feature_pos(self: Self, f_id: int):
        """Annotate positive mode ion frags of feature and store data in General Feature

        Arguments:
            f_id: the feature ID
        """
        feature = self.features.get(f_id)

        if feature.Spectrum is None or len(feature.Spectrum.peaks.mz) == 0:
            logger.debug(
                f"'AnnotationManager/FragmentAnnotator': feature ID '{f_id}' has "
                f"no associated MS/MS spectrum - SKIP "
            )
            return

        feature = self.validate_pos_aa_fragments(feature)
        self.features.modify(f_id, feature)

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""

        if self.params.MsmsParameters is None:
            logger.warning(
                "'AnnotationManager/FragmentAnnotator': no MS2 file provided - SKIP"
            )
            return

        if len(self.stats.active_features) == 0:
            logger.warning(
                "'AnnotationManager/FragmentAnnotator': no active features - SKIP"
            )
            return

        if self.params.PeaktableParameters.polarity == "positive":
            logger.info(
                "'AnnotationManager/FragmentAnnotator': positive ion mode detected. "
                "Attempt to annotate for positive ion mode fragments."
            )
            for f_id in self.stats.active_features:
                self.annotate_feature_pos(f_id)
        else:
            logger.warning(
                "'AnnotationManager/FragmentAnnotator': negative ion mode detected. "
                "Currently, negative ion mode fragment annotation is not implemented - "
                "SKIP"
            )
            return
