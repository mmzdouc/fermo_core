"""Runs the program CFM-ID in a dockerized environment

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

from subprocess import run


class RunCfmid:
    """Class that runs the program CFM-ID in a dockerized environment

    Attributes:
        prepped_cfmid_file: Path of input file containing metabolite name, SMILES.
        output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per metabolite
        prune_probability: Probability below which metabolite fragments will be excluded from predictions
    """

    def __init__(
        self,
        prepped_cfmid_file: str,
        output_folder: str,
        prune_probability: str,
    ):
        self.prepped_cfmid_file = prepped_cfmid_file
        self.output_folder = output_folder
        self.prune_probability = prune_probability

    def run_program(self):
        """Builds and executes the command to run CFM-ID in dockerized environment using nice -16

        Attributes:
            self.prepped_cfmid_file: Path of input file containing metabolite name, SMILES.
            self.output_folder: Path of cfm-id output folder where it will create 1 fragmentation spectrum file per
            metabolite.
            self.prune_probability: Probability below which metabolite fragments will be excluded from predictions.
        """
        command = (
            "nice -16 docker run --rm=true -v $(pwd):/cfmid/public/ -i wishartlab/cfmid:latest "
            + 'sh -c "cd /cfmid/public/; cfm-predict '
            + self.prepped_cfmid_file
            + " "
            + self.prune_probability
            + " "
            + "/trained_models_cfmid4.0/[M+H]+/param_output.log "
            + "/trained_models_cfmid4.0/[M+H]+/param_config.txt 1 "
            + self.output_folder
            + '"'
        )
        run(command, shell=True, executable="/bin/bash")