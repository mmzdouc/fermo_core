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
import networkx
from typing import Dict, Self, Optional

import matchms
import func_timeout

from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.core_module_parameter_managers import (
    SpecSimNetworkCosineParameters,
)

logger = logging.getLogger("fermo_core")


class ModCosineNetworker:
    """Class for calling and logging modified cosine spect. sim. networking"""

    @staticmethod
    def log_filtered_feature_no_msms(f_id: int):
        """Logs feature filtered from selection due to lack of MS/MS

        Arguments:
            f_id: feature identifier
        """
        logger.debug(
            f"'ModCosineNetworker': feature ID '{f_id}' filtered from spectral "
            f"similarity networking: has no associated MS/MS."
        )
        # TODO(MMZ 15.1.24): turn into clss of networksmanager

    @staticmethod
    def log_filtered_feature_nr_fragments(f_id: int, frags: int, min_frags: int):
        """Logs feature filtered from selection due to low number of MS/MS fragments

        Arguments:
            f_id: feature identifier
            frags: found nr of MS/MS fragments
            min_frags: minimal necessary nr or MS/MS fragments
        """
        logger.debug(
            f"'ModCosineNetworker': feature ID '{f_id}' filtered from spectral "
            f"similarity networking: min. nr. of MS/MS fragments lower than required "
            f"by parameter 'msms_min_frag_nr' ('{frags}' < '{min_frags}')."
        )
        # TODO(MMZ 15.1.24): turn into clss of networksmanager

    def filter_input_spectra(
        self: Self,
        features: tuple,
        feature_repo: Repository,
        settings: SpecSimNetworkCosineParameters,
    ) -> Dict[str, set]:
        """Filter features for spectral similarity analysis based on given restrictions.

        Arguments:
            features: a tuple of feature IDs
            feature_repo: containing GeneralFeature objects with feature info
            settings: containing given filter parameters

        Returns:
            A dictionary containing included and excluded feature ints in sets.
        """
        # TODO(MMZ 15.1.24): turn into clss of networksmanager
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
        spectra = list()

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

    @staticmethod
    def format_network_for_storage(
        graph: networkx.Graph,
    ) -> Dict:
        """Process networkx Graph object, remove redundant clusters, extract info

        Arguments:
            graph: holding spectral similarity networking information

        Returns:
            dict of full network, subnetworks, dict of clusters and contained features

        Raises:
            RuntimeError: detected overlap between subclusters in terms of feature IDs

        Notes:
            Matchms introduces "stringified" feature IDs in network - need to be
            removed by `networkx.relabel_nodes`
        """
        mapping = {node: int(node) for node in graph.nodes}
        graph = networkx.relabel_nodes(graph, mapping)

        subnetworks = []
        for component in networkx.connected_components(graph):
            subnetworks.append(graph.subgraph(component).copy())

        clusters = dict()
        for i, subnetwork in enumerate(subnetworks):
            ids = set([int(node) for node in subnetwork.nodes])
            for cluster in clusters.values():
                if len(output := ids.intersection(cluster)) != 0:
                    raise RuntimeError(
                        f"'ModCosineNetworker': detected overlap between subclusters: "
                        f"cluster with ids '{ids}' and cluster with ids '{cluster}' "
                        f"share ids '{output}'. This is unexpected - ABORT."
                    )
            clusters[i] = ids
            subnetworks[i].graph["name"] = i

        return {"network": graph, "subnetworks": subnetworks, "summary": clusters}
