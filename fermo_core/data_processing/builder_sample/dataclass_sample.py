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

import logging
from typing import Optional, Self

from pydantic import BaseModel

logger = logging.getLogger("fermo_core")


class Scores(BaseModel):
    """Organize sample-specific data, including sample-specific mol feature info.

    Attributes:
        diversity: indicates the est chemical diversity in this sample vs all samples
        specificity: indicates the unique chemistry compared to other samples
        mean_novelty: indicates the mean novelty of all features in sample
    """

    diversity: Optional[float] = None
    specificity: Optional[float] = None
    mean_novelty: Optional[float] = None

    def to_json(self: Self):
        return {
            "diversity": round(self.diversity, 2) if self.diversity is not None else 0,
            "specificity": (
                round(self.specificity, 2) if self.specificity is not None else 0
            ),
            "mean_novelty": (
                round(self.mean_novelty, 2) if self.mean_novelty is not None else 0
            ),
        }


class Sample(BaseModel):
    """Organize sample-specific data, including sample-specific mol feature info.

    Attributes:
        s_id: string identifier of sample
        features: dict of features objects with sample-specific information.
        feature_ids: set of feature ids included in sample
        networks: for each network algorithm, a set of subnetwork ids found in sample
        max_intensity: the highest intensity of a feature in the sample (absolute)
        max_area: the highest area of a feature in the sample (absolute)
        Scores: a Scores object summarizing scores calculated for sample
    """

    s_id: Optional[str] = None
    features: Optional[dict] = None
    feature_ids: Optional[set] = None
    networks: Optional[dict] = None
    max_intensity: Optional[int] = None
    max_area: Optional[int] = None
    Scores: Optional[Scores] = None

    def to_json(self: Self) -> dict:
        """Convert class attributes to json-compatible dict.

        Returns:
            A dictionary with class attributes as keys
        """
        attributes = (
            ("s_id", self.s_id, str),
            ("feature_ids", self.feature_ids, list),
            ("max_intensity", self.max_intensity, int),
            ("max_area", self.max_area, int),
        )

        json_dict = {}
        for attribute in attributes:
            if attribute[1] is not None:
                json_dict[attribute[0]] = attribute[2](attribute[1])

        json_dict["scores"] = self.Scores.to_json() if self.Scores is not None else {}

        json_dict["networks"] = (
            {key: list(val) for key, val in self.networks.items()}
            if self.networks is not None
            else {}
        )

        if self.feature_ids is not None:
            json_dict["sample_spec_features"] = {}
            for feature_id in self.feature_ids:
                json_dict["sample_spec_features"][feature_id] = self.features[
                    feature_id
                ].to_json()
        else:
            json_dict["sample_spec_features"] = {}

        return json_dict
