"""Drives the different classes of the MIBiG spectral library pipeline

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

from parse_mibig_entries import ParseMibigEntries
from run_cfmid import RunCfmid
from sys import argv


class LibraryPrep:
    """Class that manages the other MIBiG spectral library classes.

    Attributes:
        mibig_folder: Path of the mibig.json folder containing .json files.
        prepped_cfmid_file: Path of output file containing metabolite name, SMILES.
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per
        metabolite.
        prune_probability: Probability below which metabolite fragments will be excluded from predictions.
    """

    def __init__(
        self,
        mibig_folder: str,
        prepped_cfmid_file: str,
        prepped_metadata_file: str,
        output_folder: str,
        prune_probability: str,
    ):
        self.mibig_folder = mibig_folder
        self.prepped_cfmid_file = prepped_cfmid_file
        self.prepped_metadata_file = prepped_metadata_file
        self.output_folder = output_folder
        self.prune_probability = prune_probability

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

    def run_cfmid(self):
        """Builds and executes the command to run CFM-ID in dockerized environment using nice -16

        Attributes:
            self.prepped_cfmid_file: Path of input file containing metabolite name, SMILES.
            self.output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per
            metabolite.
            self.prune_probability: Probability below which metabolite fragments will be excluded from predictions.
        """
        spectra = RunCfmid(
            self.prepped_cfmid_file, self.output_folder, self.prune_probability
        )
        spectra.run_program()


# Will later do better and flexible input handling using argparse
if __name__ == "__main__":
    data = LibraryPrep(argv[1], argv[2], argv[3], argv[4], argv[5])
    data.process_mibig()
    data.run_cfmid()
