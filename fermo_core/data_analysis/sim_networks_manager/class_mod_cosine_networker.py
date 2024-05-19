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

import func_timeout
import matchms
import networkx

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)

logger = logging.getLogger("fermo_core")


class ModCosineNetworker:
    """Class for calling and logging modified cosine spect. sim. networking"""

    @staticmethod
    def spec_sim_networking(
        features: tuple,
        feature_repo: Repository,
        settings: SpecSimNetworkCosineParameters,
    ) -> matchms.Scores:
        """Calls modified cosine based spectral similarity networking.

        Arguments:
            features: a tuple of feature IDs to consider in networking
            feature_repo: containing GeneralFeature objects with feature info
            settings: containing given filter parameters

        Returns:
            A matchms Scores object

        Raises:
            func_timeout.FunctionTimedOut: function took longer than a user-specified
             number of seconds

        Notes:
            Timeout can be disabled by user by setting settings.maximum_runtime to 0.
        """
        spectra = []

        for f_id in features:
            feature = feature_repo.get(f_id)
            spectra.append(feature.Spectrum)

        sim_algorithm = matchms.similarity.ModifiedCosine(
            tolerance=settings.fragment_tol
        )

        if settings.maximum_runtime != 0:
            return func_timeout.func_timeout(
                timeout=settings.maximum_runtime,
                func=matchms.calculate_scores,
                kwargs={
                    "references": spectra,
                    "queries": spectra,
                    "similarity_function": sim_algorithm,
                    "is_symmetric": True,
                },
            )
        else:
            return matchms.calculate_scores(
                references=spectra,
                queries=spectra,
                similarity_function=sim_algorithm,
                is_symmetric=True,
            )

    @staticmethod
    def create_network(
        scores: matchms.Scores, settings: SpecSimNetworkCosineParameters
    ) -> networkx.Graph:
        """Process scores object and generate network

        Arguments:
            scores: holding spectral similarity scores information
            settings: parameter settings

        Returns:
            A networkx Graph object of the created network
        """
        network = matchms.networking.SimilarityNetwork(
            identifier_key="id",
            score_cutoff=settings.score_cutoff,
            max_links=settings.max_nr_links,
            top_n=settings.max_nr_links,
            link_method="mutual",
        )

        network.create_network(scores, "ModifiedCosine_score")

        return network.graph
