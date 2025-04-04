"""Runs the ms2query library annotation module.

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
from pathlib import Path
from typing import Self

import pandas as pd
from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Annotations,
    Match,
)
from fermo_core.data_processing.class_repository import Repository
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class MS2QueryAnnotator(BaseModel):
    """Pydantic-based class to organize calling and logging of ms2query lib matching

    Attributes:
        features: Repository object, holds "General Feature" objects
        params: User-provided parameters
        active_features: a set of active features
        cutoff: a float between 0 and 1 indicating the minimum accepted score
    """

    features: Repository
    params: ParameterManager
    active_features: set
    cutoff: float

    def return_features(self: Self) -> Repository:
        """Return the modified Feature objects as Repository object

        Returns:
            A Repository object with modified Feature objects
        """
        return self.features

    def assign_feature_info(self: Self, results_path: str | Path):
        """Load ms2query results and add annotation to Feature objects

        Arguments:
            results_path: location of the ms2query results file
        """
        df = pd.read_csv(results_path)
        df.fillna("unknown", inplace=True)
        if "feature_id" in df.columns:
            df.rename(columns={"feature_id": "id"}, inplace=True)

        for _, row in df.iterrows():
            if int(row["id"]) not in self.active_features:
                logger.warning(
                    f"'AnnotationManager/MS2QueryAnnotator': in MS2Query results, "
                    f"feature with ID "
                    f"'{row['id']}' is not part of set of currently active features. "
                    f"This feature might have been filtered out due to fermo_core "
                    f"filter settings. Alternatively, the wrong MS2Query results file "
                    f"was provided - SKIP"
                )
                continue
            else:
                if float(row["ms2query_model_prediction"]) >= self.cutoff:
                    feature = self.features.get(int(row["id"]))

                    if feature.Annotations is None:
                        feature.Annotations = Annotations()
                    if feature.Annotations.matches is None:
                        feature.Annotations.matches = []

                    feature.Annotations.matches.append(
                        Match(
                            id=row["analog_compound_name"],
                            library="ms2query",
                            algorithm="ms2query",
                            score=float(row["ms2query_model_prediction"]),
                            mz=float(row["precursor_mz_analog"]),
                            diff_mz=float(row["precursor_mz_difference"]),
                            module="ms2query_annotation",
                            smiles=str(row["smiles"]),
                            inchikey=str(row["inchikey"]),
                            npc_class=str(row["npc_class_results"]),
                        )
                    )
                    self.features.modify(int(row["id"]), feature)
