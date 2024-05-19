"""Runs the ms2deepscore library annotation module.

Copyright (c) 2024 Mitja Maximilian Zdouc, PhD

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
from typing import Any, Optional, Self
from urllib.parse import urlparse

import func_timeout
import matchms
from ms2deepscore import MS2DeepScore
from ms2deepscore.models import load_model
from pydantic import BaseModel

from fermo_core.config.class_default_settings import DefaultPaths
from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Match,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.utils.utility_method_manager import UtilityMethodManager

logger = logging.getLogger("fermo_core")


class Ms2deepscoreAnnotator(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2deepscore lib matching

    Attributes:
        features: Repository object, holds "General Feature" objects
        active_features: a set of active features
        polarity: the ion mode polarity
        library: a list of Spectrum object representing the library to match against
        library_name: the name of the library that is matched against
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
    library_name: str
    queries: Optional[list] = None
    scores: Optional[Any] = None
    max_time: int
    score_cutoff: float
    max_precursor_mass_diff: float

    def return_features(self: Self) -> Repository:
        """Return the modified Feature objects as Repository object

        Returns:
            A Repository object with modified Feature objects
        """
        return self.features

    def prepare_queries(self: Self):
        """Prepare a filtered list of query spectra for matching

        Raise:
            RuntimeError: no query spectra collected (empty list)
        """
        query_spectra = []
        for f_id in self.active_features:
            feature = self.features.get(f_id)
            if feature.Spectrum is None or len(feature.Spectrum.peaks.mz) == 0:
                logger.debug(
                    f"'AnnotationManager/Ms2deepscoreAnnotator': feature with ID "
                    f"'{feature.f_id}' has no associated MS2 spectrum - SKIP"
                )
                continue
            else:
                query_spectra.append(feature.Spectrum)

        if len(query_spectra) != 0:
            self.queries = query_spectra
            return
        else:
            raise RuntimeError(
                "'AnnotationManager/Ms2deepscoreAnnotator': no query spectra qualify "
                "for matching - SKIP"
            )

    def calculate_scores_ms2deepscore(self: Self):
        """Calculate matchms scores using ms2deepscore algorithm

        Raises:
            RuntimeError: fatal error preventing successful execution of module - abort
            func_timeout.FunctionTimedOut: ms2deepscore calc takes too long.
        """
        UtilityMethodManager().check_ms2deepscore_req(self.polarity)

        if self.queries is None:
            raise RuntimeError(
                "'AnnotationManager/Ms2deepscoreAnnotator': no query spectra found. "
                "Did you run "
                "'prepare_queries()'? - SKIP "
            )

        file = urlparse(DefaultPaths().url_ms2deepscore_pos).path.split("/")[-1]
        model = load_model(DefaultPaths().dirpath_ms2deepscore_pos.joinpath(file))

        sim_algorithm = MS2DeepScore(model=model, progress_bar=False)

        if self.max_time == 0:
            logger.info(
                "'AnnotationManager/Ms2deepscoreAnnotator': Started ms2deepscore "
                "library matching "
                "algorithm with no timeout set."
            )
            self.scores = matchms.calculate_scores(
                references=self.library,
                queries=self.queries,
                similarity_function=sim_algorithm,
            )
        else:
            try:
                logger.info(
                    f"'AnnotationManager/Ms2deepscoreAnnotator': Started ms2deepscore library matching"
                    f" algorithm with a timeout of '{self.max_time}' seconds."
                )
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
                logger.warning(
                    f"'AnnotationManager/Ms2deepscoreAnnotator': timeout of "
                    f"MS2dDeepScore-based "
                    f"calculation: more than specified '{self.max_time}' seconds."
                    f"For unlimited runtime, set 'maximum_runtime' to 0 - SKIP"
                )
                raise e

    def filter_match(self: Self, match: tuple, f_mz: float) -> bool:
        """Filter ms2deepscore-derived matches for user-specified params

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

    def extract_userlib_scores(self: Self):
        """Extract best matches against user library

        This method must only be called for extracting matches resulting from hits
        against a user-provided library.

        Raises:
            RuntimeError: 'self.scores' None - no scores calculated
        """
        if self.scores is None:
            raise RuntimeError(
                "'AnnotationManager/Ms2deepscoreAnnotator': 'self.scores' is None."
                "Did you run 'self.calculate_scores_ms2deepscore()'?"
            )

        for spectrum in self.queries:
            feature = self.features.get(int(spectrum.metadata.get("id")))

            sorted_matches = self.scores.scores_by_query(
                spectrum, name="MS2DeepScore", sort=True
            )
            for match in sorted_matches:
                if self.filter_match(match, feature.mz):
                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.matches is None:
                        feature.Annotations.matches = []

                    feature.Annotations.matches.append(
                        Match(
                            id=match[0].metadata.get("compound_name"),
                            library=self.library_name,
                            algorithm="ms2deepscore",
                            score=float(match[1].round(2)),
                            mz=match[0].metadata.get("precursor_mz"),
                            diff_mz=round(
                                abs(match[0].metadata.get("precursor_mz") - feature.mz),
                                4,
                            ),
                            module="user_library_annotation",
                            smiles=match[0].metadata.get("smiles") or "unknown",
                            inchikey=match[0].metadata.get("inchikey") or "unknown",
                        )
                    )

            self.features.modify(int(spectrum.metadata.get("id")), feature)

    def extract_mibig_scores(self: Self, kcb_results: dict):
        """Extract matches against targeted mibig library, incorporate KCB results

        Attributes:
            kcb_results: A dict containing the knownclusterblast results

        Raises:
            RuntimeError: 'self.scores' None - no scores calculated
        """
        if self.scores is None:
            raise RuntimeError(
                "'AnnotationManager/Ms2deepscoreAnnotator': 'self.scores' is None."
                "Did you run 'self.calculate_scores_ms2deepscore()'?"
            )

        for spectrum in self.queries:
            feature = self.features.get(int(spectrum.metadata.get("id")))

            sorted_matches = self.scores.scores_by_query(
                spectrum, name="MS2DeepScore", sort=True
            )
            for match in sorted_matches:
                if self.filter_match(match, feature.mz):
                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.matches is None:
                        feature.Annotations.matches = []

                    mibig_id_list = match[0].metadata.get("mibigaccession").split(",")

                    similarity = ""
                    region = ""
                    mibig_id = ""
                    for id in mibig_id_list:
                        if id in kcb_results:
                            similarity = kcb_results[id].get("bgc_sim")
                            region = kcb_results[id].get("region")
                            mibig_id = id

                    feature.Annotations.matches.append(
                        Match(
                            id=(
                                f'{match[0].metadata.get("id")}|'
                                f"{mibig_id}|"
                                f"sim%:{similarity}|"
                                f"{region}"
                            ),
                            library=self.library_name,
                            algorithm="ms2deepscore",
                            score=float(match[1].round(2)),
                            mz=match[0].metadata.get("precursor_mz"),
                            diff_mz=round(
                                abs(match[0].metadata.get("precursor_mz") - feature.mz),
                                4,
                            ),
                            module="antismash_kcb_annotation",
                            smiles=match[0].metadata.get("smiles") or "unknown",
                            inchikey=match[0].metadata.get("inchikey") or "unknown",
                        )
                    )

            self.features.modify(int(spectrum.metadata.get("id")), feature)
