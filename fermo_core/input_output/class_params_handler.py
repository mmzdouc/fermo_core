"""Hold parameters and methods to validate user input.

Interface to collect and hold user input from both command line and GUI.
Validation methods cover generic types as well as some plausibility testing
of specific parameters (e.g. mass_dev_ppm etc). Input files are validated more
thoroughly in their specific classes.

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
from typing import Self, Tuple


class ParamsHandler:
    """Organize user input for processing by fermo_core.

    Interface for user input from both graphical user interface and command line.
    Holds values and organizes methods for input testing.

    Attribute syntax: if multiple competing input styles for one input file
    type exists, they should be called with the same prefix (e.g. peaktable_fermo,
    (hypothetical) peaktable_openms)

    Method syntax: validation methods MUST start with "validate" prefix

    Attributes:
        version: Current program version.
        root: "Root" directory of program.
        session: Fermo json session file.
        peaktable_mzmine3: Mzmine3-style peaktable.
        msms_mgf: Mgf-style msms file.
        phenotype_fermo: Fermo-style phenotypic data file.
        group_fermo: Fermo-style group data file.
        speclib_mgf: Mgf-style spectral library file.
        mass_dev_ppm: Expected mass deviation tolerance in ppm.
        msms_frag_min: Minimum tolerable number of msms fragments per spectrum.
        phenotype_fold: Fold-factor to retain features in sub-inhibitory
            concentration.
        column_ret_fold: Fold-factor to retain features cross-bleeding in blanks.
        fragment_tol: Tolerance in m/z to connect features by spectral sim.
        spectral_sim_score_cutoff: Cutoff tolerance to connect features by
            spectra similarity.
        max_nr_links_spec_sim: Maximum tolerable nr of connections to other
            features per feature.
        min_nr_matched_peaks: Minimum tolerable nr of peaks for a match in
            spectral similarity matching.
        spectral_sim_network_alg: Selected spectral similarity networking algorithm.
        flag_ms2query: Flag for annotation by ms2query.
        flag_ms2query_blank: Flag for blank-associated feature annotation by
            ms2query.
        ms2query_filter_range: Restrict annotation by ms2query based on
            relative intensity.
        rel_int_range: Restrict processing of features based on relative
            intensity.
    """

    def __init__(self: Self, version: str, root: Path):
        self.version: str = version
        self.root: Path = root
        self.session: str | None = None
        self.peaktable_mzmine3: str | None = None
        self.msms_mgf: str | None = None
        self.phenotype_fermo: str | None = None
        self.group_fermo: str | None = None
        self.speclib_mgf: str | None = None
        self.mass_dev_ppm: int = 20
        self.msms_frag_min: int = 5
        self.phenotype_fold: int = 10
        self.column_ret_fold: int = 10
        self.fragment_tol: float = 0.1
        self.spectral_sim_score_cutoff: float = 0.7
        self.max_nr_links_spec_sim: int = 10
        self.min_nr_matched_peaks: int = 5
        self.spectral_sim_network_alg: str = "modified_cosine"
        self.flag_ms2query: bool = False
        self.flag_ms2query_blank: bool = False
        self.ms2query_filter_range: Tuple[float, float] = (0.0, 1.0)
        self.rel_int_range: Tuple[float, float] = (0.0, 1.0)

    @staticmethod
    def validate_bool(b: bool) -> Tuple[bool, str]:
        """Validate input boolean, return outcome and message.

        Args:
            b: input-value for validation.

        Returns:
            Tuple with outcome and (error) message.
        """
        if not isinstance(b, bool):
            return False, "Not a valid input. Please type 'True' or 'False'."
        else:
            return True, ""

    @staticmethod
    def validate_string(s: str) -> Tuple[bool, str]:
        """Validate input string, return outcome and message.

        Args:
            s: input-value for validation.

        Returns:
            Tuple with outcome and (error) message.
        """
        if not isinstance(s, str):
            return False, "Not a valid string."
        else:
            return True, ""

    @staticmethod
    def validate_pos_int(i: int) -> Tuple[bool, str]:
        """Validate input integer, return outcome and message.

        Args:
            i: input-value for validation.

        Returns:
            Tuple with outcome and (error) message.
        """
        if not isinstance(i, int):
            return False, "Not an integer value."
        elif not i > 0:
            return False, "Value not > 0"
        else:
            return True, ""

    @staticmethod
    def validate_pos_int_or_zero(i: int) -> Tuple[bool, str]:
        """Validate input integer, return outcome and message.

        Args:
            i: input-value for validation.

        Returns:
            Tuple with outcome and (error) message.
        """
        if not isinstance(i, int):
            return False, "Not an integer value."
        elif not i >= 0:
            return False, "Value not >= 0"
        else:
            return True, ""

    @staticmethod
    def validate_float_zero_one(f: float) -> Tuple[bool, str]:
        """Validate input float, return outcome and message.

        Args:
            f: input-value for validation.

        Returns:
            Tuple with outcome and (error) message.
        """
        if not isinstance(f, float):
            return False, "Not a float (comma) number."
        elif not 0 <= f <= 1:
            return False, "Not a number from 0.0 to 1.0."
        else:
            return True, ""

    @staticmethod
    def validate_mass_dev_ppm(ppm: int) -> Tuple[bool, str]:
        """Validate input for mass_dev_ppm for type and validity.

        Args:
           ppm: mass deviation in ppm, determines mass accuracy.

        Returns:
           Tuple with outcome and (error) message
        """
        if not isinstance(ppm, int):
            return False, "Not an integer value."
        elif not ppm > 0:
            return False, "No value < 1 allowed."
        elif not ppm <= 100:
            return False, "Value unreasonable high (> 100 ppm)."
        else:
            return True, ""

    @staticmethod
    def validate_spectral_sim_network_alg(alg: str) -> Tuple[bool, str]:
        """Validate input string for spectral_sim_network_alg for type and validity.

        Args:
           alg: choice of spectral similarity networking algorithm.

        Returns:
           Tuple with outcome and (error) message
        """
        if not isinstance(alg, str):
            return False, "Not a string."
        elif not any(
            alg == item for item in ["all", "modified_cosine", "ms2deepscore"]
        ):
            return False, "Not a valid algorithm choice"
        else:
            return True, ""

    @staticmethod
    def validate_range_zero_one(r: Tuple[float, float]) -> Tuple[bool, str]:
        """Validate input range.

        Args:
           r: tuple with two floats between and including 0-1.

        Returns:
           Tuple with outcome and (error) message
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
