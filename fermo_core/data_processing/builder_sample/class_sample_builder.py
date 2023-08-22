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
from typing import Any
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


class SampleBuilder:
    """Contains methods to build variants of samples based on user input.

    In set_feature, a new Feature object is added to the feature_dict attribute,
    created by the SpecificFeatureDirector
    """

    def __init__(self):
        self.sample = Sample()

    @staticmethod
    def type_testing(var: Any, kind: type):
        try:
            if not isinstance(var, kind):
                raise ValueError(
                    f"SampleBuilder: Invalid type for '{var}'. Expected'{kind}', got "
                    f"'{type(var)}'."
                )
        except ValueError as e:
            logging.error(str(e))
            raise e

    def set_s_id(self, s_id: str):
        self.type_testing(s_id, str)
        self.sample.s_id = s_id
        return self

    def set_features(self):
        self.sample.features = dict()
        return self

    def set_max_intensity(self, max_intensity: int):
        self.type_testing(max_intensity, int)
        self.sample.max_intensity = max_intensity
        return self

    def get_result(self):
        return self.sample
