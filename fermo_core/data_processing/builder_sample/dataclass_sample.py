"""Organize data of sample-specific information.

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

from typing import Self, Optional


class Sample:
    """Organize sample-specific data, including sample-specific mol feature info.

    Attributes:
        s_id: identifier of sample
        features: dict of features detected in sample; contain sample-specific data
        groups: group association of sample (if provided)
        cliques: number of cliques in this sample
        phenotypes: indicates the phenotype the sample is associated with
        max_intensity: the highest intensity of a feature in the sample (absolute)
    """

    def __init__(self: Self):
        self.s_id: Optional[str] = None
        self.features: Optional[dict] = None
        self.groups: Optional[dict] = None
        self.cliques: Optional[dict] = None
        self.phenotypes: Optional[dict] = None
        self.max_intensity: Optional[dict] = None

        # TODO(MMZ): Add further parameters if necessary
