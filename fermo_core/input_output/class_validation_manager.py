"""Hold methods to validate user input from command line and GUI.

Validation methods consist of static methods for validation of generic values
and instance methods for testing of more specialized input values/parameters.

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
import pandas as pd
from pathlib import Path
from pyteomics import mgf
from typing import List


class ValidationManager:
    """Manage methods for user input validation and error-handling logic

    Method syntax: All validation methods should start with "validate".
    """

    @staticmethod
    def validate_string(string: str):
        """Validate that input is a string.

        Parameters:
            string: a valid string

        Raises:
            TypeError: not a valid string
        """
        if not isinstance(string, str):
            raise TypeError(f"Not a valid string: '{string}'.")

    @staticmethod
    def validate_integer(integer: int):
        """Validate that input is an integer.

        Parameters:
            integer: an integer

        Raises:
            TypeError: not a valid string
        """
        if not isinstance(int(integer), int):
            raise TypeError(f"Not a valid integer value: '{integer}'.")

    @staticmethod
    def validate_file_exists(path: str):
        """Validate that input file exists.

        Parameters:
            path: a valid path as str

        Raises:
            FileNotFoundError: file does not exist
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"File not found: {path}")

    @staticmethod
    def validate_file_extension(path: str, extension: str):
        """Validate the file name extension.

        Parameters:
            path: a valid path as str
            extension: a str describing the file extension

        Raises:
            FileExtensionError: incorrect file name extension
        """
        if Path(path).suffix != extension:
            raise TypeError(
                f"File extension incorrect. Should be '{extension}', is"
                f" {Path(path).suffix}."
            )

    @staticmethod
    def validate_keys(json_dict: dict, *args: str):
        """Validate presence of keys in dict.

        Parameters:
            json_dict: a dictionary containing one or more keys
            args: one or more keys to validate

        Raises:
            KeyError: missing key in dict
        """
        for arg in args:
            if json_dict.get(arg) is None:
                raise KeyError(f"Could not find parameter '{arg}'.")

    @staticmethod
    def validate_value_in_list(list_values: List[str], value: str):
        """Validate presence of a value in a list.

        Parameters:
            list_values: a list of strings
            value: a string to validate presence in list

        Raises:
            ValueError: missing value in list
        """
        if value not in list_values:
            raise ValueError(
                f"Could not find specified format '{value}' in allowed formats "
                f"'{list_values}'."
            )

    @staticmethod
    def validate_csv_file(csv_file: str):
        """Validate that input file is a comma separated values file (csv).

        Args:
           csv_file: A file path str

        Raises:
           pd.errors.ParserError if file is not readable by pandas
        """
        try:
            pd.read_csv(csv_file, sep=",")
        except pd.errors.ParserError:
            raise ValueError(
                f"File '{csv_file}' does not seem to be a valid file in '.csv' format."
            )

    @staticmethod
    def validate_peaktable_mzmine3(mzmine: str):
        """Validate that input file is a mzmine3-style peaktable

        Args:
           mzmine: A validated file path string to a mzmine3-style file

        Raises:
            ValueError: unexpected values
        """
        df = pd.read_csv(mzmine, sep=",")
        for arg in [
            ("^id$", "id"),
            ("^mz$", "mz"),
            ("^rt$", "rt"),
            ("^datafile:", "datafile: ..."),
            (":intensity_range:max$", "... :intensity_range:max"),
            (":feature_state$", "... :feature_state"),
            (":fwhm$", "... :fwhm"),
            (":rt$", "... :rt"),
            (":rt_range:min$", "... :rt_range:min"),
            (":rt_range:max$", "... :rt_range:max"),
        ]:
            if df.filter(regex=arg[0]).columns.empty:
                raise KeyError(
                    f"Column '{arg[1]}' is missing in MZmine3-style peaktable "
                    f"'{mzmine}'."
                )

    @staticmethod
    def validate_no_duplicate_entries_csv_column(csv: str, column: str):
        """Validate that csv column has no duplicate entries

        Args:
           csv: A validated file path string to a csv file
           column: Name of column to test for duplicate entries

        Raises:
            ValueError: duplicate entries found
        """
        df = pd.read_csv(csv, sep=",")
        if df.duplicated(subset=[column]).any():
            raise ValueError(
                f"Duplicate entries found in column '{column}' of file 'csv'. The "
                f"same identifier cannot be used multiple times."
            )

    @staticmethod
    def validate_mgf_file(mgf_file: str):
        """Validate that file is a mgf file containing MS/MS spectra.

        Args:
           mgf_file: A validated file path string pointing toward a mascot generic
            format (mgf) file

        Raises:
            ValueError: Not a mgf file or empty
        """
        try:
            with open(mgf_file) as infile:
                next(mgf.read(infile))
        except StopIteration:
            raise ValueError(f"File '{mgf_file}' is not a .mgf-file or is empty.")

    @staticmethod
    def validate_phenotype_fermo(phenotype: str):
        """Validate that file is a phenotype file in fermo style.

        Args:
           phenotype: A validated file path string pointing toward a fermo-style
           phenotype/bioactivity file.

        Raises:
            ValueError: Not a fermo style bioactivity/phenotype file
        """

        def _raise_error(message):
            raise ValueError(f"{message}  in file '{phenotype}' detected.")

        df = pd.read_csv(phenotype, sep=",")

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif not len(df.columns) > 1:
            _raise_error("No data column(s)")
        elif df.isnull().any().any():
            _raise_error("Empty fields in 'sample_name' or data column(s)")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")
        elif (
            df.loc[:, df.columns != "sample_name"]
            .select_dtypes(include="object")
            .any()
            .any()
        ):
            _raise_error("Data column(s) with non-numeric values")

    @staticmethod
    def validate_group_metadata_fermo(group: str):
        """Validate that file is a group metadata file in fermo style.

        Args:
           group: A validated file path string pointing toward a fermo-style group
            metadata file

        Raises:
            ValueError: Not a fermo style group metadata file
        """

        def _raise_error(message):
            raise ValueError(f"{message}  in file '{group}' detected.")

        df = pd.read_csv(group)

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif not len(df.columns) > 1:
            _raise_error("No data column(s)")
        elif df.isnull().any().any():
            _raise_error("Empty fields in 'sample_name' or data column(s)")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")
        elif df.applymap(lambda x: x == "DEFAULT").any().any():
            _raise_error("Fields with prohibited value 'DEFAULT'")
