"""Organizes several classes that hold and validate parameters for additional modules.

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
from pathlib import Path
from typing import List, Optional

from pydantic import (
    BaseModel,
    model_validator,
    PositiveInt,
    PositiveFloat,
    DirectoryPath,
)

from fermo_core.input_output.class_validation_manager import ValidationManager


class FeatureFilteringParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of feature filtering parameters.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        filter_rel_int_range: A range of relative peak intensity to retain features.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
        ValueError: raised by 'validate_range_zero_one', malformed range.
    """

    activate_module: bool = False
    filter_rel_int_range: Optional[List[float]] = None

    @model_validator(mode="after")
    def order_and_validate_range(self):
        if self.filter_rel_int_range is not None:
            r_list = self.filter_rel_int_range
            r_list = [min(r_list), max(r_list)]
            ValidationManager.validate_range_zero_one(r_list)
            self.filter_rel_int_range = r_list
            return self


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


class SpectralLibMatchingCosineParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spectral library matching params.

    This class addresses parameters for the modified cosine algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        fragment_tol: max tolerable diff to consider two fragments as equal, in m/z
        min_nr_matched_peaks: peak cutoff to consider a match of two MS/MS spectra
        score_cutoff: score cutoff to consider a match of two MS/MS spectra

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    fragment_tol: PositiveFloat = 0.1
    min_nr_matched_peaks: PositiveInt = 5
    score_cutoff: PositiveFloat = 0.7


class SpectralLibMatchingDeepscoreParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spectral library matching params.

    This class addresses parameters for the MS2DeepScore algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        directory_path: pathlib Path object pointing to dir with ms2deepscore files.
        score_cutoff: score cutoff to consider a match of two MS/MS spectra.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    directory_path: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2deepscore"
    )
    score_cutoff: PositiveFloat = 0.7


class Ms2QueryAnnotationParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of ms2query annotation params.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        directory_path: pathlib Path object pointing to dir with ms2query files.
        consider_blank: indicates if blank-associated features are annotated too
        filter_rel_int_range: only features inside range are annotated

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    directory_path: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2query"
    )
    consider_blank: bool = False
    filter_rel_int_range: List[float] = [0.0, 1.0]

    @model_validator(mode="after")
    def order_and_validate_range(self):
        r_list = self.filter_rel_int_range
        r_list = [min(r_list), max(r_list)]
        ValidationManager.validate_range_zero_one(r_list)
        self.filter_rel_int_range = r_list
        return self
