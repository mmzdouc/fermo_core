# Contributing to [fermo_core]

Thank you for your interest in contributing to [fermo_core]! Please take a moment to
read this document to understand how you can contribute.

## Preamble

When contributing to this repository, please first discuss the change you wish to
make via issue, email, or any other method with the owners of this repository
before making a change. Please note we have a [Code of Conduct](CODE_OF_CONDUCT.md),
please follow it in all your interactions with the project.

## Getting Started/Pull Request Process

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine:
   - `git clone git@github.com:mmzdouc/fermo_core.git`
3. Create a new branch for your contribution:
   - `git checkout -b feature/your-feature-name`
4. Install the package, its requirements, and the developer requirements:
   - `pip install -e .`
   - `pip install -e '.[dev]'`
5. Install `pre-commit` which applies formatting and code testing before every commit:
   - `pre-commit install`
6. Make your changes and keep track of them in the [CHANGELOG.md] file.
7. Before committing the changes, increase the version number in [pyproject.toml].
8. Commit your changes to your branch:
   - `git commit -m "Add your commit message here"`
9. Push your changes to your forked repository:
   - `git push origin feature/your-feature-name`
10. Create a Pull Request (PR) on GitHub with a clear title and description.
    Reference any related issues, if applicable. Your PR will be reviewed and, if
    approved, merged.

## Code style and Guidelines

We want to write well-documented, clear and concise code that is easily maintainable.
For our strategy to achieve our goal, see below.

*"Writing code for yourself is easy - but it is difficult to write code that other
people can easily understand."*

### Code style

- We use [Semantic Versioning](http://semver.org/) for versioning.
- For code style and documentation, we follow the
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). An
  easy way to check for adherence is by using the `pycodestyle` package.
- We apply following design principles:
  - **OOP** (object-oriented programming)
  - **KISS** (keep it super simple)
  - **DRY** (don't repeat yourself)
  - **SOLID** (single responsibility, open/closed, Liskov's substitution, interface
    segregation, dependency inversion)
  - **TDD** (test-driven development)
  - **Logging**
  - **LCC** (Low cognitive complexity)
- We (try to) follow the Zen of Python (`import this`)

## Testing

- We write unit tests for our code using `pytest`.
- Addition of new functionality/modification of existent functionality goes in hand
  with addition/modification of the appropriate tests.

## Functionality Addition/Modification Guidelines

### Addition/Modification of Parameters

- Modify/add the default parameter file [`fermo_core/config/default_parameters.json`]
- Modify the json schema [`fermo_core/config/schema.json`]
- Modify the ParameterManager class
  [`fermo_core/input_output/class_parameter_manager`]:
  add/modify the attributes and methods to parse the parameter file and to assign the
  parameters.
- Modify/add validation methods in the ValidationManager class
  [`fermo_core/input_output/class_validation_manager`]:
  add/modify the methods to validate parameters
- Depending on the type of parameter, implement downstream changes in data processing
- Adjust/add the unit tests covering the modified classes (each class is covered by
  a separate file.)
- If applicable, add an example file to `tests/example_files/`

#### Example: New Peaktable Format

Example protocol for addition of new peaktable format to make fermo_core compatible
with another pre-processing program:
- Add the new peaktable format to `allowed_formats` in the file
  [`fermo_core/config/default_parameters.json`].
- Since this change affects an existing array in the json file, no change to `schema.
  json` is required.
- Add the new peaktable format to `allowed_formats` in the file
  [`tests/example_files/example_parameters.json`].
- Since the change affects an existing attribute, no changes to the ParameterManager
  file are required.
- Since the change affects an existing attribute, no changes/additions to the
  ValidationManager are required.
- In the PeaktableParser class in
  [`fermo_core/data_processing/parser/class_peaktable_parser.py`], in the `parse()`
  method, add a `case` statement for the new peaktable format. Further, add a new
  method `parse_newformat` that parses the new peaktable format.
- Cover the new method `parse_newformat` with unit tests to verify its functioning.
  Add a new example file to [`tests/example_files/newpeaktable.format`] to use for
  the testing.
- Inspect the return values (`stats, features, samples`) for correctness.
