"""Organizes several classes that hold and validate core module parameter.

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

from typing import Self

from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator

from fermo_core.input_output.class_validation_manager import ValidationManager


class AdductAnnotationParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of adduct annotation parameters.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        mass_dev_ppm: The estimated maximum mass deviation in ppm.

    Raise:
        ValueError: Mass deviation unreasonably high.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    mass_dev_ppm: PositiveFloat = 10.0

    @model_validator(mode="after")
    def validate_adduct_annotation_parameters(self):
        ppm = self.mass_dev_ppm
        ValidationManager.validate_mass_deviation_ppm(ppm)
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "mass_dev_ppm": float(self.mass_dev_ppm),
            }
        else:
            return {"activate_module": self.activate_module}


class NeutralLossParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of neutral loss annotation params.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        mass_dev_ppm: The estimated maximum mass deviation in ppm.
        nonbiological: Switch on comparison against losses in 'generic_other_pos.csv'

    Raise:
        ValueError: Mass deviation unreasonably high.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    mass_dev_ppm: PositiveFloat = 10.0
    nonbiological: bool = False

    @model_validator(mode="after")
    def validate_adduct_annotation_parameters(self):
        ppm = self.mass_dev_ppm
        ValidationManager.validate_mass_deviation_ppm(ppm)
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "mass_dev_ppm": float(self.mass_dev_ppm),
                "nonbiological": self.nonbiological,
            }
        else:
            return {"activate_module": self.activate_module}


class FragmentAnnParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of fragment annotation params.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        mass_dev_ppm: The estimated maximum mass deviation in ppm.

    Raise:
        ValueError: Mass deviation unreasonably high.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    mass_dev_ppm: PositiveFloat = 10.0

    @model_validator(mode="after")
    def validate_fragment_annotation_parameters(self):
        ppm = self.mass_dev_ppm
        ValidationManager.validate_mass_deviation_ppm(ppm)
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "mass_dev_ppm": float(self.mass_dev_ppm),
            }
        else:
            return {"activate_module": self.activate_module}


class SpecSimNetworkCosineParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spec. similarity network params.

    This class manages parameters for the modified cosine algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        msms_min_frag_nr: minimum nr of fragments a spectrum must have to be considered.
        fragment_tol: the tolerance between matched fragments, in m/z units.
        score_cutoff: the minimum similarity score between two spectra.
        max_nr_links: max nr of connections from a node.
        maximum_runtime: max runtime of module, in seconds; 0 indicates no runtime limit

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    msms_min_frag_nr: PositiveInt = 5
    fragment_tol: PositiveFloat = 0.1
    score_cutoff: PositiveFloat = 0.7
    max_nr_links: PositiveInt = 10
    maximum_runtime: int = 1200

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "msms_min_frag_nr": int(self.msms_min_frag_nr),
                "fragment_tol": float(self.fragment_tol),
                "score_cutoff": float(self.score_cutoff),
                "max_nr_links": int(self.max_nr_links),
                "maximum_runtime": int(self.maximum_runtime),
            }
        else:
            return {"activate_module": self.activate_module}


class SpecSimNetworkDeepscoreParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spec. similarity network params.

    This class manages parameters for the ms2deepscore algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        score_cutoff: the minimum similarity score between two spectra.
        max_nr_links: max links to a single spectra.
        msms_min_frag_nr: minimum number of fragments in MS2 to run it in analysis
        maximum_runtime: max runtime of module, in seconds; 0 indicates no runtime limit

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    score_cutoff: PositiveFloat = 0.8
    max_nr_links: PositiveInt = 10
    msms_min_frag_nr: PositiveInt = 5
    maximum_runtime: int = 1200

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "score_cutoff": float(self.score_cutoff),
                "max_nr_links": int(self.max_nr_links),
                "msms_min_frag_nr": int(self.msms_min_frag_nr),
                "maximum_runtime": int(self.maximum_runtime),
            }
        else:
            return {"activate_module": self.activate_module}
