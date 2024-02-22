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
from typing import Self, List, Dict, Optional

from pydantic import BaseModel


class AddMibigMetadata(BaseModel):
    """Adds real mass, publication IDs and MIBiG cluster IDs to CFM-ID output.

    Attributes:
        output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per metabolite
        prepped_metadata_file: Path of output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        log_files: Table of file paths of the CFM-ID log files output
        metadata: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
             chemical formula, molecular mass, database IDs, MIBiG entry ID.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    output_folder: str
    prepped_metadata_file: str
    log_files: Optional[List] = []
    metadata: Optional[Dict] = {}

    def extract_filenames(self: Self):
        """Extracts the filenames of all .log files from a folder and adds them to self.log_files"""
        folder = Path(self.output_folder)
        for item in folder.iterdir():
            if item.is_dir():
                pass
            else:
                if item.suffix == ".log":
                    self.log_files.append(str(item))

    def extract_metadata(self: Self):
        """Extracts the relevant metadata from the metadata .csv file and
        adds a new entry to self_metadata for every metabolite found.
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

    def add_metadata_cfmid_files(self: Self):
        """Adds the missing metadata to all files in the CFM-ID output folder"""

        for filename in self.log_files:
            with open(filename, "r") as file:
                lines = file.readlines()
                for linenr in range(len(lines)):
                    if lines[linenr].startswith("#RealMass"):
                        print(
                            "File "
                            + filename
                            + " already contains metadata, exiting now."
                        )
                        exit()
                    if lines[linenr].startswith("#PMass"):
                        lines[linenr] = (
                            lines[linenr]
                            + "#RealMass="
                            + self.metadata[
                                filename.strip(".log")
                                .strip(self.output_folder)
                                .strip("\\")
                                .strip("/")
                            ][2]
                            + "\n#Publications="
                            + self.metadata[
                                filename.strip(".log")
                                .strip(self.output_folder)
                                .strip("\\")
                                .strip("/")
                            ][3]
                            + "\n#MibigAccession="
                            + self.metadata[
                                filename.strip(".log")
                                .strip(self.output_folder)
                                .strip("\\")
                                .strip("/")
                            ][4]
                            + "\n"
                        )
            with open(filename, "w") as file:
                for line in lines:
                    file.write(line)
