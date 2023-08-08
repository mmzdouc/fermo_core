"""Storage and handling of general stats of analysis run

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

from typing import Self, Tuple, Optional


class Stats:
    """Organize stats regarding overall analysis run

    TODO(MMZ): Improve description of class

    Attributes:
        rt_min: overall lowest retention time start across all samples, in minutes
        rt_max: overall highest retention time stop across all samples, in minutes
        rt_range: range in minutes between lowest start and highest stop.
        samples: all sample ids in analysis run
        features: all feature ids in analysis run
        groups: all group ids in analysis run
        cliques: all similarity cliques in analysis run
        phenotypes: all phenotype classifications in analysis run
        blank: all blank-associated features in analysis run
        int_removed: all features that were removed due to intensity range
        annot_removed: all features that were removed due to annotation range
    """

    def __init__(
        self: Self,
        rt_min: float,
        rt_max: float,
        rt_range: float,
    ):
        self.rt_min: float = rt_min
        self.rt_max: float = rt_max
        self.rt_range: float = rt_range
        self.samples: Optional[Tuple] = None
        self.features: Optional[Tuple] = None
        self.groups: Optional[Tuple] = None
        self.cliques: Optional[Tuple] = None
        self.phenotypes: Optional[Tuple] = None
        self.blank: Optional[Tuple] = None
        self.int_removed: Optional[Tuple] = None
        self.annot_removed: Optional[Tuple] = None
