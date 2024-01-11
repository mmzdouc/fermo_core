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
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


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
        logging.info("'SimNetworksManager': started analysis steps.")

        modules = (
            (
                self.params.SpecSimNetworkCosineParameters.activate_module,
                self.run_modified_cosine_alg,
            ),
        )

        for module in modules:
            if module[0]:
                module[1]()

        logging.info("'SimNetworksManager': completed analysis steps.")

    def run_modified_cosine_alg(self: Self):
        """Run modified cosine-based spectral similarity networking on features."""
        logging.info(
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
            logging.warning(
                f"'SimNetworksManager/ModCosineNetworker': timeout of modified "
                f"cosine spectral similarity network calculation. Calculation "
                f"took longer than "
                f"'{self.params.SpecSimNetworkCosineParameters.maximum_runtime}' "
                f"seconds. Increase the 'modified_cosine/maximum_runtime' parameter "
                f"or set it to 0 (zero) for unlimited runtime. Alternatively, "
                f"filter out low-intensity/area peaks with 'feature_filtering'."
            )
            return None

        # TODO(MMZ 09.01.24): mehthod 3: create network

        # TODO(MMZ 09.01.24): mehthod 4: post-process data so that it can be stored
        #  in the respective objects (in General Features and in Stats)

        logging.info(
            "'SimNetworksManager': completed modified cosine-based spectral similarity "
            "(=molecular) networking."
        )
