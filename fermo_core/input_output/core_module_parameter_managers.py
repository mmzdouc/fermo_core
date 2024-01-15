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

from pathlib import Path
from pydantic import (
    BaseModel,
    model_validator,
    PositiveFloat,
    PositiveInt,
    DirectoryPath,
)

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
    mass_dev_ppm: PositiveFloat = 20.0

    @model_validator(mode="after")
    def validate_adduct_annotation_parameters(self):
        ppm = self.mass_dev_ppm
        ValidationManager.validate_mass_deviation_ppm(ppm)
        return self


class SpecSimNetworkCosineParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spec. similarity network params.

    This class manages parameters for the modified cosine algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        msms_min_frag_nr: minimum nr of fragments a spectrum must have to be considered.
        fragment_tol: the tolerance between matched fragments, in m/z units.
        min_nr_matched_peaks: the min number of peaks two matching spectra must share.
        score_cutoff: the minimum similarity score between two spectra.
        max_nr_links: max nr of connections from a node.
        max_precursor_mass_diff: max diff between precursor masses of two spectra
        maximum_runtime: max runtime of module, in seconds; 0 indicates no runtime limit

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    msms_min_frag_nr: PositiveInt = 5
    fragment_tol: PositiveFloat = 0.1
    min_nr_matched_peaks: PositiveInt = 5
    score_cutoff: PositiveFloat = 0.7
    max_nr_links: PositiveInt = 10
    max_precursor_mass_diff: PositiveInt = 400
    maximum_runtime: int = 1200


class SpecSimNetworkDeepscoreParameters(BaseModel):
    """A Pydantic-based class for repr. and valid. of spec. similarity network params.

    This class manages parameters for the ms2deepscore algorithm.

    Attributes:
        activate_module: bool to indicate if module should be executed.
        directory_path: pathlib Path object pointing to dir with ms2deepscore files.
        filename: the name of the ms2deepscore reference file.
        url: the URL to download the file from
        score_cutoff: the minimum similarity score between two spectra.
        max_nr_links: max links to a single spectra.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    activate_module: bool = True
    directory_path: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2deepscore"
    )
    filename: str = "ms2deepscore_positive_10k_1000_1000_1000_500.hdf5"
    url: str = (
        "https://zenodo.org/records/8274763/files/"
        "ms2deepscore_positive_10k_1000_1000_1000_500.hdf5?download=1"
    )
    score_cutoff: PositiveFloat = 0.7
    max_nr_links: PositiveInt = 10
