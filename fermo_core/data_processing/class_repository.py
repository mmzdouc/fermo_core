"""Storage and handling of instances complex objects

TODO(MMZ): Improve description of class

TODO(MMZ): Add correct type hints for what can go into repository: General Feature, Sample

Copyright (c) 2022-2023 Mitja Maximilian Zdouc, PhD

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
from abc import ABC, abstractmethod
from fermo_core.data_processing.builder.dataclass_feature import Feature
from fermo_core.data_processing.builder.dataclass_sample import Sample


class IRepository(ABC):
    """Abstract base class for a Repository design pattern."""

    @abstractmethod
    def add(self, identifier, entry):
        """Add a non-existing entry to the repository."""
        raise NotImplementedError

    @abstractmethod
    def get(self, identifier):
        """Retrieve an existing entry from the repository."""
        raise NotImplementedError

    @abstractmethod
    def modify(self, identifier, entry):
        """Modify an existing entry by overwriting it."""
        raise NotImplementedError


class Repository(IRepository):
    """Handles addition, retrieval, and modification of class instances.

    Attributes:
        entries: a dict to store instances of the class in repository
    """

    def __init__(self):
        self.entries: dict = {}

    def add(self, identifier: int | str, entry: Feature | Sample):
        """Add a new entry to repository dict.

        Args:
            identifier: an identifier used as key in dictionary
            entry: object to store
        """
        if identifier not in self.entries:
            self.entries[identifier] = entry
        else:
            print(f"Cannot add entry: '{identifier}' already exists in repository.")

    def get(self, identifier: int) -> Feature | Sample:
        """Get an entry from the repository dict.

        Args:
            identifier: an identifier found in the repository dict.

        Returns:
            An object instance from entries dict
        """
        if identifier in self.entries:
            return self.entries.get(identifier)
        else:
            print(f"Cannot get entry: '{identifier}' does not exist in repository.")

    def modify(self, identifier: int, entry: Feature | Sample):
        """Modify an entry by overwriting it.

        Args:
            identifier: an identifier found in the repository dict.
            entry: an object instance.
        """
        if identifier in self.entries:
            self.entries[identifier] = entry
        else:
            print("Cannot modify entry: does not exist.")
