"""Runs the ms2deepscore library annotation module.

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
from typing import Self, Optional, Any
import urllib.error

import func_timeout
import matchms
from ms2deepscore import MS2DeepScore
from ms2deepscore.models import load_model
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultSettings
from fermo_core.utils.utility_method_manager import UtilityMethodManager
from fermo_core.data_processing.class_repository import Repository

logger = logging.getLogger("fermo_core")


class Ms2deepscoreAnnotator(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2deepscore lib matching

    Attributes:
        features: Repository object, holds "General Feature" objects
        active_features: a set of active features
        polarity: the ion mode polarity
        library: a list of Spectrum object representing the library to match against
        queries: a list of Spectra for which to perform matching
        scores: a matchms.Scores object storing the raw results of the matching
        max_time: maximum allowed calculation time of individual steps
        score_cutoff: minimum score for a match
        max_precursor_mass_diff: maximum precursor mass difference
    """

    features: Repository
    active_features: set
    polarity: str
    library: list
    queries: Optional[list] = None
    scores: Optional[Any] = None
    max_time: int
    score_cutoff: float
    max_precursor_mass_diff: float

    def log_ms2deepscore_timeout(self: Self):
        """Logs timeout due to long-running ms2deepscore library matching"""
        logger.warning(
            f"'AnnotationManager/Ms2deepscoreAnnotator': timeout of "
            f"ms2deepscore-based calculation "
            f"- took longer than maximum set time of '{self.max_time}' seconds.  "
            f"For unlimited runtime, set 'maximum_runtime' parameter to 0 (zero) - SKIP"
        )

    def return_scores(self: Self) -> matchms.Scores:
        """Return the generated matchms Scores object

        Returns:
            A matchms.Scores object
        """
        return self.scores

    def prepare_queries(self: Self):
        """Prepare a filtered list of query spectra for matching

        Raise:
            RuntimeError: no query spectra collected (empty list)
        """
        query_spectra = []
        for f_id in self.active_features:
            feature = self.features.get(f_id)
            if feature.Spectrum is None:
                logger.debug(
                    f"'AnnotationManager/Ms2deepscoreAnnotator': feature with id "
                    f"'{feature.f_id}' has no associated MS2 spectrum - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)

        if len(query_spectra) != 0:
            self.queries = query_spectra
        else:
            logger.warning(
                "'AnnotationManager/Ms2deepscoreAnnotator': no query spectra could be "
                "collected for matching - SKIP "
            )
            raise RuntimeError

    def calculate_scores_ms2deepscore(self: Self):
        """Calculate matchms scores using ms2deepscore algorithm

        Raises:
            RuntimeError: fatal error preventing successful execution of module - abort
            func_timeout.FunctionTimedOut: ms2deepscore calc takes too long.
            urllib.error.URLError: download failed
        """
        if self.polarity != "positive":
            logger.warning(
                "'AnnotationManager/Ms2deepscoreMatcher': specified ionization "
                "polarity invalid. This MS2DeepScore version only supports positive "
                "ion mode - SKIP."
            )
            raise RuntimeError

        try:
            if not UtilityMethodManager().check_ms2deepscore_req():
                UtilityMethodManager().download_ms2deepscore_req(self.max_time)
        except urllib.error.URLError as e:
            raise e

        if self.queries is None or len(self.queries) == 0:
            logger.warning(
                "'AnnotationManager/Ms2deepscoreMatcher': no query spectra - SKIP "
            )
            raise RuntimeError

        model = load_model(
            DefaultSettings().dirpath_ms2deepscore.joinpath(
                DefaultSettings().filename_ms2deepscore
            )
        )

        sim_algorithm = MS2DeepScore(model=model, progress_bar=False)

        if self.max_time == 0:
            self.scores = matchms.calculate_scores(
                references=self.library,
                queries=self.queries,
                similarity_function=sim_algorithm,
            )
        else:
            try:
                self.scores = func_timeout.func_timeout(
                    timeout=self.max_time,
                    func=matchms.calculate_scores,
                    kwargs={
                        "references": self.library,
                        "queries": self.queries,
                        "similarity_function": sim_algorithm,
                    },
                )
            except func_timeout.FunctionTimedOut as e:
                self.log_ms2deepscore_timeout()
                raise e

    def filter_match(self: Self, match: tuple, f_mz: float) -> bool:
        """Filter matches for user-specified params

        Arguments:
            match: a tuple of (matchms.Spectrum, score)
            f_mz: the m/z of the matched feature

        Returns:
            A bool indicating if match is inside the settings (True) or not (False)
        """
        if match[1] < self.score_cutoff:
            return False
        elif (
            abs(match[0].metadata.get("precursor_mz") - f_mz)
            > self.max_precursor_mass_diff
        ):
            return False
        else:
            return True
