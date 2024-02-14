"""Processes a folder of all MIBiG entries and outputs 2 space delimited .csv files.
"""

# import pathlib
import json

# import pandas as pd


class ParseMibigEntries:
    """
    Class that parses the MIBiG .json files and outputs 2 space delimited .csv files.

    Attributes:
        mibig_folder: Path of the mibig.json folder containing .json files.
        prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        bgc_file: Path of a .json file containing the information on a single BCG cluster from MIBiG database.
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
        # Will later make method to handle file delivery to extract_metadata
        self.bgc_file = "test.json"
        self.bgc_dict = {}

    def extract_metadata(self):
        """Extracts the relevant metadata from a .json file and
        adds a new entry to bgc_dict for every metabolite found.

        Attributes:
            self.bgc_file: Path of a .json file containing the information on a single BCG cluster from MIBiG database.
            self.bgc_dict: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
             chemical formula, molecular mass, database IDs, MIBiG entry ID.

        Raises:
            KeyError: If .json file doesn't contain either a metabolite name or SMILES.
        """

        with open(self.bgc_file) as file:
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
                except KeyError():
                    print("No metabolite name found for " + metadata_table[5] + " !")
                try:
                    metadata_table[1] = metabolite["chem_struct"]
                except KeyError():
                    print("No SMILES found for " + metadata_table[5] + " !")
                metadata_table[2] = metabolite["molecular_formula"]
                metadata_table[3] = metabolite["mol_mass"]
                metadata_table[4] = metabolite["database_id"]
                self.bgc_dict[metadata_table[0]] = [
                    metadata_table[1],
                    metadata_table[2],
                    metadata_table[3],
                    metadata_table[4],
                    metadata_table[5],
                ]


# Testing
testje = ParseMibigEntries("1", "1", "1")
testje.extract_metadata()
print(testje.bgc_dict)
