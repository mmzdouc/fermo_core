"""Processes a folder of all MIBiG entries and outputs 2 space delimited .csv files.

Copyright (c) 2022 to present Mitja M. Zdouc, PhD and individual contributors.

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
import json
import pandas as pd


class ParseMibigEntries:
    """
    Class that parses the MIBiG .json files and outputs 2 space delimited .csv files.

    Attributes:
        mibig_folder: Path of the mibig.json folder containing .json files.
        prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        bgc_files: A list containing all file paths of the MIBiG entries .json files
        bgc_dict: Dictionary with metabolite_name as key and metadata in a list as values: SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
    """

    def __init__(
        self,
        mibig_folder: str,
        prepped_cfmid_file: str,
        prepped_metadata_file: str,
    ):
        self.mibig_folder = mibig_folder
        self.prepped_cfmid_file = prepped_cfmid_file
        self.prepped_metadata_file = prepped_metadata_file
        self.bgc_files = []
        self.bgc_dict = {}

    def extract_metadata(self, file_path):
        """Extracts the relevant metadata from a .json file and
        adds a new entry to bgc_dict for every metabolite found.

        Attributes:
            file_path: Path of a .json file containing the information on a single BCG cluster from MIBiG database.
            self.bgc_dict: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
             chemical formula, molecular mass, database IDs, MIBiG entry ID.

        Raises:
            KeyError: If .json file doesn't contain either a metabolite name or SMILES.
        """

        with open(file_path) as file:
            complete_bgc_dict = json.load(file)
            metadata_table = [
                None,
                None,
                None,
                None,
                None,
                complete_bgc_dict["cluster"]["mibig_accession"],
            ]
            for metabolite in complete_bgc_dict["cluster"]["compounds"]:
                try:
                    metadata_table[0] = metabolite["compound"]
                except KeyError as e:
                    print("Keyerror:", e, "No metabolite name found in file", file_path)
                    exit()
                try:
                    metadata_table[1] = metabolite["chem_struct"]
                except KeyError as e:
                    print("Keyerror:", e, "No SMILES found in file", file_path)
                    exit()
                try:
                    metadata_table[2] = metabolite["molecular_formula"]
                except KeyError:
                    metadata_table[2] = ""
                try:
                    metadata_table[3] = metabolite["mol_mass"]
                except KeyError:
                    metadata_table[3] = ""
                try:
                    metadata_table[4] = metabolite["database_id"]
                except KeyError:
                    metadata_table[4] = ""
                self.bgc_dict[metadata_table[0]] = [
                    metadata_table[1],
                    metadata_table[2],
                    metadata_table[3],
                    metadata_table[4],
                    metadata_table[5],
                ]

    def extract_filenames(self):
        """Extracts the filenames of all .json files from a folder and adds them to self.bcg_files

        Attributes:
            self.mibig_folder: Path of the mibig.json folder containing .json files.
            self.bcg_files: A list containing all file paths of the MIBiG entries .json files
        """
        folder = Path(self.mibig_folder)
        for item in folder.iterdir():
            if item.is_dir():
                pass
            else:
                if item.suffix == ".json":
                    self.bgc_files.append(str(item))

    def write_outfiles(self):
        """Uses pandas to write space delimited .csv style files from the MIBiG data

        Attributes:
            self.prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
            self.prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
            molecular mass, database IDs, MIBiG entry ID.
            self.bgc_dict: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
            chemical formula, molecular mass, database IDs, MIBiG entry ID.
        """
        metadataframe = pd.DataFrame(
            self.bgc_dict,
            index=[
                "SMILES",
                "chemical_formula",
                "molecular_mass",
                "database_IDs",
                "MIBiG_entry_ID",
            ],
        )
        columns = metadataframe.columns.str.replace(" ", "_", regex=True)
        metadataframe.columns = columns
        metadataframe = metadataframe.T
        metadataframe.to_csv(
            self.prepped_metadata_file, sep=" ", index_label="metabolite_name"
        )
        metadataframe[["SMILES"]].to_csv(self.prepped_cfmid_file, sep=" ", header=False)
