#!/usr/bin/env python3

from importlib import metadata


VERSION = metadata.version("fermo_core")



def placeholder_function(a, b):
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b




if __name__ == "__main__":
    print(VERSION)
