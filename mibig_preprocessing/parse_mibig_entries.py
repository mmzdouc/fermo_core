"""Processes a folder of all MIBiG entries and outputs 2 space delimited .csv files.
"""

from pathlib import Path
import json
from sys import argv
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
        # Will later make method to handle file delivery to extract_metadata
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

    def cleanup_output(self):
        """Removes double quotes from output files of pandas

        Attributes:
            self.prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
            self.prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
            molecular mass, database IDs, MIBiG entry ID.
        """
        with open(self.prepped_cfmid_file, "r+") as file:
            text = file.read().replace('"', "")
            file.truncate(0)
            file.seek(0)
            file.write(text)
        with open(self.prepped_metadata_file, "r+") as file:
            text = file.read().replace('"', "")
            file.truncate(0)
            file.seek(0)
            file.write(text)

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
        """Uses pandas to write space delimited .csv files from the MIBiG data

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
                "chemical formula",
                "molecular mass",
                "database IDs",
                "MIBiG entry ID",
            ],
        )
        metadataframe = metadataframe.T
        metadataframe.to_csv(
            self.prepped_metadata_file, sep=" ", index_label="metabolite name"
        )
        metadataframe[["SMILES"]].to_csv(self.prepped_cfmid_file, sep=" ", header=False)


# testing
if __name__ == "__main__":
    testje = ParseMibigEntries(argv[1], "cfm_id_input.csv", "metadata.csv")
    testje.extract_filenames()
    for path_file in testje.bgc_files:
        testje.extract_metadata(path_file)
    # testje.cleanup_dictionary()
    # print(testje.bgc_files)
    # testje.extract_metadata()
    print(testje.bgc_dict)
    testje.write_outfiles()
    testje.cleanup_output()
