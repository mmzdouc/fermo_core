"""Direct the creation of an instance of a generalized molecular feature object.

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


class GeneralFeatureDirector:
    """Directs the construction of the Generalized Feature instance"""

    @staticmethod
    def construct_mzmine3(row: pd.Series) -> Feature:
        """Construct the Feature product instance.

        Args:
            row: a pandas series containing feature information

        Returns:
            An instance of the Feature class.
        """

        return (
            FeatureBuilder()
            .set_f_id(int(row["id"]))
            .set_area(int(row["area"]))
            .set_mz(float(row["mz"]))
            .set_rt(float(row["rt"]))
            .set_rt_start(float(row["rt_range:min"]))
            .set_rt_stop(float(row["rt_range:max"]))
            .set_samples(row)
            .set_area_per_sample(row)
            .set_height_per_sample(row)
            .get_result()
        )
