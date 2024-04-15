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
from typing import Optional, Tuple, Dict, Set, Self, List, Any, Type

from pydantic import BaseModel


class Adduct(BaseModel):
    """A Pydantic-based class to represent adduct annotation information

    Attributes:
        adduct_type: describes type of adduct
        partner_adduct: adduct of partner feature
        partner_id: partner feature id based on which the adduct was found
        partner_mz: partner feature mz
        diff_ppm: the difference in ppm between the two features
        sample: the sample identifier
    """

    adduct_type: str
    partner_adduct: str
    partner_id: int
    partner_mz: float
    diff_ppm: float
    sample: str


class Match(BaseModel):
    """A Pydantic-based class to represent library matching information

    Attributes:
        id: identifier of matched molecule
        library: name of library file matched molecule is from
        algorithm: algorithm used for matching
        score: score that led to a matching between feature and matched molecule
        mz: m/z ratio of matched molecule
        diff_mz: difference between m/z ratios of feature and matched molecule
        module: responsible for matching operation
    """

    id: Any
    library: str
    algorithm: str
    score: float
    mz: float
    diff_mz: float
    module: str


class NeutralLoss(BaseModel):
    """A Pydantic-based class to represent detected neutral losses in MS2 spectrum

    Attributes:
        id: neutral loss identifier
        mz_det: detected m/z
        mz_ex: expected m/z
        diff: difference in ppm
    """

    id: str
    mz_det: float
    mz_ex: float
    diff: float


class Peptide(BaseModel):
    """A Pydantic-based class to represent peptide-specific information

    Attributes:
        chem_class: the peptide class identifier
        aa_tags: detected amino acids, derived from neutral losses, one-letter AA code
        evidence: a list of evidences pointing toward the class
    """

    chem_class: str = "peptidic"
    aa_tags: List = []
    evidence: List = []


class Annotations(BaseModel):
    """A Pydantic-based class to represent annotation information

    Attributes:
        adducts: list of Adduct objects representing putative adducts of this feature
        matches: list of Match objects repr. putative library matching hits
        classes: list of objects to annotate putative chemical classes of feature
        losses: list of NeutralLoss objects annotating functional groups of feature
    """

    adducts: Optional[List[Adduct]] = None
    matches: Optional[List[Match]] = None
    classes: Optional[List[Type]] = None
    losses: Optional[List[NeutralLoss]] = None


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
        Spectrum: a matchms Spectrum object instance using data from msms
        samples: a tuple of samples to which feature is associated.
        blank: bool to indicate if feature is blank-associated (if provided).
        groups: association to groups if such metadata was provided.
        groups_fold: indicates the fold differences between groups if provided. Should
            be sorted from highest to lowest.
        phenotypes: dict of objects representing associated phenotype data
        Annotations: objects summarizing associated annotation data
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
    Spectrum: Optional[Any] = None
    samples: Optional[Tuple] = None
    blank: Optional[bool] = None
    groups: Optional[Set] = None
    groups_fold: Optional[Dict] = None
    phenotypes: Optional[Dict] = None
    Annotations: Optional[Annotations] = None
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
            json_dict["spectrum"]["int"] = [
                round(i, 3) for i in self.Spectrum.intensities
            ]
            json_dict["spectrum"]["metadata"] = self.Spectrum.metadata

        if self.networks is not None:
            json_dict["networks"] = dict()
            for network in self.networks:
                json_dict["networks"][network] = {
                    "algorithm": str(self.networks[network].algorithm),
                    "network_id": int(self.networks[network].network_id),
                }

        if self.Annotations is not None:
            json_dict["annotations"] = dict()

            if self.Annotations.adducts is not None:
                json_dict["annotations"]["adducts"] = []
                for adduct in self.Annotations.adducts:
                    json_dict["annotations"]["adducts"].append(
                        {
                            "adduct_type": adduct.adduct_type,
                            "partner_adduct": adduct.partner_adduct,
                            "partner_id": adduct.partner_id,
                            "partner_mz": adduct.partner_mz,
                            "diff_ppm": adduct.diff_ppm,
                            "sample": adduct.sample,
                        }
                    )
            if self.Annotations.matches is not None:
                json_dict["annotations"]["matches"] = []
                for match in self.Annotations.matches:
                    json_dict["annotations"]["matches"].append(
                        {
                            "id": match.id,
                            "library": match.library,
                            "algorithm": match.algorithm,
                            "score": match.score,
                            "mz": match.mz,
                            "diff_mz": match.diff_mz,
                            "module": match.module,
                        }
                    )

            if self.Annotations.losses is not None:
                json_dict["annotations"]["losses"] = []
                for loss in self.Annotations.losses:
                    json_dict["annotations"]["losses"].append(
                        {
                            "id": loss.id,
                            "mz_det": loss.mz_det,
                            "mz_ed": loss.mz_ex,
                            "diff": loss.diff,
                        }
                    )

            if self.Annotations.classes is not None:
                json_dict["annotations"]["classes"] = []
                for cla in self.Annotations.classes:
                    if isinstance(cla, Peptide):
                        json_dict["annotations"]["classes"].append(
                            {
                                "chem_class": cla.chem_class,
                                "aa_tags": sorted(cla.aa_tags, reverse=False),
                                "evidence": sorted(cla.evidence, reverse=False),
                            }
                        )

        # TODO(MMZ 20.1.24): implement assignment for complex attributes group_folds,
        #  annotations, phenotypes, scores

        return json_dict
