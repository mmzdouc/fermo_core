"""Organize data of sample-specific information.

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

from typing import Self, Dict, Optional


class Sample:
    """Collect sample-specific data

    TODO(MMZ): Expand the attributes

    Attributes:
        sample_id: identifier of sample
        features: dict of features associated to the sample (instances of SpecificFeature)
        groups: group association of sample (if provided)

        cliques: number of cliques in this sample
        phenotypes: indicates the sample is associated with

    """

    def __init__(self: Self, sample_id: str):
        self.sample_id: str = sample_id
        self.features: Optional[Dict] = None
        self.groups: Optional[Dict] = None
        self.cliques: Optional[Dict] = None
        self.phenotypes: Optional[Dict] = None
