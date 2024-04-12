"""Direct the creation of an instance of a sample-specific feature

These features are created with sample-specific information (e.g. retention time,
which can be different in each sample). This is different to generalized features,
which contain average values across samples.

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

from fermo_core.data_processing.builder_feature.class_feature_builder import (
    FeatureBuilder,
)
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature


class SpecificFeatureDirector:
    """Directs the construction of the sample-specific Feature instance"""

    @staticmethod
    def construct_mzmine3(
        row: pd.Series, s_id: str, max_intensity: int, max_area: int
    ) -> Feature:
        """Construct the Feature product instance.

        Args:
            row: a pandas series containing feature information
            s_id: indicating the sample identifier
            max_intensity: the highest intensity of the molecular feature in sample
            max_area: the highest area of the molecular feature in sample

        Returns:
            An instance of the Feature class.
        """
        return (
            FeatureBuilder()
            .set_f_id(int(row["id"]))
            .set_mz(float(row["mz"]))
            .set_fwhm(float(row[f"datafile:{s_id}:fwhm"]))
            .set_intensity(int(row[f"datafile:{s_id}:intensity_range:max"]))
            .set_rt_start(float(row[f"datafile:{s_id}:rt_range:min"]))
            .set_rt_stop(float(row[f"datafile:{s_id}:rt_range:max"]))
            .set_rt(float(row[f"datafile:{s_id}:rt"]))
            .set_area(int(row[f"datafile:{s_id}:area"]))
            .set_rt_range()
            .set_rel_intensity(
                row[f"datafile:{s_id}:intensity_range:max"], max_intensity
            )
            .set_rel_area(row[f"datafile:{s_id}:area"], max_area)
            .get_result()
        )
