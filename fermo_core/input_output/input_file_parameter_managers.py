"""Organizes classes that handle and validate input file parameter.

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

from pydantic import BaseModel, model_validator, FilePath

from fermo_core.input_output.class_validation_manager import ValidationManager


class PeaktableParameters(BaseModel):
    """A Pydantic-based class for representing and validating peaktable parameters.

    Attributes:
        filepath: a pathlib Path object pointing towards a peaktable file
        format: indicates the format of the peaktable file
        polarity: indicates the polarity of the data ('positive', 'negative').

    Raise:
        ValueError: Unsupported peaktable format.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    filepath: FilePath
    format: str
    polarity: str

    @model_validator(mode="after")
    def validate_peaktable_format(self):
        path_peaktable = self.filepath
        format_peaktable = self.format
        match format_peaktable:
            case "mzmine3":
                ValidationManager.validate_file_extension(path_peaktable, ".csv")
                ValidationManager.validate_csv_file(path_peaktable)
                ValidationManager.validate_peaktable_mzmine3(path_peaktable)
                ValidationManager.validate_no_duplicate_entries_csv_column(
                    path_peaktable, "id"
                )
            case _:
                raise ValueError(f"Unsupported peaktable format: '{format_peaktable}'.")
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
            "polarity": str(self.polarity),
        }


class MsmsParameters(BaseModel):
    """A Pydantic-based class for representing and validating MS/MS file parameters.

    Attributes:
        filepath: a pathlib Path object pointing towards an MS/MS file
        format: indicates the format of the MS/MS file

    Raise:
        ValueError: Unsupported MS/MS file format.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    filepath: FilePath
    format: str

    @model_validator(mode="after")
    def validate_msms_format(self):
        path_msms = self.filepath
        format_msms = self.format
        match format_msms:
            case "mgf":
                ValidationManager.validate_file_extension(path_msms, ".mgf")
                ValidationManager.validate_mgf_file(path_msms)
            case _:
                raise ValueError(f"Unsupported MS/MS format: '{format_msms}'.")
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
        }


class PhenotypeParameters(BaseModel):
    """A Pydantic-based class for representing and validating phenotype file parameters.

    Attributes:
        filepath: a pathlib Path object pointing towards a phenotype file
        format: indicates the format of the phenotype file

    Raise:
        ValueError: Unsupported phenotype file format.
        pydantic.ValidationError: Pydantic validation failed during instantiation.

    Notes:
        A fermo-style phenotype data file is a .csv-file with the layout:

        sample_name,phenotype_col_1,phenotype_col_2,...,phenotype_col_n \n
        sample1,1,0.1 \n
        sample2,10,0.01 \n
        sample3,100,0.001 \n

        Ad columns: "sample_name" mandatory, one or more additional columns
        Ad values: One experiment per column. All experiments must be of the
        same type (e.g. concentration, percentage inhibition).
        This is indicated by the "mode" of the file:
        -> percentage-like (the higher the better),
        -> concentration-like (the lower the better)
    """

    filepath: FilePath
    format: str

    @model_validator(mode="after")
    def validate_phenotype_format(self):
        path_phenotype = self.filepath
        format_phenotype = self.format
        match format_phenotype:
            case "fermo":
                ValidationManager.validate_file_extension(path_phenotype, ".csv")
                ValidationManager.validate_csv_file(path_phenotype)
                ValidationManager.validate_phenotype_fermo(path_phenotype)
                ValidationManager.validate_no_duplicate_entries_csv_column(
                    path_phenotype, "sample_name"
                )
            case _:
                raise ValueError(f"Unsupported phenotype format: '{format_phenotype}'.")
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
        }


class GroupMetadataParameters(BaseModel):
    """A Pydantic-based class for representing and validating group metadata parameters.

    Attributes:
        filepath: a pathlib Path object pointing towards a group metadata file
        format: indicates the format of the group metadata file

    Raise:
        ValueError: Unsupported group metadata file format.
        pydantic.ValidationError: Pydantic validation failed during instantiation.

    Notes:
        A fermo-style group data file is a .csv-file with the layout:

        sample_name,group_col_1,group_col_2,...,group_col_n \n
        sample1,medium_A,condition_A \n
        sample2,medium_B,condition_A\n
        sample3,medium_C,condition_A \n

        Ad values: The only prohibited value is 'DEFAULT' which is reserved for
        internal use. 'BLANK' os a special value that indicates the sample/medium
        blank for automated subtraction.
    """

    filepath: FilePath
    format: str

    @model_validator(mode="after")
    def validate_group_metadata_format(self):
        path_group = self.filepath
        format_group = self.format
        match format_group:
            case "fermo":
                ValidationManager.validate_file_extension(path_group, ".csv")
                ValidationManager.validate_csv_file(path_group)
                ValidationManager.validate_group_metadata_fermo(path_group)
                ValidationManager.validate_no_duplicate_entries_csv_column(
                    path_group, "sample_name"
                )
            case _:
                raise ValueError(
                    f"Unsupported group metadata format: " f"'{format_group}'."
                )
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
        }


class SpecLibParameters(BaseModel):
    """Pydantic-based class for repres. and valid. of spectral library files parameters.

    Attributes:
        filepath: a pathlib Path object pointing towards a spectral library file
        format: indicates the format of the spectral library file

    Raise:
        ValueError: Unsupported spectral library format.
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    filepath: FilePath
    format: str

    @model_validator(mode="after")
    def validate_spectral_library_format(self):
        path_speclib = self.filepath
        format_speclib = self.format
        match format_speclib:
            case "mgf":
                ValidationManager.validate_file_extension(path_speclib, ".mgf")
                ValidationManager.validate_mgf_file(path_speclib)
            case _:
                raise ValueError(
                    f"Unsupported spectral library format: " f"'{format_speclib}'."
                )
        return self

    def to_json(self: Self) -> dict:
        """Convert attributes to json-compatible ones."""
        return {
            "filepath": str(self.filepath.resolve()),
            "format": str(self.format),
        }
