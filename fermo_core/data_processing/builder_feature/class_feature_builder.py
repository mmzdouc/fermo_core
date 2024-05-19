"""Builder for different instances of molecular features.

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

import pandas as pd
from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import (
    Feature,
    SampleInfo,
)

logger = logging.getLogger("fermo_core")


class FeatureBuilder(BaseModel):
    """Pydantic-based class to build variants of Feature objects based on user input."""

    feature: Feature = Feature()

    def set_f_id(self, f_id: int):
        """Set attribute

        Arguments:
            f_id: the molecular feature identifier
        """
        self.feature.f_id = f_id
        return self

    def set_mz(self, mz: float):
        """Set attribute

        Arguments:
            mz: the molecular feature mass/charge ratio
        """
        self.feature.mz = mz
        return self

    def set_rt(self, rt: float):
        """Set attribute

        Arguments:
            rt: the retention time of the peak apex
        """
        self.feature.rt = rt
        return self

    def set_rt_start(self, rt_start: float):
        """Set attribute

        Arguments:
            rt_start: the retention time at the start of the peak
        """
        self.feature.rt_start = rt_start
        return self

    def set_rt_stop(self, rt_stop: float):
        """Set attribute

        Arguments:
            rt_stop: the retention time at the end of the peak
        """
        self.feature.rt_stop = rt_stop
        return self

    def set_rt_range(self):
        """Calculate and set attribute for retention time range

        Raises:
            ValueError: method called out of order
        """
        if self.feature.rt_start is None or self.feature.rt_stop is None:
            raise ValueError(
                "'FeatureBuilder': self.set_rt_range() called out of order. "
                "'self.feature.rt_start' and 'self.feature.rt_stop' must "
                "not be 'None'."
            )

        self.feature.rt_range = round(
            float(self.feature.rt_stop - self.feature.rt_start), 2
        )
        return self

    def set_fwhm(self, fwhm: float):
        """Set attribute

        Arguments:
            fwhm: the feature with at half maximum intensity of the peak
        """
        self.feature.fwhm = fwhm
        return self

    def set_intensity(self, intensity: int):
        """Set attribute

        Arguments:
            intensity: the (absolute) intensity (=height) of the peak
        """
        self.feature.intensity = intensity
        return self

    def set_rel_intensity(self, intensity: int, max_intensity: int):
        """Calculate and set attribute for relative intensity

        Arguments:
            intensity: height of feature
            max_intensity: height of most intense feature per sample
        """
        self.feature.rel_intensity = round((intensity / max_intensity), 2)
        return self

    def set_area(self, area: int):
        """Set attribute

        Arguments:
            area: the (absolute) area under the curve of the molecular feature
        """
        self.feature.area = area
        return self

    def set_rel_area(self, area: int, max_area: int):
        """Calculate and set attribute for relative area

        Arguments:
            area: the area under the curve (AUC) of the feature
            max_area: AUC of the feature with the highest area per sample
        """
        self.feature.rel_area = round((area / max_area), 2)
        return self

    def set_samples(self, row: pd.Series):
        """Extract and set sample ids

        Arguments:
            row: a pandas Series to extract IDs of samples in which feature was detected
        """
        samples = []
        for sample in row.filter(regex=":feature_state").index:
            sample_id = sample.split(":")[1]
            if row[f"datafile:{sample_id}:feature_state"] == "DETECTED":
                samples.append(sample_id)

        self.feature.samples = set(samples)
        return self

    def set_area_per_sample(self, row: pd.Series):
        """Extract and set area per sample

        Arguments:
            row: a pandas Series to extract sample IDs and areas from

        Raises:
            ValueError: method called out of order
        """
        if self.feature.samples is None:
            raise ValueError(
                "'FeatureBuilder': self.set_area_per_sample() called out of order. "
                "'self.feature.samples' must not be 'None'."
            )

        area_per_sample = []
        for s_id in self.feature.samples:
            area_per_sample.append(
                SampleInfo(s_id=s_id, value=row[f"datafile:{s_id}:area"])
            )
        area_per_sample = sorted(area_per_sample, key=lambda x: x.value, reverse=True)
        self.feature.area_per_sample = area_per_sample
        return self

    def set_height_per_sample(self, row: pd.Series):
        """Extract and set max height per sample

        Arguments:
            row: a pandas Series to extract sample IDs and max height from

        Raises:
            ValueError: method called out of order
        """
        if self.feature.samples is None:
            raise ValueError(
                "'FeatureBuilder': self.set_height_per_sample() called out of order. "
                "'self.feature.samples' must not be 'None'."
            )

        height_per_sample = []
        for s_id in self.feature.samples:
            height_per_sample.append(
                SampleInfo(s_id=s_id, value=row[f"datafile:{s_id}:intensity_range:max"])
            )
        height_per_sample = sorted(
            height_per_sample, key=lambda x: x.value, reverse=True
        )
        self.feature.height_per_sample = height_per_sample
        return self

    def get_result(self):
        """Return object instance.

        Returns:
            The modified object instance.
        """
        return self.feature
