"""Storage and handling of instances of complex objects.

Layer of abstraction for storing/retrieving object instances. If necessary, storage
in Python dict can be replaced with more sophisticated methods (e.g. database).

Copyright (c) 2022-2023 Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons toFill this up whom the Software is
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

from typing import Self, Union

from pydantic import BaseModel

from fermo_core.data_processing.builder_feature.dataclass_feature import Feature
from fermo_core.data_processing.builder_sample.dataclass_sample import Sample


class Repository(BaseModel):
    """Handles addition, retrieval, modification, and deletion of class instances.

    Attributes:
        entries: a dict to store instances of the class in repository
    """

    entries: dict = {}

    def add(self: Self, identifier: Union[int, str], entry: Union[Feature, Sample]):
        """Add a new entry to repository dict.

        Args:
            identifier: an identifier used as key in dictionary
            entry: object to store

        Raises:
            ValueError: Cannot add entry because it already exists in the repository.
        """
        if self.entries.get(identifier) is None:
            self.entries[identifier] = entry
        else:
            raise ValueError(f"Object '{identifier}' already exists in repository.")

    def get(self: Self, identifier: Union[int, str]) -> Union[Feature, Sample]:
        """Get an entry from the repository dict.

        Args:
            identifier: an identifier found in the repository dict.

        Returns:
            An object instance from entries dict

        Raises:
            KeyError: Cannot get the entry because it does not exist in repository.
        """
        if (entry := self.entries.get(identifier)) is not None:
            return entry
        else:
            raise KeyError(f"Object '{identifier}' does not exist in repository.")

    def modify(self: Self, identifier: Union[int, str], entry: Union[Feature, Sample]):
        """Modify an entry by overwriting it.

        Args:
            identifier: an identifier found in the repository dict.
            entry: an object instance.

        Raises:
            KeyError: Cannot modify entry because it does not exist in the repository.
        """
        if self.entries.get(identifier) is not None:
            self.entries[identifier] = entry
        else:
            raise KeyError(f"Object '{identifier}' does not exist in repository.")

    def remove(self: Self, identifier: Union[int, str]):
        """Remove an entry from Repository.

        Args:
            identifier: an identifier found in the repository dict.

        Raises:
            KeyError: Cannot remove entry because it does not exist in the repository.
        """
        if self.entries.get(identifier) is not None:
            del self.entries[identifier]
        else:
            raise KeyError(f"Object '{identifier}' does not exist in repository.")
