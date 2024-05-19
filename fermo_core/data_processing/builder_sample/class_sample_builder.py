"""Builder for different instances of samples.

Samples act as "feature aggregators" and contain feature-specific information.

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
from typing import Self

import pandas as pd
from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.class_specific_feature_director import (
    SpecificFeatureDirector,
)
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample

logger = logging.getLogger("fermo_core")


class SampleBuilder(BaseModel):
    """Pydantic-based class to build variant of Sample objects based on user input.

    Order of calling method not
    """

    sample: Sample = Sample()

    def set_s_id(self: Self, s_id: str):
        """Set sample identifier.

        Args:
            s_id: a sample identifier string
        """
        self.sample.s_id = s_id
        return self

    def set_max_intensity_mzmine3(self: Self, s_id: str, df: pd.DataFrame):
        """Extract max feature intensity detected for sample s_id from DataFrame df

        Args:
            s_id: a sample identifier string
            df: a MZmine3 style peaktable as Pandas DataFrame
        """
        self.sample.max_intensity = int(
            df.loc[:, f"datafile:{s_id}:intensity_range:max"].max()
        )
        return self

    def set_max_area_mzmine3(self: Self, s_id: str, df: pd.DataFrame):
        """Extract max feature area detected for sample s_id from DataFrame df

        Args:
            s_id: a sample identifier string
            df: a MZmine3 style peaktable as Pandas DataFrame
        """
        self.sample.max_area = int(df.loc[:, f"datafile:{s_id}:area"].max())
        return self

    def set_features_mzmine3(self: Self, s_id: str, df: pd.DataFrame):
        """Extract features detected for sample s_id from DataFrame df

        Args:
            s_id: a sample identifier string
            df: a MZmine3 style peaktable as Pandas DataFrame

        Raises:
            ValueError: Required attributes self.sample.max_intensity or
            self.sample.max_area have not been set.
        """
        try:
            if self.sample.max_intensity is None or self.sample.max_area is None:
                raise ValueError(
                    "'SampleBuilder': self.set_features_mzmine3() called out of order. "
                    "'self.sample.max_intensity' and 'self.sample.max_area' must "
                    "not be 'None'."
                )
        except ValueError as e:
            logger.error(str(e))
            raise e

        self.sample.features = {}
        for _, row in df.iterrows():
            if row[f"datafile:{s_id}:feature_state"] == "DETECTED":
                self.sample.features[row["id"]] = (
                    SpecificFeatureDirector.construct_mzmine3(
                        row, s_id, self.sample.max_intensity, self.sample.max_area
                    )
                )
        return self

    def set_feature_ids(self: Self):
        """Sets feature IDs for convenient access.

        Raises:
            ValueError: Required attribute self.sample.features has not been set.
        """
        try:
            if self.sample.features is None:
                raise ValueError(
                    "'SampleBuilder': self.set_feature_ids() called out of order. "
                    "'self.sample.features' must not be 'None'."
                )
        except ValueError as e:
            logger.error(str(e))
            raise e

        self.sample.feature_ids = set(self.sample.features.keys())
        return self

    def get_result(self: Self):
        return self.sample
