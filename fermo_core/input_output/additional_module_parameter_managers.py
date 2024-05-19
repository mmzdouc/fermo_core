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

import logging
from typing import Optional, Self

from pydantic import BaseModel, PositiveFloat, PositiveInt, model_validator

from fermo_core.input_output.class_validation_manager import ValidationManager

logger = logging.getLogger("fermo_core")


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
    filter_rel_int_range: Optional[list[float]] = None
    filter_rel_area_range: Optional[list[float]] = None

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
    def order_and_validate_range(r_list: list[float]) -> list[float]:
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
        factor: An integer fold-change to differentiate blank features.
        algorithm: the algorithm to summarize values of different samples.
        value: the type of value to use for determination

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    factor: PositiveInt = 10
    algorithm: str = "mean"
    value: str = "area"

    @model_validator(mode="after")
    def validate_strs(self):
        if self.algorithm not in ["mean", "median", "maximum"]:
            logger.warning(
                f"Unsupported 'algorithm' format: '{self.algorithm}'. "
                "Set to default value 'mean'."
            )
            self.algorithm = "mean"
        if self.value not in ["height", "area"]:
            logger.warning(
                f"Unsupported 'value' format: '{self.value}'. "
                "Set to default value 'area'."
            )
            self.value = "area"
        return self

    def to_json(self: Self) -> dict:
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "factor": int(self.factor),
                "algorithm": str(self.algorithm),
                "value": str(self.value),
            }
        else:
            return {"activate_module": self.activate_module}


class GroupFactAssignmentParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of group factor assignment params.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        algorithm: the algorithm to summarize values of different samples.
        value: the type of value to use for comparison
    """

    activate_module: bool = False
    algorithm: str = "mean"
    value: str = "area"

    @model_validator(mode="after")
    def validate_strs(self):
        if self.algorithm not in ["mean", "median", "maximum"]:
            logger.warning(
                f"Unsupported 'algorithm' format: '{self.algorithm}'. "
                "Set to default value 'mean'."
            )
            self.algorithm = "mean"
        if self.value not in ["height", "area"]:
            logger.warning(
                f"Unsupported 'value' format: '{self.value}'. "
                "Set to default value 'area'."
            )
            self.value = "area"
        return self

    def to_json(self: Self) -> dict:
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "algorithm": str(self.algorithm),
                "value": str(self.value),
            }
        else:
            return {"activate_module": self.activate_module}


class PhenoQualAssgnParams(BaseModel):
    """A Pydantic-based class for phenotype qualitative assignment parameters

    Attributes:
        activate_module: bool to indicate if module should be executed.
        factor: An integer fold-change to differentiate phenotype-assoc. features.
        algorithm: the algorithm to summarize values of active vs inactive samples.
        value: the type of value to use for determination
    """

    activate_module: bool = False
    factor: PositiveInt = 10
    algorithm: str = "minmax"
    value: str = "area"

    @model_validator(mode="after")
    def validate_strs(self):
        if self.algorithm not in ["mean", "median", "minmax"]:
            logger.warning(
                f"Unsupported 'algorithm' format: '{self.algorithm}'. "
                "Set to default value 'minmax'."
            )
            self.algorithm = "minmax"
        if self.value not in ["height", "area"]:
            logger.warning(
                f"Unsupported 'value' format: '{self.value}'. "
                "Set to default value 'area'."
            )
            self.value = "area"
        return self

    def to_json(self: Self) -> dict:
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "factor": int(self.factor),
                "algorithm": str(self.algorithm),
                "value": str(self.value),
            }
        else:
            return {"activate_module": self.activate_module}


class PhenoQuantPercentAssgnParams(BaseModel):
    """A Pydantic-based class for phenotype quantitative percentage assignment params

    Attributes:
        activate_module: bool to indicate if module should be executed.
        sample_avg: algorithm to summarize mult measurements per sample for single assay
        value: the type of value to use for determination
        algorithm: the statistical algorithm to calculate correlation
        p_val_cutoff: minimum Bonferroni-corrected p-value to consider in assignment
        coeff_cutoff: minimum correlation coefficient cutoff to consider in assignment
    """

    activate_module: bool = False
    sample_avg: str = "mean"
    value: str = "area"
    algorithm: str = "pearson"
    p_val_cutoff: float = 0.05
    coeff_cutoff: float = 0.7

    @model_validator(mode="after")
    def validate_strs(self):
        if self.sample_avg not in ["mean", "median"]:
            logger.warning(
                f"Unsupported 'sample_avg' format: '{self.sample_avg}'. "
                "Set to default value 'mean'."
            )
            self.sample_avg = "mean"

        if self.value not in [
            "area",
        ]:
            logger.warning(
                f"Unsupported 'value' format: '{self.value}'. "
                "Set to default value 'area'."
            )
            self.value = "area"

        if self.algorithm not in [
            "pearson",
        ]:
            logger.warning(
                f"Unsupported 'algorithm' format: '{self.algorithm}'. "
                "Set to default value 'pearson'."
            )
            self.algorithm = "pearson"

        return self

    @model_validator(mode="after")
    def validate_floats(self):
        if self.p_val_cutoff > 1:
            logger.warning(
                f"Value for 'p_val_cutoff' greater than 1 (is '"
                f"{self.p_val_cutoff}'). Set to default value 0.05."
            )
            self.p_val_cutoff = 0.05
        if self.coeff_cutoff > 1:
            logger.warning(
                f"Value for 'coeff_cutoff' greater than 1 (is '"
                f"{self.coeff_cutoff}'). Set to default value 0.7."
            )
            self.coeff_cutoff = 0.7
        return self

    def to_json(self: Self) -> dict:
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "sample_avg": self.sample_avg,
                "value": self.value,
                "algorithm": self.algorithm,
                "p_val_cutoff": self.p_val_cutoff,
                "coeff_cutoff": self.coeff_cutoff,
            }
        else:
            return {"activate_module": self.activate_module}


class PhenoQuantConcAssgnParams(BaseModel):
    """A Pydantic-based class for phenotype quantitative concentration assignment params

    Attributes:
        activate_module: bool to indicate if module should be executed.
        sample_avg: algorithm to summarize mult measurements per sample for single assay
        value: the type of value to use for determination
        algorithm: the statistical algorithm to calculate correlation
        p_val_cutoff: minimum Bonferroni-corrected p-value to consider in assignment
        coeff_cutoff: minimum correlation coefficient cutoff to consider in assignment
    """

    activate_module: bool = False
    sample_avg: str = "mean"
    value: str = "area"
    algorithm: str = "pearson"
    p_val_cutoff: float = 0.05
    coeff_cutoff: float = 0.7

    @model_validator(mode="after")
    def validate_strs(self):
        if self.sample_avg not in ["mean", "median"]:
            logger.warning(
                f"Unsupported 'sample_avg' format: '{self.sample_avg}'. "
                "Set to default value 'mean'."
            )
            self.sample_avg = "mean"

        if self.value not in [
            "area",
        ]:
            logger.warning(
                f"Unsupported 'value' format: '{self.value}'. "
                "Set to default value 'area'."
            )
            self.value = "area"

        if self.algorithm not in [
            "pearson",
        ]:
            logger.warning(
                f"Unsupported 'algorithm' format: '{self.algorithm}'. "
                "Set to default value 'pearson'."
            )
            self.algorithm = "pearson"

        return self

    @model_validator(mode="after")
    def validate_floats(self):
        if self.p_val_cutoff > 1:
            logger.warning(
                f"Value for 'p_val_cutoff' greater than 1 (is '"
                f"{self.p_val_cutoff}'). Set to default value 0.05."
            )
            self.p_val_cutoff = 0.05
        if self.coeff_cutoff > 1:
            logger.warning(
                f"Value for 'coeff_cutoff' greater than 1 (is '"
                f"{self.coeff_cutoff}'). Set to default value 0.7."
            )
            self.coeff_cutoff = 0.7
        return self

    def to_json(self: Self) -> dict:
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "sample_avg": self.sample_avg,
                "value": self.value,
                "algorithm": self.algorithm,
                "p_val_cutoff": self.p_val_cutoff,
                "coeff_cutoff": self.coeff_cutoff,
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
    score_cutoff: PositiveFloat = 0.8
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
        score_cutoff: only matches with a score higher or equal to are retained
        maximum_runtime: maximum runtime in seconds

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = False
    score_cutoff: PositiveFloat = 0.7
    maximum_runtime: int = 600

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        if self.activate_module:
            return {
                "activate_module": self.activate_module,
                "score_cutoff": self.score_cutoff,
                "maximum_runtime": self.maximum_runtime,
            }
        else:
            return {"activate_module": self.activate_module}


class AsKcbCosineMatchingParams(BaseModel):
    """Pydantic-based class for params of antiSMASH KCB results mod cosine matching.

    Stores parameters for matching the in silico generated MS2 spectra of significant
    KnownClusterBlast hits from antiSMASH against the feature spectra. A targeted
    spectral library allows to use very loose similarity scores to allow for very
    distant hits. Uses the modified cosine algorithm.

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
    score_cutoff: PositiveFloat = 0.5
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


class AsKcbDeepscoreMatchingParams(BaseModel):
    """Pydantic-based class for params of antiSMASH KCB results deepscore matching.

    Stores parameters for matching the in silico generated MS2 spectra of significant
    KnownClusterBlast hits from antiSMASH against the feature spectra. A targeted
    spectral library allows to use very loose similarity scores to allow for very
    distant hits. Uses the MS2DeepScore algorithm.

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
