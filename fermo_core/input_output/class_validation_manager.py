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

import json
import logging
from pathlib import Path

import jsonschema
import pandas as pd
from pyteomics import mgf

logger = logging.getLogger("fermo_core")


class ValidationManager:
    """Manage methods for user input validation and error-handling logic.

    All validation methods are static and raise errors that need to be handled
    by the calling methods. All validation methods should start with "validate".
    """

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
    def validate_csv_file(csv_file: Path):
        """Validate that input file is a comma separated values file (csv).

        Args:
           csv_file: A pathlib Path object

        Raises:
           pd.errors.ParserError if file is not readable by pandas
        """
        try:
            pd.read_csv(csv_file, sep=",")
        except pd.errors.ParserError as e:
            logger.error(
                f"File '{csv_file.name}' does not seem to be a valid file in '.csv' "
                f"format."
            )
            raise e

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
    def validate_ms2query_results(ms2query_results: Path):
        """Validate format of ms2query results table

        Prepared for MS2Query version 1.3.0. Must have a column "id" corresponding to
        the feature id of the peak table.

        Args:
           ms2query_results: A pathlib Path object

        Raises:
            KeyError: missing columns in results file or empty
        """
        df = pd.read_csv(ms2query_results, sep=",")

        for arg in [
            ("^id$", "id"),
            ("^analog_compound_name", "analog_compound_name"),
            ("^ms2query_model_prediction", "ms2query_model_prediction"),
            ("^precursor_mz_difference", "precursor_mz_difference"),
            ("^precursor_mz_analog", "precursor_mz_analog"),
            ("^smiles", "smiles"),
            ("^inchikey", "inchikey"),
            ("^npc_class_results", "npc_class_results"),
        ]:
            if df.filter(regex=arg[0]).columns.empty:
                raise KeyError(
                    f"Column '{arg[1]}' is missing in MS2Query results file "
                    f"'{ms2query_results.name}'."
                )

    @staticmethod
    def validate_csv_has_rows(csv_path: Path):
        """Validate if csv file has rows

        Args:
           csv_path: A pathlib Path object

        Raises:
            ValueError: has no rows (data)
        """
        df = pd.read_csv(csv_path, sep=",")
        if df.shape[0] == 0:
            raise ValueError(f"Csv-file '{csv_path.name}' has no data rows.")

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
            StopIteration: Not a mgf file or empty
        """
        try:
            with open(mgf_file) as infile:
                next(mgf.read(infile))
        except StopIteration as e:
            logger.error(f"File '{mgf_file.name}' is not a .mgf-file or is empty.")
            raise e

    @staticmethod
    def validate_pheno_qualitative(pheno_file: Path):
        """Validate that file is a qualitative phenotype file

        Args:
           pheno_file: A pathlib Path object

        Raises:
            ValueError: Incorrect format
        """

        def _raise_error(message):
            raise ValueError(f"{message} in file '{pheno_file.name}' detected.")

        df = pd.read_csv(pheno_file, sep=",")

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif df.isnull().any().any():
            _raise_error("Empty fields in 'sample_name'")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")

    @staticmethod
    def validate_pheno_quant_percentage(pheno_file: Path):
        """Validate that file is a quantitative-percentage phenotype file

        Args:
           pheno_file: A pathlib Path object

        Raises:
            ValueError: Incorrect format
        """

        def _raise_error(message):
            raise ValueError(f"{message} in file '{pheno_file.name}' detected.")

        def _test_non_numeric_col(cols: list) -> bool:
            for col in cols:
                numeric_values = pd.to_numeric(df[col], errors="coerce")
                non_numeric_indices = numeric_values.isna()
                if non_numeric_indices.any():
                    return True

        df = pd.read_csv(pheno_file, sep=",")

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif df.filter(regex="^well$").columns.empty:
            _raise_error("No column labelled 'well'")
        elif len(df.columns) < 3:
            _raise_error("No assay column(s)")
        elif len(df.columns) > 8:
            _raise_error("Too many assay columns (maximum allowed: 6)")
        elif df["sample_name"].nunique() < 10:
            _raise_error("Less than 10 samples")
        elif df.isnull().any().any():
            _raise_error("Empty fields")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")
        elif any(df.columns.str.contains(r"\s")):
            _raise_error("Whitespace in column(s)")
        elif not any([col for col in df.columns if col.startswith("assay:")]):
            _raise_error("No columns starting with 'assay:'")
        elif _test_non_numeric_col([c for c in df.columns if c.startswith("assay:")]):
            _raise_error("Non-numeric values in assay column(s)")

    @staticmethod
    def validate_pheno_quant_concentration(pheno_file: Path):
        """Validate that file is a quantitative-concentration phenotype file

        Args:
           pheno_file: A pathlib Path object

        Raises:
            ValueError: Incorrect format
        """

        def _raise_error(message):
            raise ValueError(f"{message} in file '{pheno_file.name}' detected.")

        def _test_non_numeric_col(cols: list) -> bool:
            for col in cols:
                numeric_values = pd.to_numeric(df[col], errors="coerce")
                non_numeric_indices = numeric_values.isna()
                if non_numeric_indices.any():
                    return True

        df = pd.read_csv(pheno_file, sep=",")

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif df.filter(regex="^well$").columns.empty:
            _raise_error("No column labelled 'well'")
        elif len(df.columns) < 3:
            _raise_error("No assay column(s)")
        elif len(df.columns) > 8:
            _raise_error("Too many assay columns (maximum allowed: 6)")
        elif df["sample_name"].nunique() < 10:
            _raise_error("Less than 10 samples")
        elif df.isnull().any().any():
            _raise_error("Empty fields")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")
        elif any(df.columns.str.contains(r"\s")):
            _raise_error("Whitespace in column(s)")
        elif not any([col for col in df.columns if col.startswith("assay:")]):
            _raise_error("No columns starting with 'assay:'")
        elif _test_non_numeric_col([c for c in df.columns if c.startswith("assay:")]):
            _raise_error("Non-numeric values in assay column(s)")

    @staticmethod
    def validate_group_metadata_fermo(group_file: Path):
        """Validate that file is a group metadata file in fermo style.

        Args:
           group_file: A pathlib Path object to a fermo-group metadata file

        Raises:
            ValueError: Not a fermo style group metadata file
        """

        def _raise_error(message):
            raise ValueError(f"{message} in file '{group_file.name}' detected.")

        df = pd.read_csv(group_file)

        if df.filter(regex="^sample_name$").columns.empty:
            _raise_error("No column labelled 'sample_name'")
        elif len(df.columns) < 2:
            _raise_error("No category column(s)")
        elif len(df.columns) > 7:
            _raise_error("Too many category columns (maximum allowed: 7)")
        elif df.isnull().any().any():
            _raise_error("Empty fields")
        elif df.applymap(lambda x: str(x).isspace()).any().any():
            _raise_error("Fields containing only (white)space")
        elif df.applymap(lambda x: " " in str(x)).any().any():
            _raise_error("Fields containing (white)space")
        elif any(df.columns.str.contains(r"\s")):
            _raise_error("Whitespace in column(s)")

    @staticmethod
    def validate_range_zero_one(user_range: list[float]):
        """Validate that user-provided range is inside range 0.0 - 1.0.

        Arguments:
            user_range: User-provided range: two floats, upper and lower bounds.

        Raises:
            ValueError: More than two values OR not floats OR out of bounds
        """
        if len(user_range) > 2:
            raise ValueError("More than two values in range.")
        elif not all(0.0 <= entry <= 1.0 for entry in user_range):
            raise ValueError(
                "At least one of the values is outside of range 0.0 to 1.0."
            )
        elif not user_range[0] < user_range[1]:
            raise ValueError(
                f"The first value '{user_range[0]}' must be less than the second "
                f"value '{user_range[1]}'."
            )

    @staticmethod
    def validate_file_vs_jsonschema(user_input: dict, filename: str):
        """Validate user-input against jsonschema.

        Arguments:
            user_input: dict containing user-input, derived from json-file
            filename: the name of the input file for error message

        Raises:
            jsonschema.exceptions.ValidationError: user input does not validate against schema
        """
        with open(
            Path(__file__).parent.parent.joinpath("config/schema.json")
        ) as infile:
            schema = json.load(infile)

        try:
            jsonschema.validate(instance=user_input, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            lines = str(e).splitlines()
            msg = f"{filename}: {lines[0]}"
            logger.critical(msg)
            raise e

    @staticmethod
    def validate_output_created(filepath: Path):
        """Validate that output file was created and log if not

        Arguments:
            filepath: a Path object pointing to created output file

        Raises:
            FileNotFoundError: file should have been created but can't be found
        """
        if filepath.exists():
            logger.info(
                f"'ExportManager': Successfully wrote file " f"'{filepath.resolve()}'."
            )
        else:
            raise FileNotFoundError(
                f"'ExportManager': File '{filepath}' should have been written but "
                f"cannot be found - ABORT"
            )
