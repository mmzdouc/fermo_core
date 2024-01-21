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
from typing import Optional, Tuple, Dict, Set, Self

from matchms import Spectrum
from pydantic import BaseModel


class SimNetworks(BaseModel):
    """A Pydantic-based class to represent spectral similarity network information

    Attributes:
        algorithm: name of algorithm
        network_id: an integer indicating the network feature is associated with
    """

    algorithm: str
    network_id: int


class Feature(BaseModel):
    """A Pydantic-based class to represent a molecular feature.

    Attributes:
        f_id: the integer ID of the molecular feature.
        mz: the precursor mass to charge ratio (m/z).
        rt: the retention time at peak apex.
        rt_start: the start of the peak in minutes.
        rt_stop: the stop of the peak in minutes.
        rt_range: the length of a molecular feature peak in minutes.
        trace_rt: the rt data points of the pseudo-chromatogram trace
        trace_int: the relative intensity data points of the pseudo-chromatogram trace
        fwhm: the feature width at half maximum intensity (peak width).
        intensity: the maximum intensity.
        rel_intensity: the intensity relative to the highest feature in the sample.
        area: the area of the peak
        rel_area: the area relative to the feature with the highest area in the sample.
        msms: a tuple of two tuples: [0] ms/ms fragments, [1] ms/ms intensities.
        Spectrum: a matchms Spectrum object instance using data from msms
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

    f_id: Optional[int] = None
    mz: Optional[float] = None
    rt: Optional[float] = None
    rt_start: Optional[float] = None
    rt_stop: Optional[float] = None
    rt_range: Optional[float] = None
    trace_rt: Optional[Tuple] = None
    trace_int: Optional[Tuple] = None
    fwhm: Optional[float] = None
    intensity: Optional[int] = None
    rel_intensity: Optional[float] = None
    area: Optional[int] = None
    rel_area: Optional[float] = None
    msms: Optional[Tuple[Tuple[float, ...], Tuple[float, ...]]] = None
    Spectrum: Optional[Spectrum] = None
    samples: Optional[Tuple] = None
    blank: Optional[bool] = None
    groups: Optional[Set] = None
    groups_fold: Optional[Dict] = None
    phenotypes: Optional[Dict] = None
    annotations: Optional[Dict] = None
    networks: Optional[Dict] = None
    scores: Optional[Dict] = None

    def to_json(self: Self) -> dict:
        """Convert class attributes to json-compatible dict.

        Returns:
            A dictionary with class attributes as keys
        """
        attributes = (
            ("f_id", self.f_id, int),
            ("mz", self.mz, float),
            ("rt", self.rt, float),
            ("rt_start", self.rt_start, float),
            ("rt_stop", self.rt_stop, float),
            ("rt_range", self.rt_range, float),
            ("trace_rt", self.trace_rt, list),
            ("trace_int", self.trace_int, list),
            ("fwhm", self.fwhm, float),
            ("intensity", self.intensity, int),
            ("rel_intensity", self.rel_intensity, float),
            ("area", self.area, int),
            ("rel_area", self.rel_area, float),
            ("samples", self.samples, list),
            ("blank", self.blank, bool),
            ("groups", self.groups, list),
        )

        json_dict = {}
        for attribute in attributes:
            if attribute[1] is not None:
                json_dict[attribute[0]] = attribute[2](attribute[1])

        if self.Spectrum is not None:
            json_dict["spectrum"] = dict()
            json_dict["spectrum"]["mz"] = list(self.Spectrum.mz)
            json_dict["spectrum"]["int"] = list(self.Spectrum.intensities)
            json_dict["spectrum"]["metadata"] = self.Spectrum.metadata

        if self.networks is not None:
            json_dict["networks"] = dict()
            for network in self.networks:
                json_dict["networks"][network] = {
                    "algorithm": str(self.networks[network].algorithm),
                    "network_id": int(self.networks[network].network_id),
                }

        # TODO(MMZ 20.1.24): implement assignment for complex attributes group_folds,
        #  annotations, phenotypes, scores

        return json_dict
