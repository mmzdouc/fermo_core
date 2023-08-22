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
from typing import Tuple, Any
from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
import logging


class FeatureBuilder:
    """Contains methods to build variants of features based on user input

    Some product attributes are set only downstream and are therefore not included here.
    """

    def __init__(self):
        self.feature = Feature()

    @staticmethod
    def type_testing(var: Any, kind: type):
        try:
            if not isinstance(var, kind):
                raise ValueError(
                    f"FeatureBuilder: Invalid type for '{var}'. Expected'{kind}', got "
                    f"'{type(var)}'."
                )
        except ValueError as e:
            logging.error(str(e))
            raise e

    def set_f_id(self, f_id: int):
        self.type_testing(f_id, int)
        self.feature.f_id = f_id
        return self

    def set_mz(self, mz: float):
        self.type_testing(mz, float)
        self.feature.mz = mz
        return self

    def set_rt(self, rt: float):
        self.type_testing(rt, float)
        self.feature.rt = rt
        return self

    def set_rt_start(self, rt_start: float):
        self.type_testing(rt_start, float)
        self.feature.rt_start = rt_start
        return self

    def set_rt_stop(self, rt_stop: float):
        self.type_testing(rt_stop, float)
        self.feature.rt_stop = rt_stop
        return self

    def set_rt_range(self, rt_range: float):
        self.type_testing(rt_range, float)
        self.feature.rt_range = rt_range
        return self

    def set_fwhm(self, fwhm: float):
        self.type_testing(fwhm, float)
        self.feature.fwhm = fwhm
        return self

    def set_intensity(self, intensity: int):
        self.type_testing(intensity, int)
        self.feature.intensity = intensity
        return self

    def set_rel_intensity(self, rel_intensity: float):
        self.type_testing(rel_intensity, float)
        self.feature.rel_intensity = rel_intensity
        return self

    def set_area(self, area: int):
        self.type_testing(area, int)
        self.feature.area = area
        return self

    def set_samples(self, samples: Tuple):
        self.type_testing(samples, tuple)
        self.feature.samples = samples
        return self

    def get_result(self):
        return self.feature
