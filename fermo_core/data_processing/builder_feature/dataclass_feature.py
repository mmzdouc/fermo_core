"""Organize molecular feature data. Product of Feature Builder class.

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

from typing import Optional, Tuple, Self, Dict, Set


class Feature:
    """Organize data belonging to a molecular feature.

    Product of the FeatureBuilder class.

    Attributes:
        f_id: the integer ID of the molecular feature.
        mz: the precursor mass to charge ratio (m/z).
        rt: the retention time at peak apex.
        rt_start: the start of the peak in minutes.
        rt_stop: the stop of the peak in minutes.
        rt_range: the length of a molecular feature peak in minutes.
        trace: indicating the reconstructed rt/intensity trace of the molecular feature.
        fwhm: the feature width at half maximum intensity (peak width).
        intensity: the maximum intensity.
        area: the area of the peak
        msms: a tuple of two tuples: [0] ms/ms fragments, [1] ms/ms intensities.
        samples: a tuple of samples to which feature is associated.
        blank: bool to indicate if feature is blank-associated (if provided).
        groups: association to groups if such metadata was provided.
        groups_fold: indicates the fold differences between groups if provided. Should
            be sorted from highest to lowest.
        phenotypes: dict of objects representing associated phenotype data
        annotations: dict of objects representing associated annotation data
        networks: dict of objects representing associated networking data
        scores: dict of objects representing associated scores
    """

    def __init__(self: Self):
        self.f_id: Optional[int] = None
        self.mz: Optional[float] = None
        self.rt: Optional[float] = None
        self.rt_start: Optional[float] = None
        self.rt_stop: Optional[float] = None
        self.rt_range: Optional[float] = None
        self.trace: Optional[Tuple] = None
        self.fwhm: Optional[float] = None
        self.intensity: Optional[int] = None
        self.rel_intensity: Optional[float] = None
        self.area: Optional[int] = None
        self.msms: Optional[Tuple[Tuple[float, ...], Tuple[float, ...]]] = None
        self.samples: Optional[Tuple] = None
        self.blank: Optional[bool] = None
        self.groups: Optional[Set] = None
        self.groups_fold: Optional[Dict] = None
        self.phenotypes: Optional[Dict] = None
        self.annotations: Optional[Dict] = None
        self.networks: Optional[Dict] = None
        self.scores: Optional[Dict] = None
