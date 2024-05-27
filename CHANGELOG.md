# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased

N/A

## [0.2.1] 27-05-2024

### Changed

- Removed 'phenotypes' as separate Feature attribute: write to Annotation object instead.
- Implemented sorting of annotation entries in descending order

## [0.2.1] 26-05-2024

### Fixed

- Fixed bug in "SummaryWriter": implemented error catching.

## [0.2.0] 26-05-2024

### Changed

- Replaced global logger with logger specific for `main_cli()`. `main()` now needs an argument `logger`
- Reworked output file naming: all output files now start with `out.fermo.` and a suffix specifying their type
- Removed output directory selection: the output directory is now always `results` located in the directory in which the peaktable resides.
- Features now always have default result values (before, some Features could have an empty dictionary)
- MS2Query assignment now uses temporary directories for data reading/writing

### Fixed

- Removed `sys.exit(0)` in case of successful run to fix compatibility issue with Celery task manager (`fermo_gui`)

## [0.1.1] 24-05-2024

### Changed

- Implemented logging verboseness parameter for CLI interface

## [0.1.0] 19-05-2024

First public release of `fermo_core`