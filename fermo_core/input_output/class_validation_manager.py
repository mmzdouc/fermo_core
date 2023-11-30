"""Hold methods to validate user input.

Validation methods that are used by both graphical user interface and command line
interface.

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
    """Manage methods for user input validation and error-handling logic.

    Notes:
        All validation methods are static and raise errors that need to be handled
            by the calling methods.
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
            raise TypeError(f"Not a valid text string: '{string}'.")
        elif not len(string) > 0:
            raise TypeError(f"Empty text string: '{string}'.")

    @staticmethod
    def validate_bool(boolean: bool):
        """Validate if input is boolean.

        Args:
            boolean: a bool

        Raises:
            TypeError: Not a boolean value
        """
        if not isinstance(boolean, bool):
            raise TypeError(f"Not a boolean value (True/False): '{boolean}'.")

    @staticmethod
    def validate_integer(integer: int):
        """Validate that input is an integer.

        Parameters:
            integer: an integer

        Raises:
            TypeError: not a valid integer
        """
        if not isinstance(integer, int):
            raise TypeError(f"Not a valid integer number: '{integer}'.")

    @staticmethod
    def validate_float(float_nr: float):
        """Validate that input is a float number.

        Parameters:
            float_nr: a float

        Raises:
            TypeError: not a valid float
        """
        if not isinstance(float_nr, float):
            raise TypeError(f"Not a valid float point number: '{float_nr}'.")

    @staticmethod
    def validate_positive_number(number: int | float):
        """Validate if input is a positive number.

        Args:
            number: a positive number.

        Raises:
            ValueError: Not a positive number.
        """
        if not number > 0:
            raise ValueError(f"Not a positive number: '{number}'")

    @staticmethod
    def validate_mass_deviation_ppm(ppm: int):
        """Validate if mass deviation is in reasonable range.

        Args:
            ppm: a mass deviation value in ppm.

        Raises:
            ValueError: Out of reasonable range.
        """
        if ppm > 100:
            raise ValueError(
                f"User-specified mass deviation '{ppm}' greater than "
                f"reasonable maximum of '100'."
            )

    @staticmethod
    def validate_file_exists(file_path: str):
        """Validate that input file exists.

        Parameters:
            file_path: a valid path as str

        Raises:
            FileNotFoundError: file does not exist
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def validate_file_extension(filepath: Path, extension: str):
        """Validate the file name extension.

        Parameters:
            filepath: A pathlib Path object
            extension: a str describing the file extension

        Raises:
            TypeError: incorrect file name extension
        """
        if filepath.suffix != extension:
            raise TypeError(
                f"File extension incorrect. Should be '{extension}', is"
                f" '{filepath.suffix}'."
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
    def validate_csv_file(csv_file: Path):
        """Validate that input file is a comma separated values file (csv).

        Args:
           csv_file: A pathlib Path object

        Raises:
           pd.errors.ParserError if file is not readable by pandas
        """
        try:
            pd.read_csv(csv_file, sep=",")
        except pd.errors.ParserError:
            raise ValueError(
                f"File '{csv_file.name}' does not seem to be a valid file in '.csv' "
                f"format."
            )

    @staticmethod
    def validate_peaktable_mzmine3(mzmine_file: Path):
        """Validate that input file is a mzmine3-style peaktable

        Args:
           mzmine_file: A pathlib Path object

        Raises:
            ValueError: unexpected values
        """
        df = pd.read_csv(mzmine_file, sep=",")
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
                    f"'{mzmine_file.name}'."
                )

    @staticmethod
    def validate_no_duplicate_entries_csv_column(csv_file: Path, column: str):
        """Validate that csv column has no duplicate entries

        Args:
           csv_file: A pathlib Path object
           column: Name of column to test for duplicate entries

        Raises:
            ValueError: duplicate entries found
        """
        df = pd.read_csv(csv_file, sep=",")
        if df.duplicated(subset=[column]).any():
            raise ValueError(
                f"Duplicate entries found in column '{column}' of file '"
                f"{csv_file.name}'. The "
                f"same identifier cannot be used multiple times."
            )

    @staticmethod
    def validate_mgf_file(mgf_file: Path):
        """Validate that file is a mgf file containing MS/MS spectra.

        Args:
           mgf_file: A pathlib Path object to a Mascot Generic Format (mgf) file

        Raises:
            ValueError: Not a mgf file or empty
        """
        try:
            with open(mgf_file) as infile:
                next(mgf.read(infile))
        except StopIteration:
            raise ValueError(f"File '{mgf_file.name}' is not a .mgf-file or is empty.")

    @staticmethod
    def validate_phenotype_fermo(pheno_file: Path):
        """Validate that file is a phenotype file in fermo style.

        Args:
           pheno_file: A pathlib Path object pointing towards a fermo-bioactivity file

        Raises:
            ValueError: Not a fermo style bioactivity/phenotype file
        """

        def _raise_error(message):
            raise ValueError(f"{message} in file '{pheno_file.name}' detected.")

        df = pd.read_csv(pheno_file, sep=",")

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
    def validate_group_metadata_fermo(group_file: Path):
        """Validate that file is a group metadata file in fermo style.

        Args:
           group_file: A pathlib Path object to a fermo-group metadata file

        Raises:
            ValueError: Not a fermo style group metadata file
        """

        def _raise_error(message):
            raise ValueError(f"{message}  in file '{group_file.name}' detected.")

        df = pd.read_csv(group_file)

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

    @staticmethod
    def validate_range_zero_one(user_range: List[float]):
        """Validate that user-provided range is inside range 0-1.

        Args
           user_range: User-provided range: two floats, upper and lower bounds.

        Raises:
            TypeError: user-range not a list
            ValueError: More than two values OR not floats OR out of bounds
        """
        if not isinstance(user_range, list):
            raise ValueError("Range is wrongly formatted: not a list.")
        elif len(user_range) != 2:
            raise ValueError(
                f"Range must have exactly two values; has {len(user_range)} "
                f"('{user_range}')."
            )
        elif not all(isinstance(entry, float) for entry in user_range):
            raise ValueError("At least one of the values is not a float point number.")
        elif not all(0.0 <= entry <= 1.0 for entry in user_range):
            raise ValueError(
                "At least one of the values is outside of range 0.0 to 1.0."
            )
        elif not user_range[0] < user_range[1]:
            raise ValueError(
                f"The first value '{user_range[0]}' must be less than the second "
                f"value '{user_range[1]}'."
            )
