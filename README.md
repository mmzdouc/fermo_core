fermo_core
=========

[![DOI](https://zenodo.org/badge/671395100.svg)](https://zenodo.org/doi/10.5281/zenodo.11259126) [![PyPI version](https://badge.fury.io/py/fermo_core.svg)](https://badge.fury.io/py/fermo_core)

`fermo_core` is a Python-based command line tool to process, analyze, and prioritize compounds from metabolomics data. While primarily intended to be the backend processing module of `fermo_gui` of the application FERMO, `fermo_core` can be used independently for large-scale data processing and analysis. 

This README specifies the use of `fermo_core` as command line interface. For a more user-friendly version, see the [FERMO online](https://fermo.bioinformatics.nl). Please also consult the [Documentation](https://mmzdouc.github.io/fermo_docs/).


Table of Contents
-----------------
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Attribution](#attribution)
- [Contributing](#contributing)

## Installation

### With `pip` from PyPI
- Install `python 3.11.x`
- Create a virtual environment (e.g. venv, conda) and activate it
- Run `pip install fermo_core`
- Once installed, run as specified in [Run with `pip`](#run-with-pip)

### With `hatch` from GitHub
- Install `python 3.11.x`
- Install hatch (e.g. with `pipx install hatch`)
- Download or clone the [repository](https://github.com/mmzdouc/fermo_core)
- (Change into the fermo_core base directory if not already present)
- Run `hatch -v env create`
- Once installed, run as specified in [Run with `hatch`](#run-with-hatch)

### With `conda` from GitHub
- Install conda (e.g. miniconda)
- Create a conda environment with `conda create --name fermo_core python=3.11`
- Activate the conda environment with `conda activate fermo_core`
- Download or clone the [repository](https://github.com/mmzdouc/fermo_core)
- (Change into the fermo_core base directory if not already present)
- Run `pip install -e .`
- Once installed, run as specified in [Run with `conda`](#run-with-conda)

## Quick Start

### Run with `pip`
- `fermo_core --parameters <your_parameter_file.json>`

### Run with `hatch`:
- `hatch run fermo_core --parameters <your_parameter_file.json>`

### Run with `conda`:
- `python fermo_core/main.py --parameters <your_parameter_file.json>`

## Usage

`fermo_core` can be used both as a command line interface as well as a library.

All parameters and input data are specified in a `parameters.json` file be formatted following the schema specified in `fermo_core/config/schema.json`. See the example in `example_data/case_study_parameters.json` and/or consult the [Documentation](https://mmzdouc.github.io/fermo_docs/home/core.parameters/).

As **minimum** data input, fermo_core` requires a pre-processed **peaktable** summarizing the detected molecular features (**no raw data**). This peaktable must:
- Derive from liquid chromatography electrospray ionization (tandem) mass spectrometry **(LC-ESI-(MS/)MS)**
- Constitute of samples acquired at identical **concentration/dilution** and identical **injection volume**
- Be acquired using **untargeted** Data-dependent acquisition **(DDA)**
- Be of high resolution (ideally, **<20 ppm** mass deviation)
- Be in a single polarity (either **positive** or **negative** ion mode)

Optionally (but recommended), `fermo_core` also accepts the following file types:
- Mass fragmentation **(MS/MS)** accompanying the peak table
- Metadata on **sample grouping**
- **Phenotype** (bioactivity) data associated with the samples
- A **spectral library**
- An [**MS2Query**](https://github.com/iomega/ms2query) results file
- An [**antiSMASH**](https://antismash.secondarymetabolites.org) results folder

For more information on input and output files, their format, and their purpose, consult the [Documentation](https://mmzdouc.github.io/fermo_docs/home/input_output/).

## Attribution

### License

`fermo_core` is an open source tool licensed under the MIT license (see [LICENSE](LICENSE.md)).

### Publications

See [FERMO online](https://fermo.bioinformatics.nl/) for information on citing `fermo_core`.

### Authors
Mitja M. Zdouc <zdoucmm@gmail.com>

## Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. Please see [Contributing](CONTRIBUTING.md) for more information on getting involved.
Contributors agree to adhere to the specified [Code of Conduct](CODE_OF_CONDUCT.md).
For technical details, see the For Developers pages in the [Documentation](https://mmzdouc.github.io/fermo_docs/for_devs/overview/).
