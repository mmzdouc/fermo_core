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

from pydantic import BaseModel, model_validator, PositiveInt

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
    mass_dev_ppm: PositiveInt = 20

    @model_validator(mode="after")
    def validate_adduct_annotation_parameters(self):
        ppm = self.mass_dev_ppm
        ValidationManager.validate_mass_deviation_ppm(ppm)
        return self
