"""Direct the creation of an instance of the Sample object.

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

import pandas as pd
from typing import Tuple

from fermo_core.data_processing.builder.class_sample_builder import SampleBuilder
from fermo_core.data_processing.builder.dataclass_sample import Sample
from fermo_core.data_processing.builder.class_specific_feature_director import (
    SpecificFeatureDirector,
)


class SamplesDirector:
    """Directs the construction of the sample instance."""

    @staticmethod
    def construct_mzmine3(
        s_id: str,
        df: pd.DataFrame,
        features: Tuple,
    ) -> Sample:
        """Construct the Sample product instance.

        Args:
            s_id: the sample identifier
            df: a Pandas dataframe in mzmine3 format
            features: a tuple containing ids of detected features

        Returns:
            An instance of the Sample class.
        """
        sample = (
            SampleBuilder()
            .set_s_id(s_id)
            .set_features()
            .set_max_intensity(df.loc[:, f"datafile:{s_id}:intensity_range:max"].max())
            .get_result()
        )

        for _, row in df.iterrows():
            if row["id"] in features:
                if row[f"datafile:{s_id}:feature_state"] == "DETECTED":
                    sample.features[
                        row["id"]
                    ] = SpecificFeatureDirector.construct_mzmine3(
                        row, s_id, sample.max_intensity
                    )

        return sample
