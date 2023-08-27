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
from typing import Self, Tuple


class ValidationHandler:
    """Handle methods for user input validation.

    Method syntax: All validation methods should start with "validate".
    """

    @staticmethod
    def validate_bool(b: bool) -> Tuple[bool, str]:
        """Validate input boolean, return outcome and message.

        Args:
            b: input-value for validation.

        Returns:
            Tuple with [0] validation outcome and [1] (error) message.
        """
        if not isinstance(b, bool):
            return False, "Not a valid input. Please type 'True' or 'False'."
        else:
            return True, ""

    @staticmethod
    def validate_string(s: str) -> Tuple[bool, str]:
        """Validate that input is a string.

        Args:
            s: input-value for validation.

        Returns:
            Tuple with [0] validation outcome and [1] (error) message.
        """
        if not isinstance(s, str):
            return False, "Not a valid string."
        else:
            return True, ""

    @staticmethod
    def validate_pos_int(i: int) -> Tuple[bool, str]:
        """Validate that input is a positive integer greater than zero.

        Args:
            i: input-value for validation.

        Returns:
            Tuple with [0] validation outcome and [1] (error) message.
        """
        if not isinstance(i, int):
            return False, "Not an integer value."
        elif not i > 0:
            return False, "Value not > 0"
        else:
            return True, ""

    @staticmethod
    def validate_pos_int_or_zero(i: int) -> Tuple[bool, str]:
        """Validate that input is a positive integer greater than or equal to zero.

        Args:
            i: input-value for validation.

        Returns:
            Tuple with [0] validation outcome and [1] (error) message.
        """
        if not isinstance(i, int):
            return False, "Not an integer value."
        elif not i >= 0:
            return False, "Value not >= 0"
        else:
            return True, ""

    @staticmethod
    def validate_float_zero_one(f: float) -> Tuple[bool, str]:
        """Validate that input is a float between or equal to zero and one.

        Args:
            f: input-value for validation.

        Returns:
            Tuple with [0] validation outcome and [1] (error) message.
        """
        if not isinstance(f, float):
            return False, "Not a float (comma) number."
        elif not 0 <= f <= 1:
            return False, "Not a number from 0.0 to 1.0."
        else:
            return True, ""

    def validate_mass_dev_ppm(self: Self, ppm: int) -> Tuple[bool, str]:
        """Validate that input is a valid and sensible mass deviation value.

        Args:
           ppm: mass deviation in ppm, determines mass accuracy.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not (response := self.validate_pos_int(ppm))[0]:
            return response
        elif not ppm <= 100:
            return False, "Value unreasonable high (> 100 ppm)."
        else:
            return True, ""

    def validate_spectral_sim_network_alg(self: Self, alg: str) -> Tuple[bool, str]:
        """Validate input string for spectral_sim_network_alg for type and validity.

        Args:
           alg: choice of spectral similarity networking algorithm.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not (response := self.validate_string(alg))[0]:
            return response
        elif not any(
            alg == item for item in ["all", "modified_cosine", "ms2deepscore"]
        ):
            return False, "Not a valid algorithm choice."
        else:
            return True, ""

    @staticmethod
    def validate_range_zero_one(r: Tuple[float, ...]) -> Tuple[bool, str]:
        """Validate input range.

        Args:
           r: tuple with two floats between and including 0-1.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not len(r) == 2:
            return False, f"Only two values allowed. Nr of provided values: {len(r)}."
        elif not all(isinstance(i, float) for i in r):
            return False, "At least one of the values is not a float."
        elif not all(0.0 <= i <= 1.0 for i in r):
            return False, "At least one of the values is outside of range 0.0-1.0."
        elif not r[0] < r[1]:
            return (
                False,
                f"The first value {r[0]} must be smaller than the second "
                f"value {r[1]}.",
            )
        else:
            return True, ""

    @staticmethod
    def validate_path(s: str) -> Tuple[bool, str]:
        """Validate that Path can be called on input.

        Args:
           s: A string pointing toward a file.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        try:
            Path(s)
            return True, ""
        except TypeError:
            return False, "Does not appear to be a file."

    @staticmethod
    def validate_file_exists(f: Path) -> Tuple[bool, str]:
        """Validate that input file exists.

        Args:
           f: A pathlib.Path instance that points towards a file.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not Path.exists(f):
            return False, "File does not exist."
        else:
            return True, ""

    @staticmethod
    def validate_file_ending(f: Path, ending: str) -> Tuple[bool, str]:
        """Validate that input file has the correct ending.

        Args:
           f: A pathlib.Path instance that points towards a file.
           ending: The required file ending

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if f.suffix != ending:
            return False, f"File ending should be {ending}, is {f.suffix}."
        else:
            return True, ""

    def validate_csv_file(self: Self, f: Path) -> Tuple[bool, str]:
        """Validate that input file is a comma separated values file (csv).

        Args:
           f: A pathlib.Path instance that points towards a file.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """

        if not (response := self.validate_file_exists(f))[0]:
            return response
        elif not (response := self.validate_file_ending(f, ".csv"))[0]:
            return response

        try:
            pd.read_csv(f, sep=",")
            return True, ""
        except pd.errors.ParserError:
            return False, "Does not appear to be a .csv file."

    @staticmethod
    def validate_csv_duplicate_col_entries(
        df: pd.DataFrame, column: str
    ) -> Tuple[bool, str]:
        """Validate that there are no duplicate entries in a column.

        Args:
           df: A pd.DataFrame instance containing input csv file.
           column: The column to check for duplicate entries.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if df.duplicated(subset=[column]).any():
            return False, f"Duplicate entries in column '{column}'."
        else:
            return True, ""

    def validate_peaktable_mzmine3(self: Self, f: Path) -> Tuple[bool, str]:
        """Validate that input file is a mzmine3-style peaktable

        Args:
           f: A pathlib.Path instance that points towards a mzmine3-style peaktable.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not (response := self.validate_csv_file(f))[0]:
            return response

        df = pd.read_csv(f)

        def _is_col_name(exp: str, msg: str) -> Tuple[bool, str]:
            if df.filter(regex=exp).columns.empty:
                return False, f"Column '{msg}' is missing."
            else:
                return True, ""

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
            if not (outcome := _is_col_name(arg[0], arg[1]))[0]:
                return outcome

        if (response := self.validate_csv_duplicate_col_entries(df, "id"))[0]:
            return response

        return True, ""

    def validate_mgf(self: Self, f: Path) -> Tuple[bool, str]:
        """Validate that input file is a .mfg-file containing MS/MS spectra.

        Args:
           f: A pathlib.Path instance that points towards a .mgf-file.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not (response := self.validate_file_exists(f))[0]:
            return response
        elif not (response := self.validate_file_ending(f, ".mgf"))[0]:
            return response

        with open(f) as infile:
            try:
                next(mgf.read(infile))
            except StopIteration:
                return False, "Is not an .mgf-file or is empty."

        return True, ""

    def validate_phenotype_fermo(self: Self, f: Path, mode: str) -> Tuple[bool, str]:
        """Validate that input file is a fermo-style phenotype data table.

        A fermo-style phenotype data file is a .csv-file with the layout:

        sample_name,phenotype_col_1,phenotype_col_2,...,phenotype_col_n \n
        sample1,1,0.1 \n
        sample2,10,0.01 \n
        sample3,100,0.001 \n

        Ad columns: "sample_name" mandatory, one or more further columns
        Ad values: One experiment per column. All experiments must be of the same type
        (e.g. concentration, percentage inhibition). This is indicated by the "mode"
        of the file: percentage-like (the higher the better), concentration-like (the
        lower the better)

        Args:
           f: A pathlib.Path instance that points towards a fermo-style phenotype data
           table.
           mode: Specifying the formatting mode of the phenotype data table.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if mode is None:
            return False, "'--phenotype_fermo_mode' must be specified, was left empty."
        elif not any(mode == item for item in ["percentage", "concentration"]):
            return (
                False,
                "'--phenotype_fermo_mode' not 'percentage' or 'concentration'.",
            )
        elif not (response := self.validate_csv_file(f))[0]:
            return response

        df = pd.read_csv(f)

        if df.filter(regex="^sample_name$").columns.empty:
            return False, "No column labelled 'sample_name' detected."
        elif not len(df.columns) > 1:
            return False, "No data column(s) detected."
        elif df.isnull().any().any():
            return False, "Empty fields in 'sample_name' or data column(s) detected."
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            return False, "Fields containing only (white)space detected."
        elif (
            df.loc[:, df.columns != "sample_name"]
            .select_dtypes(include="object")
            .any()
            .any()
        ):
            return False, "Data column(s) include non-numeric values."
        elif not (
            response := self.validate_csv_duplicate_col_entries(df, "sample_name")
        )[0]:
            return response

        return True, ""

    def validate_group_fermo(self: Self, f: Path) -> Tuple[bool, str]:
        """Validate that input file is a fermo-style group data table.

        A fermo-style group data file is a .csv-file with the layout:

        sample_name,group_col_1,group_col_2,...,group_col_n \n
        sample1,medium_A,condition_A \n
        sample2,medium_B,condition_A\n
        sample3,medium_C,condition_A \n

        Ad values: The only prohibited value is 'GENERAL' which is reserved for
        internal use. 'BLANK' os a special value that indicates the sample/medium
        blank for automated subtraction.

        Args:
           f: A pathlib.Path instance that points towards a fermo-style group data
           table.

        Returns:
           Tuple with [0] validation outcome and [1] (error) message.
        """
        if not (response := self.validate_csv_file(f))[0]:
            return response

        df = pd.read_csv(f)

        if df.filter(regex="^sample_name$").columns.empty:
            return False, "No column labeled 'sample_name' detected."
        elif not len(df.columns) > 1:
            return False, "No data column(s) detected."
        elif df.isnull().any().any():
            return False, "Empty fields in 'sample_name' or data column(s) detected."
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            return False, "Fields containing only (white)space detected."
        elif df.applymap(lambda x: x == "DEFAULT").any().any():
            return False, "Fields with prohibited value 'DEFAULT' detected."

        return True, ""
