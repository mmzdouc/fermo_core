"""Organizes certain hardcoded default settings for easier access.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

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

import pandas as pd
from pydantic import BaseModel, DirectoryPath, FilePath, model_validator


class DefaultPaths(BaseModel):
    """A Pydantic-based class for storing shared hardcoded default settings.

    Attributes:
        dirpath_ms2deepscore_pos: points towards default ms2deepscore dir
        url_ms2deepscore_pos: the url to download the default ms2deepscore file
        dirpath_ms2query_base: points towards default ms2query dir
        dirpath_ms2query_pos: points towards default ms2query dir positive mode
        dirpath_ms2query_neg: points towards default ms2query dir negative mode
        url_ms2query_pos: urls to default ms2query files for positive ion mode
        url_ms2query_neg: urls to default ms2query files for negative ion mode
        dirpath_losses: point towards neutral loss dir
        dirpath_frags: point towards fragment dir
        library_mibig_pos: points towards mibig spectral library for positive ion mode
    """

    dirpath_ms2deepscore_pos: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2deepscore/pos"
    )
    url_ms2deepscore_pos: str = (
        "https://zenodo.org/records/8274763/files/"
        "ms2deepscore_positive_10k_1000_1000_1000_500.hdf5?download=1"
    )
    dirpath_ms2query_base: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2query/"
    )
    dirpath_ms2query_pos: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2query/pos"
    )
    dirpath_ms2query_neg: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2query/neg"
    )
    url_ms2query_pos: tuple = (
        "https://zenodo.org/records/10527997/files"
        "/ALL_GNPS_210409_positive_processed_annotated_CF_NPC_classes.txt?download=1",
        "https://zenodo.org/records/10527997/files"
        "/library_GNPS_15_12_2021_ms2ds_embeddings.parquet?download=1",
        "https://zenodo.org/records/10527997/files"
        "/library_GNPS_15_12_2021_s2v_embeddings.parquet?download=1",
        "https://zenodo.org/records/10527997/files/ms2ds_model_GNPS_15_12_2021.hdf5"
        "?download=1",
        "https://zenodo.org/records/10527997/files/ms2query_library.sqlite?download=1",
        "https://zenodo.org/records/10527997/files/ms2query_random_forest_model.onnx"
        "?download=1",
        "https://zenodo.org/records/10527997/files/spec2vec_model_GNPS_15_12_2021"
        ".model?download=1",
        "https://zenodo.org/records/10527997/files/spec2vec_model_GNPS_15_12_2021"
        ".model.syn1neg.npy?download=1",
        "https://zenodo.org/records/10527997/files/spec2vec_model_GNPS_15_12_2021"
        ".model.wv.vectors.npy?download=1",
    )
    url_ms2query_neg: tuple = (
        "https://zenodo.org/records/10528030/files/neg_GNPS_15_12_2021_ms2ds_model"
        ".hdf5?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_GNPS_15_12_2021_ms2query_random_forest_model.onnx?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_mode_GNPS_15_12_2021_ms2ds_embeddings.parquet?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_mode_GNPS_15_12_2021_s2v_embeddings.parquet?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_mode_spec2vec_model_GNPS_15_12_2021.model?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_mode_spec2vec_model_GNPS_15_12_2021.model.syn1neg.npy?download=1",
        "https://zenodo.org/records/10528030/files"
        "/neg_mode_spec2vec_model_GNPS_15_12_2021.model.wv.vectors.npy?download=1",
        "https://zenodo.org/records/10528030/files/negative_mode_15_12_2021.sqlite"
        "?download=1",
    )
    dirpath_losses: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/loss_libs/"
    )
    dirpath_frags: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/frag_libs/"
    )
    library_mibig_pos: FilePath = Path(__file__).parent.parent.joinpath(
        "libraries/mibig/pos/mibig_in_silico_spectral_library_3_1.mgf"
    )


class DefaultMasses(BaseModel):
    """A Pydantic-based class for storing atom and ion masses for adduct annotation

    Sources:
        https://fiehnlab.ucdavis.edu/staff/kind/Metabolomics/MS-Adduct-Calculator/
        https://media.iupac.org/publications/pac/2003/pdf/7506x0683.pdf
        https://pubchem.ncbi.nlm.nih.gov/compound/Bicarbonate-Ion
        https://pubchem.ncbi.nlm.nih.gov/compound/Water

    Attributes:
        Na: sodium monoisotopic mass
        H: proton monoisotopic mass
        C13_12: mass difference between 13C and 12C isotopes
        Fe56: monoisotopic mass of 56Fe
        NH4: monoisotopic mass ammonium
        K: monoisotopic mass potassium
        H2O: monoisotopic mass water
        Cl35: monoisotopic mass of 35Cl
        HCO2: monoisotopic mass of bicarbonate anion
        TFA: monoisotopic mass of trifluoroacetic acid anion
        Ac: monoisotopicmass of acetic acid anion
    """

    Na: float = 22.989218
    H: float = 1.007276
    C13_12: float = 1.0033548
    Fe56: float = 55.934941
    NH4: float = 18.033823
    K: float = 38.963158
    H2O: float = 18.010565
    Cl35: float = 34.969402
    HCO2: float = 60.992568
    TFA: float = 112.985586
    Ac: float = 59.013851


class Loss(BaseModel):
    """A Pydantic-based class for storing information on neutral losses

    Attributes:
        loss: the neutral loss in Da
        descr: the neutral loss description
        abbr: the neutral loss abbreviation
    """

    loss: float
    descr: str
    abbr: str


class NeutralLosses(BaseModel):
    """A Pydantic-based class for storing monoisotopic masses of neutral losses in MS2

    Sources:
        Kersten et al 2011 (doi.org/10.1038/nchembio.684)

        Kersten et al 2013 (doi.org/10.1073/pnas.1315492110)

        Interpretation of MS-MS Mass Spectra of Drugs and Pesticides, Niessen,
        Correa 2017 (ISBN 9781119294245)

    Attributes:
        ribosomal_src: path to the file location
        ribosomal: neutral losses derived from ribosomal peptides, positive mode
        nonribo_src: path to the file location
        nonribo: neutral losses derived from nonribosomal peptides, positive mode
        glycoside_src: path to the file location
        glycoside: neutral losses derived from glycosides, positive mode
        gen_bio_pos_src: path to file location
        gen_bio_pos: generic neutral losses from metabolites, positive mode
        gen_other_pos_src: path to file location
        gen_other_pos: generic neutral losses (metabolite+synthetics), positive mode
        gen_other_neg_src: path to file location
        gen_other_neg: generic neutral losses (metabolite+synthetics), negative mode
    """

    ribosomal_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "kersten_ribosomal.csv"
    )
    ribosomal: list[Loss] = []
    nonribo_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "kersten_nonribosomal.csv"
    )
    nonribo: list[Loss] = []
    glycoside_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "kersten_glycosides.csv"
    )
    glycoside: list[Loss] = []
    gen_bio_pos_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "generic_bio_pos.csv"
    )
    gen_bio_pos: list[Loss] = []
    gen_other_pos_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "generic_other_pos.csv"
    )
    gen_other_pos: list[Loss] = []
    gen_other_neg_src: FilePath = DefaultPaths().dirpath_losses.joinpath(
        "generic_other_neg.csv"
    )
    gen_other_neg: list[Loss] = []

    @model_validator(mode="after")
    def read_files(self):
        df = pd.read_csv(self.ribosomal_src)
        for _, row in df.iterrows():
            self.ribosomal.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        df = pd.read_csv(self.nonribo_src)
        for _, row in df.iterrows():
            self.nonribo.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        df = pd.read_csv(self.glycoside_src)
        for _, row in df.iterrows():
            self.glycoside.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        df = pd.read_csv(self.gen_bio_pos_src)
        for _, row in df.iterrows():
            self.gen_bio_pos.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        df = pd.read_csv(self.gen_other_pos_src)
        for _, row in df.iterrows():
            self.gen_other_pos.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        df = pd.read_csv(self.gen_other_neg_src)
        for _, row in df.iterrows():
            self.gen_other_neg.append(
                Loss(loss=row["loss"], descr=row["descr"], abbr=row["abbr"])
            )

        return self


class Fragment(BaseModel):
    """A Pydantic-based class for storing information on characteristic fragments

    Attributes:
        mass: the m/z value of the fragment
        descr: the neutral loss description
    """

    mass: float
    descr: str


class CharFragments(BaseModel):
    """A Pydantic-based class for storing characteristic ion fragment masses

    Attributes:
        aa_frags_src: path to the file location
        aa_frags: b2 and y2 series of (proteinogenic) amino acids
    """

    aa_frags_src: FilePath = DefaultPaths().dirpath_frags.joinpath(
        "aa_m+h_fragment_series.csv"
    )
    aa_frags: list[Fragment] = []

    @model_validator(mode="after")
    def read_files(self):
        df = pd.read_csv(self.aa_frags_src)
        for _, row in df.iterrows():
            self.aa_frags.append(
                Fragment(
                    mass=row["y2"],
                    descr=f"{row['pair']}(y2, [M+H]+)",
                )
            )
            self.aa_frags.append(
                Fragment(
                    mass=row["b2"],
                    descr=f"{row['pair']}(b2, [M+H]+)",
                )
            )
        return self
