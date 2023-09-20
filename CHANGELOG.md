# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] 20-09-2023

### Added

- Command line interface: allows to run FERMO via command line without GUI.

### Modified

- MS/MS data is not mandatory anymore. However, this disables certain functionality
  (e.g. MS2Query annotation)
- Group metadata: each sample can be part of an arbitrary number of groups. The
  following group names are still reserved: 'BLANK' (annotation of sample-blank
  associated feature), 'DEFAULT' (reserved for internal use)
- Phenotype/bioactivity data: in the default "fermo" file format, measurements of
  zero are considered negative (non-active) measurements and ignored in the
  calculations.