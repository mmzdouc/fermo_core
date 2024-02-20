"""Adds real mass, database IDs and MIBiG cluster IDs to CFM-ID output.

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


class AddMibigMetadata:
    """Adds real mass, database IDs and MIBiG cluster IDs to CFM-ID output.

    Attributes:
        output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per metabolite
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.

    """

    def __init__(
        self,
        output_folder: str,
        prepped_metadata_file: str,
    ):
        self.output_folder = output_folder
        self.prepped_metadata_file = prepped_metadata_file
        self.log_files = []
        self.metadata = {}

    def extract_filenames(self):
        """Extracts the filenames of all .log files from a folder and adds them to self.bcg_files

        Attributes:
            self.output_folder: Path of the CFM-ID output folder containing the spectral library
            self.log_files: A list containing all file paths of the CFM-ID output spectra
        """
        folder = Path(self.output_folder)
        for item in folder.iterdir():
            if item.is_dir():
                pass
            else:
                if item.suffix == ".log":
                    self.log_files.append(str(item))

    def extract_metadata(self):
        """Extracts the relevant metadata from the metadata .csv file and
        adds a new entry to self_metadata for every metabolite found.

        Attributes:
            self.prepped_metadata_file: Path of the .csv file containing the metadata
            self.metadata: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
             chemical formula, molecular mass, database IDs, MIBiG entry ID.
        """
        with open(self.prepped_metadata_file, "r") as file:
            for line in file:
                metadata_table = line.strip("\n").split(" ")
                self.metadata[metadata_table[0]] = [
                    metadata_table[1],
                    metadata_table[2],
                    metadata_table[3],
                    metadata_table[4],
                    metadata_table[5],
                ]


if __name__ == "__main__":
    metadata = AddMibigMetadata("s_output", "s_meta.csv")
    metadata.extract_filenames()
    metadata.extract_metadata()
