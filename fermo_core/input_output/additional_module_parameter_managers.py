"""Organizes classes that hold and validate parameters for additional modules.

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
from typing import List, Optional, Self

from pydantic import (
    BaseModel,
    model_validator,
    PositiveInt,
    PositiveFloat,
)

from fermo_core.input_output.class_validation_manager import ValidationManager


class FeatureFilteringParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of feature filtering parameters.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        filter_rel_int_range: A range of relative peak intensity to retain features.
        filter_rel_area_range: A range of relative area to retain features.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
        ValueError: raised by 'validate_range_zero_one', malformed range.
    """

    activate_module: bool = False
    filter_rel_int_range: Optional[List[float]] = None
    filter_rel_area_range: Optional[List[float]] = None

    @model_validator(mode="after")
    def validate_attrs(self):
        if self.filter_rel_int_range is not None:
            self.filter_rel_int_range = self.order_and_validate_range(
                self.filter_rel_int_range
            )

        if self.filter_rel_area_range is not None:
            self.filter_rel_area_range = self.order_and_validate_range(
                self.filter_rel_area_range
            )

        return self

    @staticmethod
    def order_and_validate_range(r_list: List[float]) -> List[float]:
        """Order the list and validate format.

        Attributes:
            r_list: a range of two floats

        Returns:
            The modified list of a range of two floats
        """
        r_list = [min(r_list), max(r_list)]
        ValidationManager.validate_range_zero_one(r_list)
        return r_list

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "filter_rel_int_range": self.filter_rel_int_range,
                "filter_rel_area_range": self.filter_rel_area_range,
            }
        else:
            return {"activate_module": self.activate_module}


class BlankAssignmentParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of blank assignment parameters.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        column_ret_fold: An integer fold-change to differentiate blank features.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    column_ret_fold: PositiveInt = 10

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "column_ret_fold": int(self.column_ret_fold),
            }
        else:
            return {"activate_module": self.activate_module}


class PhenotypeAssignmentFoldParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of phenotype assignment parameters.

    This class addresses parameters for the fold-difference algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        fold_diff: An integer fold-change to differentiate phenotype-assoc. features.
        data_type: Type of data ('percentage'- or 'concentration'-like).

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    fold_diff: PositiveInt = 10
    data_type: str = "percentage"

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "fold_diff": int(self.fold_diff),
                "data_type": str(self.data_type),
            }
        else:
            return {"activate_module": self.activate_module}


class SpectralLibMatchingCosineParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spectral library matching params.

    This class addresses parameters for the modified cosine algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        fragment_tol: max tolerable diff to consider two fragments as equal, in m/z
        min_nr_matched_peaks: peak cutoff to consider a match of two MS/MS spectra
        score_cutoff: score cutoff to consider a match of two MS/MS spectra
        max_precursor_mass_diff: maximum precursor mass difference
        maximum_runtime: maximum runtime in seconds

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    fragment_tol: PositiveFloat = 0.1
    min_nr_matched_peaks: PositiveInt = 5
    score_cutoff: PositiveFloat = 0.7
    max_precursor_mass_diff: PositiveInt = 600
    maximum_runtime: int = 600

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "fragment_tol": float(self.fragment_tol),
                "min_nr_matched_peaks": int(self.min_nr_matched_peaks),
                "score_cutoff": float(self.score_cutoff),
                "max_precursor_mass_diff": int(self.max_precursor_mass_diff),
                "maximum_runtime": int(self.maximum_runtime),
            }
        else:
            return {"activate_module": self.activate_module}


class SpectralLibMatchingDeepscoreParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spectral library matching params.

    This class addresses parameters for the MS2DeepScore algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        score_cutoff: score cutoff to consider a match of two MS/MS spectra.
        max_precursor_mass_diff: max allowed precursor mz difference to accept a match
        maximum_runtime: maximum runtime in seconds

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    score_cutoff: PositiveFloat = 0.7
    max_precursor_mass_diff: PositiveInt = 600
    maximum_runtime: int = 600

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "score_cutoff": float(self.score_cutoff),
                "max_precursor_mass_diff": int(self.max_precursor_mass_diff),
                "maximum_runtime": int(self.maximum_runtime),
            }
        else:
            return {"activate_module": self.activate_module}


class Ms2QueryAnnotationParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of ms2query annotation params.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        exclude_blank: sets if blank-associated features should be excluded from annot
        score_cutoff: only matches with a score higher or equal to are retained
        maximum_runtime: maximum runtime in seconds

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    exclude_blank: bool = False
    score_cutoff: PositiveFloat = 0.7
    maximum_runtime: int = 600

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "exclude_blank": self.exclude_blank,
                "score_cutoff": self.score_cutoff,
                "maximum_runtime": self.maximum_runtime,
            }
        else:
            return {"activate_module": self.activate_module}
