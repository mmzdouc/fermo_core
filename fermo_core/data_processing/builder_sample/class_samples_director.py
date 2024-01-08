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

from fermo_core.data_processing.builder_sample.class_sample_builder import SampleBuilder
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


class SamplesDirector:
    """Directs the construction of the sample instance."""

    @staticmethod
    def construct_mzmine3(
        s_id: str,
        df: pd.DataFrame,
    ) -> Sample:
        """Construct the Sample product instance.

        Args:
            s_id: the sample identifier
            df: a Pandas dataframe in mzmine3 format

        Returns:
            An instance of the Sample class.
        """
        return (
            SampleBuilder()
            .set_s_id(str(s_id))
            .set_max_intensity_mzmine3(s_id, df)
            .set_max_area_mzmine3(s_id, df)
            .set_features_mzmine3(s_id, df)
            .set_feature_ids()
            .get_result()
        )
