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
from typing import Optional, Dict, Union

from pydantic import BaseModel


class Phenotype(BaseModel):
    """Pydantic-based class to organize phenotype/bioactivity info of Sample object

    Attributes:
        value: the measured original value for the sample in an experiment
        conc: the concentration of the sample (if all samples were measured
            at the same concentration, this is 1)
    """

    value: Union[int, float]
    conc: Union[int, float]


class Sample(BaseModel):
    """Organize sample-specific data, including sample-specific mol feature info.

    Attributes:
        s_id: string identifier of sample
        features: dict of features detected in sample; contain sample-specific data
        feature_ids: tuple of feature ids
        groups: group association of sample (if provided, else default group DEFAULT)
        cliques: number of cliques in this sample
        max_intensity: the highest intensity of a feature in the sample (absolute)
        phenotypes: indicates the conditions in which the sample showed activity. A
            dict of condition : Phenotype() pairs.
    """

    s_id: Optional[str] = None
    features: Optional[dict] = None
    feature_ids: Optional[tuple] = None
    groups: Optional[set[str]] = {"DEFAULT"}
    cliques: Optional[dict] = None
    max_intensity: Optional[int] = None
    phenotypes: Optional[Dict[str, Phenotype]] = None
