Repo for the processing part of FERMO (fermo_core)


Download, Installation
============

- Create a virtual environment (e.g. with `conda`)
- Install `python 3.11.4`
- Install `fermo_core` with `pip install -e .` (while in the `fermo_core` directory)

Usage
=====

While fermo_core is primarily intended to be the backend processing of fermo_gui, it
can be run as a command line tool. This is mainly oriented towards computationally
experienced users. Run `fermo_core` with:

`python fermo_core/main.py --parameters <your_parameter_file.json>`

Here, the parameter file is a specifically formatted json file, containing
user-provided parameters and settings. The schema for the json file can be found in
`fermo_core/config/schema.json` and an example file can be found in
`example_data/case_study_parameters.json`.

Data Compatibility
=====

Input data for fermo_core processing **MUST** be:
- Liquid chromatography electrospray ionization mass spectrometry data (LC-ESI-MS)
- Pre-processed by a pre-processing tool (see section `Compatibility`)
- In a single polarity (either `positive` or `negative` ion mode)
- Data-dependent acquisition.

Further, data for fermo_core processing is **PREFERABLY**:
- Mass spectrometry (MS1) data interlaced with tandem mass spectrometry (MS/MS)
  scans
- High resolution (< 20 ppm mass deviation)
- Acquired on a reverse-phase chromatography gradient


Background
==========

TBA

For developers
==============

For guidelines regarding contributing to this project, see
[CONTRIBUTING](CONTRIBUTING.md).

Install development dependencies with `pip install -e '.[dev]'`.

Several tools are used to keep code and style consistent.
These tools include:
- `black` (v23.3.0)
- `flake8` (v6.0.0)

We recommend using the package `pre-commit` to run these tools before committing.
`pre-commit` can be installed with `pre-commit install`.

Besides, we use type hinting and document code using Google-style docstrings.
A convenient tool to check documentation style is `pycodestyle`.

We use [Semantic Versioning](http://semver.org/) for versioning.

Slow-running unit tests can be conditionally disabled using the decorator
`@pytest.mark.slow`. To also run slow tests, use `pytest --runslow`. `Pre-commit`
also runs all tests.

About
=====

## Dependencies

A list of dependencies can be found in the file [pyproject.toml](pyproject.toml).

## License

MIT license (see [LICENSE](LICENSE.md))

Authors
=======

- Mitja M. Zdouc (Wageningen University)
