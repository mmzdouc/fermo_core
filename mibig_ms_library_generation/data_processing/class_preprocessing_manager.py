"""Processes a folder of all MIBiG entries and outputs 2 space delimited .csv files.

Copyright (c) 2022 to present Koen van Ingen, Mitja M. Zdouc, PhD and individual contributors.

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
from typing import Self, Dict, Optional

import pandas as pd
from pydantic import BaseModel


class PreprocessingManager(BaseModel):
    """
    Class that parses the MIBiG .json files and outputs 2 space delimited .csv files.

    Attributes:
        prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        bgc_dict: Dictionary with metabolite_name as key and metadata in a list as values: SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.

    """

    prepped_cfmid_file: str
    prepped_metadata_file: str
    bgc_dict: Optional[Dict] = {}

    def extract_metadata(self: Self, file_path: str):
        """Extracts the relevant metadata from a .json file and
        adds a new entry to bgc_dict for every metabolite found.
        """

        with open(file_path) as file:
            complete_bgc_dict = json.load(file)
            for metabolite in complete_bgc_dict["cluster"]["compounds"]:
                if "compound" in metabolite.keys():
                    metadata_table = [metabolite["compound"]]
                else:
                    break
                if "chem_struct" in metabolite.keys():
                    metadata_table.append(metabolite["chem_struct"])
                else:
                    break
                if "molecular_formula" in metabolite.keys():
                    metadata_table.append(metabolite["molecular_formula"])
                else:
                    metadata_table.append("")
                if "mol_mass" in metabolite.keys():
                    metadata_table.append(metabolite["mol_mass"])
                else:
                    metadata_table.append("")
                if "database_id" in metabolite.keys():
                    metadata_table.append(
                        str(metabolite["database_id"]).replace(" ", "")
                    )
                else:
                    metadata_table.append("")
                if metabolite["compound"] in self.bgc_dict.keys():
                    metadata_table.append(
                        complete_bgc_dict["cluster"]["mibig_accession"]
                        + ","
                        + self.bgc_dict[metabolite["compound"]][4]
                    )

                else:
                    metadata_table.append(
                        complete_bgc_dict["cluster"]["mibig_accession"]
                    )
                self.bgc_dict[metadata_table[0]] = [
                    metadata_table[1],
                    metadata_table[2],
                    metadata_table[3],
                    metadata_table[4],
                    metadata_table[5],
                ]

    @staticmethod
    def extract_filenames(folder_path, extension):
        """Extracts the filenames of all files from a certain extension in a folder and returns them in a list

        Attributes:
            folder_path: Path to the folder containing the files.
            extension: File extension in str format like ".str"

        Returns:
            files_list: List of all file paths in the folder meeting the extension criteria
        """
        files_list = []
        folder = Path(folder_path)
        for item in folder.iterdir():
            if not item.is_dir() and item.suffix == extension:
                files_list.append(str(item))
        return files_list

    def write_outfiles(self: Self):
        """Uses pandas to write space delimited .csv style files from the MIBiG data"""
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
