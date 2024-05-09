"""Organize the calling of phenotype annotation modules.

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
from typing import Self, Tuple

from pydantic import BaseModel

from fermo_core.data_analysis.phenotype_manager.class_phen_quant_assigner import (
    PhenQuantAssigner,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager


logger = logging.getLogger("fermo_core")


class PhenotypeManager(BaseModel):
    """Pydantic-based class to organize calling and logging of phenotype annot modules

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

    def return_attrs(self: Self) -> Tuple[Stats, Repository]:
        """Returns modified attributes from PhenotypeManager to the calling function

        Returns:
            Tuple containing Stats, Feature Repository objects.
        """
        return self.stats, self.features

    def run_analysis(self: Self):
        """Organizes calling of phenotype annotation steps."""
        logger.info("'PhenotypeManager': started analysis steps.")

        match self.params.PhenotypeParameters.format:
            case "qualitative":
                self.run_assigner_qualitative()
            # TODO(8.5.): expand for other conditions
            case _:
                logger.warning("'PhenotypeManager': unexpected phenotype format - SKIP")
                return

        logger.info("'PhenotypeManager': completed analysis steps.")

    def run_assigner_qualitative(self: Self):
        """Run the phenotype feature annotation based on qualitative data"""
        logger.info("'PhenotypeManager': started qualitative phenotype data analysis.")

        if self.params.PhenoQuantAssgnParams.activate_module is False:
            logger.info(
                "'PhenotypeManager': parameters for "
                "'phenotype_assignment/qualitative' not specified or model turned off "
                " - SKIP"
            )
            return

        try:
            quant_assigner = PhenQuantAssigner(
                params=self.params,
                features=self.features,
                stats=self.stats,
                samples=self.samples,
            )
            quant_assigner.run_analysis()
            self.stats, self.features = quant_assigner.return_values()
        except Exception as e:
            logger.error(str(e))
            logger.error(
                "'PhenotypeManager': Error during running of PhenQuantAssigner - SKIP"
            )
            return

        logger.info(
            "'PhenotypeManager': completed qualitative phenotype data analysis."
        )
