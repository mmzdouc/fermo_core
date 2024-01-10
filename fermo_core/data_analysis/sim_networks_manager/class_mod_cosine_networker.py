"""Organize modified cosine spectral similarity networking methods.

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
from typing import Dict, Self

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)


class ModCosineNetworker:
    """Class for calling and logging modified cosine spect. sim. networking"""

    @staticmethod
    def log_filtered_feature_no_msms(f_id: int):
        """Logs feature filtered from selection due to lack of MS/MS

        Arguments:
            f_id: feature identifier
        """
        logging.debug(
            f"'ModCosineNetworker': feature ID '{f_id}' filtered from spectral "
            f"similarity networking: has no associated MS/MS."
        )

    @staticmethod
    def log_filtered_feature_nr_fragments(f_id: int, frags: int, min_frags: int):
        """Logs feature filtered from selection due to low number of MS/MS fragments

        Arguments:
            f_id: feature identifier
            frags: found nr of MS/MS fragments
            min_frags: minimal necessary nr or MS/MS fragments
        """
        logging.debug(
            f"'ModCosineNetworker': feature ID '{f_id}' filtered from spectral "
            f"similarity networking: min. nr. of MS/MS fragments lower than required "
            f"by parameter 'msms_min_frag_nr' ('{frags}' < '{min_frags}')."
        )

    def filter_input_spectra(
        self: Self,
        features: tuple,
        feature_repo: Repository,
        settings: SpecSimNetworkCosineParameters,
    ) -> Dict[str, set]:
        """Filter features for spectral similarity analysis based on given restrictions.

        Attributes:
            features: a tuple of feature IDs
            feature_repo: containing GeneralFeature objects with feature info
            settings: containing given filter parameters

        Returns:
            A dictionary containing included and excluded feature ints in sets.
        """
        included = set()
        excluded = set()

        for f_id in features:
            feature = feature_repo.get(f_id)
            if feature.Spectrum is None:
                excluded.add(f_id)
                self.log_filtered_feature_no_msms(f_id)
            elif len(feature.Spectrum.peaks.mz) < settings.msms_min_frag_nr:
                excluded.add(f_id)
                self.log_filtered_feature_nr_fragments(
                    f_id, len(feature.Spectrum.peaks.mz), settings.msms_min_frag_nr
                )
            else:
                included.add(f_id)

        return {"included": included, "excluded": excluded}

        # TODO(MMZ 10.1.24): add a test for first condition

        # TODO(MMZ 9.1.24): Add self -> needs logging messages that can be called in
        #  to log why a particular MSMS is not considered - more trackable

        # TODO(MMZ 9.1.24): contrinue here: finish function and write test,
        #  then continue with next method (spectral matching

        # dont forget about logging
