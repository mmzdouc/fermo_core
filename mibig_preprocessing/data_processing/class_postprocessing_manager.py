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


class PostprocessingManager(BaseModel):
    """Adds real mass, publication IDs and MIBiG cluster IDs to CFM-ID output.

    Attributes:
        output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per metabolite
        prepped_metadata_file: Path of parsing_manager output file containing metabolite name, SMILES, chemical formula,
        molecular mass, database IDs, MIBiG entry ID.
        log_files: Table of file paths of the CFM-ID log files output
        metadata: Dictionary with metabolite_name as key and metadata in a list as values: SMILES,
             chemical formula, molecular mass, database IDs, MIBiG entry ID.
        log_dict: Dictionary with metabolite_name as key and with value a list of .log file lines, now with metadata.
        preprocessed_mgf_list: A triple nested list containing the data on file, lines and different columns within
        those lines respectively.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
    """

    output_folder: str
    prepped_metadata_file: str
    # mgf_file: str
    log_files: Optional[List] = []
    metadata: Optional[Dict] = {}
    log_dict: Optional[Dict] = {}
    preprocessed_mgf_list: Optional[List] = []

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
        """Adds the missing metadata to all files in the CFM-ID output folder and saves result in mgf_dict."""
        for filename in self.log_files:
            with open(filename, "r") as file:
                lines = file.readlines()
                for linenr in range(len(lines)):
                    if lines[linenr].startswith("#PMass"):
                        lines = (
                            lines[0 : linenr + 1]
                            + [
                                "PUBLICATIONS="
                                + self.metadata[
                                    filename.strip(".log")
                                    .strip(self.output_folder)
                                    .strip("\\")
                                    .strip("/")
                                ][3]
                                + "\n",
                                "MIBIGACCESSION="
                                + self.metadata[
                                    filename.strip(".log")
                                    .strip(self.output_folder)
                                    .strip("\\")
                                    .strip("/")
                                ][4]
                                + "\n",
                            ]
                            + lines[linenr + 2 :]
                        )

                        break
            self.log_dict[
                filename.strip(".log").strip(self.output_folder).strip("\\").strip("/")
            ] = lines

    def cleanup_log_dict(self: Self):
        """Formats the .log files in log_dict to an .mgf like format in preprocessed_mgf_list."""
        for metabolite, lines in self.log_dict.items():
            for linenr in range(len(lines)):
                if lines[linenr].startswith("0 "):
                    lines = lines[0 : linenr - 1]
                    break
            for linenr in range(len(lines)):
                if lines[linenr].startswith("energy1"):
                    lines = lines[0:linenr] + lines[linenr + 1 :]
                    break
            for linenr in range(len(lines)):
                if lines[linenr].startswith("energy2"):
                    lines = lines[0:linenr] + lines[linenr + 1 :]
                    break
            for linenr in range(len(lines)):
                if lines[linenr].startswith("#In-silico"):
                    lines[linenr] = "INSILICO=" + lines[linenr][10:].replace(" ", "")
                if lines[linenr].startswith("#PREDICTED BY"):
                    lines[linenr] = "PREDICTEDBY=" + lines[linenr][13:].replace(" ", "")
                if lines[linenr].startswith("#ID="):
                    lines[linenr] = "ID=" + lines[linenr][4:].replace(" ", "")
                if lines[linenr].startswith("#SMILES="):
                    lines[linenr] = "SMILES=" + lines[linenr][8:].replace(" ", "")
                if lines[linenr].startswith("#InChiKey="):
                    lines[linenr] = "INCHIKEY=" + lines[linenr][10:].replace(" ", "")
                if lines[linenr].startswith("#Formula="):
                    lines[linenr] = "FORMULA=" + lines[linenr][9:].replace(" ", "")
                if lines[linenr].startswith("#PMass="):
                    lines[linenr] = "PMass=" + lines[linenr][7:].replace(" ", "")
            entry_list = []
            for line in lines:
                entries = line.replace("\n", "").split(" ")
                entry_list.append(entries)
            self.preprocessed_mgf_list.append(entry_list)
