"""Builder design pattern

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
from typing import Tuple
from fermo_core.data_processing.builder.dataclass_feature import Feature


class FeatureBuilder:
    """The Feature Builder.

    Some attributes are defined in later parts of the program.
    """

    def __init__(self):
        self.feature = Feature()

    def set_f_id(self, f_id: int):
        self.feature.f_id = f_id
        return self

    def set_mz(self, mz: float):
        self.feature.mz = mz
        return self

    def set_rt(self, rt: float):
        self.feature.rt = rt
        return self

    def set_rt_start(self, rt_start: float):
        self.feature.rt_start = rt_start
        return self

    def set_rt_stop(self, rt_stop: float):
        self.feature.rt_stop = rt_stop
        return self

    def set_rt_range(self, rt_range: float):
        self.feature.rt_range = rt_range
        return self

    def set_trace(self, trace: Tuple):
        self.feature.trace = trace
        return self

    def set_fwhm(self, fwhm: float):
        self.feature.fwhm = fwhm
        return self

    def set_intensity(self, intensity: int):
        self.feature.intensity = intensity
        return self

    def set_area(self, area: int):
        self.feature.area = area
        return self

    def set_msms(self, msms: Tuple):
        self.feature.msms = msms
        return self

    def set_samples(self, samples: Tuple):
        self.feature.samples = samples
        return self

    def get_result(self):
        return self.feature
