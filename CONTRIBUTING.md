# Contributing to `fermo_core`

Thank you for your interest in contributing to `fermo_core`! Please take a moment to
read this document to understand how you can contribute.

## Preamble

When contributing to this repository, please first discuss the change you wish to
make via issue, email, or any other method with the owners of this repository
before making a change. Please note we have a [Code of Conduct](CODE_OF_CONDUCT.md),
please follow it in all your interactions with the project.

## Getting Started/Pull Request Process

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your contribution and push it to your remote:
   - `git checkout -b <your-feature-name>`
   - `git push origin <your-feature-name>`
   - `git branch --set-upstream-to=origin/<your-feature-name>`
4. Install the package including the developer requirements as described in the Documentation.
5. Install `pre-commit` and run the test suite as described in the Documentation.
6. Make your changes and keep track of them in the [CHANGELOG.md] file.
7. Once the changes are ready for a pull request (PR), increase the version number in [pyproject.toml].
8. Create a PR on GitHub with a clear title, description, and a list of changes.
9. Your changes will be reviewed and, if approved, merged in the main branch.

## Code style and Guidelines

We want to write well-documented, clear and concise code that is easily maintainable.
For our strategy to achieve our goal, see below.

### Code style

- We use [Semantic Versioning](http://semver.org/) for versioning.
- We follow the
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
- We use automated linting and formatting.
- We apply following design principles:
  - **OOP** (object-oriented programming)
  - **KISS** (keep it super simple)
  - **DRY** (don't repeat yourself)
  - **SOLID** (single responsibility, open/closed, Liskov's substitution, interface
    segregation, dependency inversion)
  - **TDD** (test-driven development)
  - **Logging**
  - **LCC** (Low cognitive complexity)