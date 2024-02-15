"""Drives the different classes of the MIBiG spectral library pipeline
"""

from parse_mibig_entries import ParseMibigEntries
from sys import argv


class LibraryPrep:
    """Class that manages the other MIBiG spectral library classes.

    Attributes:
        mibig_folder: Path of the mibig.json folder containing .json files.
        prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
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

    def process_mibig(self):
        """Processes the .json files from MIBiG into input for CFM-ID and metadata file.

        Attributes:
            self.mibig_folder: Path of the mibig.json folder containing .json files.
            self.prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
            self.prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
            molecular mass, database IDs, MIBiG entry ID.
        """
        preprocessed_data = ParseMibigEntries(
            self.mibig_folder, self.prepped_cfmid_file, self.prepped_metadata_file
        )
        preprocessed_data.extract_filenames()
        for file_path in preprocessed_data.bgc_files:
            preprocessed_data.extract_metadata(file_path)
        preprocessed_data.write_outfiles()
        """ This step should probably take place after CFMID processing
        preprocessed_data.cleanup_output()"""


# Will later do better and flexible input handling using argparse
if __name__ == "__main__":
    data = LibraryPrep(argv[1], argv[2], argv[3])
    data.process_mibig()
