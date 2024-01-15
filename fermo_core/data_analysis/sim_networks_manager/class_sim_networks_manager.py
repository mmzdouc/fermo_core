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
import func_timeout
from typing import Tuple, Self

from pydantic import BaseModel

from fermo_core.data_analysis.sim_networks_manager.class_mod_cosine_networker import (
    ModCosineNetworker,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats, SpecSimNet
from fermo_core.data_processing.builder_feature.dataclass_feature import SimNetworks
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class SimNetworksManager(BaseModel):
    """Pydantic-based class to organize calling and logging of networking modules

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

    def return_attrs(self: Self) -> Tuple[Stats, Repository, Repository]:
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
            # TODO(MMZ 15.1.24): Add a tuple to activate the Ms2deepscore module
        )

        for module in modules:
            if module[0]:
                module[1]()

        logger.info("'SimNetworksManager': completed analysis steps.")

    def run_modified_cosine_alg(self: Self):
        """Run modified cosine-based spectral similarity networking on features."""
        logger.info(
            "'SimNetworksManager': started modified cosine-based spectral similarity "
            "(=molecular) networking."
        )
        mod_cosine_networker = ModCosineNetworker()
        filtered_features = mod_cosine_networker.filter_input_spectra(
            tuple(self.stats.active_features),
            self.features,
            self.params.SpecSimNetworkCosineParameters,
        )

        try:
            scores = mod_cosine_networker.spec_sim_networking(
                tuple(filtered_features["included"]),
                self.features,
                self.params.SpecSimNetworkCosineParameters,
            )
        except func_timeout.FunctionTimedOut:
            logger.warning(
                f"'SimNetworksManager/ModCosineNetworker': timeout of modified "
                f"cosine spectral similarity network calculation. Calculation "
                f"took longer than "
                f"'{self.params.SpecSimNetworkCosineParameters.maximum_runtime}' "
                f"seconds. Increase the 'modified_cosine/maximum_runtime' parameter "
                f"or set it to 0 (zero) for unlimited runtime. Alternatively, "
                f"filter out low-intensity/area peaks with 'feature_filtering'."
            )
            return

        network = mod_cosine_networker.create_network(
            scores, self.params.SpecSimNetworkCosineParameters
        )

        try:
            network_data = mod_cosine_networker.format_network_for_storage(
                network,
            )
        except RuntimeError as e:
            logger.error(str(e))
            return

        self.store_network_data("modified_cosine", network_data, filtered_features)

        logger.info(
            "'SimNetworksManager': completed modified cosine-based spectral similarity "
            "(=molecular) networking."
        )

    # TODO(MMZ 15.1.24): add method to start the ms2deepscore networker class; must
    #  check if positive mode true, else skip with log message

    def store_network_data(
        self: Self, network_name: str, network_data: dict, filtered_features: dict
    ):
        """Store network data in storage objects for later use

        Arguments:
            network_name: name of networking algorithm
            network_data: dict of network, subnetworks, clusters
            filtered_features: dict features included and excluded from networking
        """
        if self.stats.networks is None:
            self.stats.networks = {}

        self.stats.networks[network_name] = SpecSimNet(
            algorithm=network_name,
            network=network_data["network"],
            subnetworks=network_data["subnetworks"],
            summary=network_data["summary"],
        )

        for f_id in filtered_features["included"]:
            feature = self.features.get(f_id)
            if feature.networks is None:
                feature.networks = {}

            for cluster_id in network_data["summary"]:
                if f_id in network_data["summary"][cluster_id]:
                    feature.networks[network_name] = SimNetworks(
                        algorithm=network_name, network_id=cluster_id
                    )

            self.features.modify(f_id, feature)
