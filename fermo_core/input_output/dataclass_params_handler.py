"""Hold parameters for downstream data processing and analysis.

Interface to collect and hold user input from both command line and GUI.

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
    """Handle parameters for processing by fermo_core.

    Handle input from both graphical user interface and command line,
    well as default values, for downstream processing.

    Attribute syntax: if multiple competing input styles for one input file
    type exists, they should be called with the same prefix (e.g. peaktable_fermo,
    (hypothetical) peaktable_openms)

    Attributes:
        version: Current program version.
        root: "Root" directory of program.
        session: Fermo json session file.
        peaktable_mzmine3: Mzmine3-style peaktable.
        msms_mgf: Mgf-style msms file.
        phenotype_fermo: Fermo-style phenotypic data file.
        phenotype_fermo_mode: Specifies mode of file phenotype_fermo (concentration or
            percent)
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
        self.session: Path | None = None
        self.peaktable_mzmine3: Path | None = None
        self.msms_mgf: Path | None = None
        self.phenotype_fermo: Path | None = None
        self.phenotype_fermo_mode: str | None = None
        self.group_fermo: Path | None = None
        self.speclib_mgf: Path | None = None
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
