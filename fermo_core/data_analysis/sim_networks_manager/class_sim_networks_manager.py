"""Organize the calling of (spectral) similarity networking modules.

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
import urllib.error
from typing import Self

import func_timeout
import networkx
from pydantic import BaseModel

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)
from fermo_core.data_analysis.sim_networks_manager.class_ms2deepscore_networker import (
    Ms2deepscoreNetworker,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import SimNetworks
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import SpecSimNet, Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.utils.utility_method_manager import UtilityMethodManager

logger = logging.getLogger("fermo_core")


class SimNetworksManager(BaseModel):
    """Pydantic-based class to organize calling and logging of networking modules

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects

    Notes:
        `UtilityMethodManager` baseclass gives additional utility methods.
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository

    @staticmethod
    def log_filtered_feature_no_msms(f_id: int):
        """Logs feature filtered from selection due to lack of MS/MS

        Arguments:
            f_id: feature identifier
        """
        logger.debug(
            f"'SimNetworksManager': feature ID '{f_id}' filtered from spectral "
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
        logger.debug(
            f"'SimNetworksManager': feature ID '{f_id}' filtered from spectral "
            f"similarity networking: min. nr. of MS/MS fragments lower than required "
            f"by parameter 'msms_min_frag_nr' ('{frags}' < '{min_frags}')."
        )

    @staticmethod
    def log_timeout_mod_cosine(max_time: str):
        """Logs timeout due to long-running modified cosine network calculation

        Arguments:
            max_time: the set maximum calculation time
        """
        logger.warning(
            f"'SimNetworksManager/ModCosineNetworker': timeout of modified "
            f"cosine spectral similarity network calculation. Calculation "
            f"took longer than '{max_time}' seconds. Increase the "
            f"'spec_sim_networking/modified_cosine/maximum_runtime' parameter "
            f"or set it to 0 (zero) for unlimited runtime. Alternatively, "
            f"filter out low-intensity/area peaks with 'feature_filtering' - SKIP."
        )

    @staticmethod
    def log_timeout_ms2deepscore(max_time: str):
        """Logs timeout due to long-running ms2deepscore network calculation

        Arguments:
            max_time: the set maximum calculation time
        """
        logger.warning(
            f"'SimNetworksManager/Ms2deepscoreNetworker': timeout of "
            f"ms2deepscore similarity network calculation. Calculation "
            f"took longer than '{max_time}' seconds. Increase the "
            f"'spec_sim_networking/ms2deepscore/maximum_runtime' parameter "
            f"or set it to 0 (zero) for unlimited runtime. Alternatively, "
            f"filter out low-intensity/area peaks with 'feature_filtering' - SKIP"
        )

    def return_attrs(self: Self) -> tuple[Stats, Repository, Repository]:
        """Returns modified attributes from SimNetworksManager to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""
        logger.info("'SimNetworksManager': started analysis steps.")

        modules = (
            (
                self.params.SpecSimNetworkCosineParameters.activate_module,
                self.run_modified_cosine_alg,
            ),
            (
                self.params.SpecSimNetworkDeepscoreParameters.activate_module,
                self.run_ms2deepscore_alg,
            ),
        )

        for module in modules:
            if module[0]:
                module[1]()

        logger.info("'SimNetworksManager': completed analysis steps.")

    def run_modified_cosine_alg(self: Self):
        """Run modified cosine-based spectral similarity networking on features."""
        logger.info("'SimNetworksManager/ModCosineNetworker': started calculation")

        filtered_features = self.filter_input_spectra(
            tuple(self.stats.active_features),
            self.features,
            self.params.SpecSimNetworkCosineParameters.msms_min_frag_nr,
        )

        try:
            mod_cosine_networker = ModCosineNetworker()
            scores = mod_cosine_networker.spec_sim_networking(
                tuple(filtered_features["included"]),
                self.features,
                self.params.SpecSimNetworkCosineParameters,
            )
        except func_timeout.FunctionTimedOut:
            self.log_timeout_mod_cosine(
                str(self.params.SpecSimNetworkCosineParameters.maximum_runtime)
            )
            return

        network = mod_cosine_networker.create_network(
            scores, self.params.SpecSimNetworkCosineParameters
        )

        try:
            network_data = self.format_network_for_storage(network)
        except RuntimeError as e:
            logger.error(str(e))
            return

        self.store_network_data(
            "modified_cosine", network_data, tuple(filtered_features.get("included"))
        )

        logger.info("'SimNetworksManager/ModCosineNetworker': completed calculation")

    def run_ms2deepscore_alg(self: Self):
        """Run ms2deepscore-based spectral similarity networking on features."""
        logger.info("'SimNetworksManager/Ms2deepscoreNetworker': started calculation.")

        try:
            UtilityMethodManager().check_ms2deepscore_req(
                self.params.PeaktableParameters.polarity
            )
        except urllib.error.URLError:
            return
        except RuntimeError:
            return

        filtered_features = self.filter_input_spectra(
            tuple(self.stats.active_features),
            self.features,
            self.params.SpecSimNetworkDeepscoreParameters.msms_min_frag_nr,
        )

        try:
            ms2deepscore_networker = Ms2deepscoreNetworker()
            scores = ms2deepscore_networker.spec_sim_networking(
                tuple(filtered_features["included"]),
                self.features,
                self.params.SpecSimNetworkDeepscoreParameters,
            )
        except func_timeout.FunctionTimedOut:
            self.log_timeout_ms2deepscore(
                str(self.params.SpecSimNetworkDeepscoreParameters.maximum_runtime)
            )
            return
        except FileNotFoundError:
            logger.warning(
                "'SimNetworksManager/Ms2deepscoreNetworker': no embedding file - SKIP"
            )
            return

        network = ms2deepscore_networker.create_network(
            scores, self.params.SpecSimNetworkDeepscoreParameters
        )

        try:
            network_data = self.format_network_for_storage(
                network,
            )
        except RuntimeError as e:
            logger.error(str(e))
            return

        self.store_network_data(
            "ms2deepscore", network_data, tuple(filtered_features.get("included"))
        )

        logger.info("'SimNetworksManager/Ms2deepscoreNetworker': completed calculation")

    def filter_input_spectra(
        self: Self,
        features: tuple,
        feature_repo: Repository,
        msms_min_frag_nr: int,
    ) -> dict[str, set]:
        """Filter features for spectral similarity analysis based on given restrictions.

        Arguments:
            features: a tuple of feature IDs
            feature_repo: containing GeneralFeature objects with feature info
            msms_min_frag_nr: minimum number of fragments per spectrum to be considered

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
            elif len(feature.Spectrum.peaks.mz) < msms_min_frag_nr:
                excluded.add(f_id)
                self.log_filtered_feature_nr_fragments(
                    f_id, len(feature.Spectrum.peaks.mz), msms_min_frag_nr
                )
            else:
                included.add(f_id)

        return {"included": included, "excluded": excluded}

    @staticmethod
    def format_network_for_storage(
        graph: networkx.Graph,
    ) -> dict:
        """Process networkx Graph object, remove redundant clusters, extract info

        Arguments:
            graph: holding spectral similarity networking information

        Returns:
            dict of full network, subnetworks, dict of clusters/contained features

        Raises:
            RuntimeError: detected overlap between subclusters in terms of feature IDs

        Notes:
            Matchms introduces "stringified" feature IDs in network - need to be
            removed by `networkx.relabel_nodes`
        """
        mapping = {node: int(node) for node in graph.nodes}
        graph = networkx.relabel_nodes(graph, mapping)

        subnetworks = {}
        for i, component in enumerate(networkx.connected_components(graph)):
            subnetworks[i] = graph.subgraph(component).copy()
            subnetworks[i].graph["name"] = i

        clusters = {}
        for sub in subnetworks:
            ids = {int(node) for node in subnetworks[sub].nodes}
            for cluster in clusters.values():
                if len(output := ids.intersection(cluster)) != 0:
                    raise RuntimeError(
                        f"'SimNetworksManager': detected overlap between subclusters: "
                        f"cluster with ids '{ids}' and cluster with ids '{cluster}' "
                        f"share ids '{output}'. This is unexpected - ABORT."
                    )
            clusters[sub] = ids

        return {"network": graph, "subnetworks": subnetworks, "summary": clusters}

    def store_network_data(
        self: Self, network_name: str, network_data: dict, features: tuple
    ):
        """Store network data in storage objects for later use

        Arguments:
            network_name: name of networking algorithm
            network_data: dict of network, subnetworks, summary
            features: tuple of features included in networking
        """
        if self.stats.networks is None:
            self.stats.networks = {}

        self.stats.networks[network_name] = SpecSimNet(
            algorithm=network_name,
            network=network_data["network"],
            subnetworks=network_data["subnetworks"],
            summary=network_data["summary"],
        )

        for f_id in features:
            feature = self.features.get(f_id)
            if feature.networks is None:
                feature.networks = {}

            for cluster_id in network_data["summary"]:
                if f_id in network_data["summary"][cluster_id]:
                    feature.networks[network_name] = SimNetworks(
                        algorithm=network_name, network_id=cluster_id
                    )

            self.features.modify(f_id, feature)
