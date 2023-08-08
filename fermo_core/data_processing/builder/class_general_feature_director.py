"""Direct the creation of a dict of generalized features


TODO(MMZ): Improve description of class


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
from pathlib import Path
from typing import Dict
from fermo_core.data_processing.builder.class_feature_builder import FeatureBuilder


class GeneralFeatureDirector:
    """Builds the general feature instances"""

    @staticmethod
    def construct_mzmine(peaktable: Path) -> Dict:
        """Constructs the products and returns them in a dict.

        Args:
            peaktable: Path towards an mzmine3 peaktable

        Returns:
            A dict containing instances of the GeneralFeature class.
        """
        feature_dict = dict()

        df = pd.read_csv(peaktable)
        for i, row in df.iterrows():
            # TODO(MMZ): filter for features that were filtered out based on rel int?
            # TODO: if int(row["feature_ID"]) not in detected_features:
            feature_dict[row["id"]] = (
                FeatureBuilder()
                .set_f_id(row["id"])
                .set_intensity(row["height"])
                .set_area(row["area"])
                .set_mz(row["mz"])
                .set_rt(row["rt"])
                .set_rt_start(row["rt_range:min"])
                .set_rt_stop(row["rt_range:max"])
                .get_result()
            )

        return feature_dict
