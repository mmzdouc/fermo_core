"""Organizes certain hardcoded default settings for easier access.

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

from typing import List, Optional
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, DirectoryPath, model_validator, FilePath


class DefaultPaths(BaseModel):
    """A Pydantic-based class for storing shared hardcoded default settings.

    Attributes:
        dirpath_ms2deepscore: points towards default ms2deepscore dir
        filename_ms2deepscore: points towards default ms2deepscore dir
        url_ms2deepscore: the url to download the default ms2deepscore file
        dirpath_ms2query: points towards default ms2query dir
        url_ms2query_pos: urls to default ms2query files for positive ion mode
        url_ms2query_neg: urls to default ms2query files for negative ion mode
    """

    dirpath_ms2deepscore: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2deepscore"
    )
    filename_ms2deepscore: str = "ms2deepscore_positive_10k_1000_1000_1000_500.hdf5"
    url_ms2deepscore: str = (
        "https://zenodo.org/records/8274763/files/"
        "ms2deepscore_positive_10k_1000_1000_1000_500.hdf5?download=1"
    )
    dirpath_ms2query: DirectoryPath = Path(__file__).parent.parent.joinpath(
        "libraries/ms2query"
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


class DefaultMasses(BaseModel):
    """A Pydantic-based class for storing atom and ion masses for adduct annotation

    Sources:
        https://fiehnlab.ucdavis.edu/staff/kind/Metabolomics/MS-Adduct-Calculator/
        https://media.iupac.org/publications/pac/2003/pdf/7506x0683.pdf

    Attributes:
        Na: sodium monoisotopic mass
        H: proton monoisotopic mass
        C13_12: mass difference between 13C and 12C isotopes
        Fe56: monoisotopic mass of 56Fe
        NH4: monoisotopic mass ammonium
        K: monoisotopic mass potassium
        H2O: monoisotopic mass water
    """

    Na: float = 22.989218
    H: float = 1.007276
    C13_12: float = 1.0033548
    Fe56: float = 55.934941
    NH4: float = 18.033823
    K: float = 38.963158
    H2O: float = 18.011114


class Loss(BaseModel):
    """A Pydantic-based class for storing information on neutral losses

    Attributes:
        id: the identifier/description
        mass: the neutral loss in Da
        ribo_tag: the ribosomal amino acids the loss derives from, single letter code
        nribo_tag: the non-ribosomal amino acid tag (NORINE-code)
        nribo_mon: putative monomer the non-ribosomal AA derives from
    """

    id: str
    mass: float
    ribo_tag: Optional[str] = None
    nribo_tag: Optional[str] = None
    nribo_mon: Optional[str] = None


class NeutralMasses(BaseModel):
    """A Pydantic-based class for storing monoisotopic masses of neutral losses in MS2

    Sources:
        Kersten et al 2011 (doi.org/10.1038/nchembio.684)

        Interpretation of MS-MS Mass Spectra of Drugs and Pesticides, Niessen,
        Correa 2017 (ISBN 9781119294245)

    Attributes:
        ribosomal_src: the path to the file location
        ribosomal: a list of Loss objects derived from a ribosomal peptide
        nonribo_src: the path to the file location
        nonribo: a list of Loss objects derived from a nonribosomal peptide
    """

    ribosomal_src: FilePath = Path(__file__).parent.joinpath("kersten_ribosomal.csv")
    ribosomal: List[Loss] = []
    nonribo_src: FilePath = Path(__file__).parent.joinpath("kersten_nonribosomal.csv")
    nonribo: List[Loss] = []

    @model_validator(mode="after")
    def read_files(self):
        df_rib = pd.read_csv(self.ribosomal_src)
        for _, row in df_rib.iterrows():
            self.ribosomal.append(
                Loss(
                    id=row["description"],
                    mass=row["loss"],
                    ribo_tag=row["tag"],
                )
            )
        df_nonrib = pd.read_csv(self.nonribo_src)
        for _, row in df_nonrib.iterrows():
            self.nonribo.append(
                Loss(
                    id=row["description"],
                    mass=row["loss"],
                    nribo_tag=row["tag"],
                    nribo_mon=row["monomer"],
                )
            )
        return self
