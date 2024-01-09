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
from typing import Tuple, Self, Optional

from matchms import Spectrum
from pydantic import BaseModel

from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats


class SimNetworksManager(BaseModel):
    """Pydantic-based class to organize calling and logging of networking modules

    Attributes:
        params: ParameterManager object, holds user-provided parameters
        stats: Stats object, holds stats on molecular features and samples
        features: Repository object, holds "General Feature" objects
        samples: Repository object, holds "Sample" objects
        spectra: list ot matchms Spectrum objects for matching operations
    """

    params: ParameterManager
    stats: Stats
    features: Repository
    samples: Repository
    spectra: Optional[list] = None

    # TODO(MMZ 9.1.24): remove wrong to-dos; Spectrum object part of GeneralFeature
    #  object

    def return_attributes(self: Self) -> Tuple[Stats, Repository, Repository]:
        """Returns modified attributes from SimNetworksManager to the calling function

        Returns:
            Tuple containing Stats, Feature Repository and Sample Repository objects.
        """
        return self.stats, self.features, self.samples

    def run_analysis(self: Self):
        """Organizes calling of data analysis steps."""
        logging.info("'SimNetworksManager': started analysis steps.")

        modules = (
            self.params.SpecSimNetworkCosineParameters.activate_module,
            self.run_modified_cosine_alg,
        )

        for module in modules:
            if module[0] is not None:
                module[1]()

        logging.info("'SimNetworksManager': completed analysis steps.")

    def run_modified_cosine_alg(self: Self):
        """Run modified cosine-based spectral similarity networking on features."""
        logging.info(
            "'SimNetworksManager': started modified cosine-based spectral similarity "
            "(=molecular) networking."
        )

        # TODO(MMZ 09.01.24): call static methods from ModCosineNetworker,

        logging.info(
            "'SimNetworksManager': completed modified cosine-based spectral similarity "
            "(=molecular) networking."
        )
