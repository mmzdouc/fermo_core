#!/usr/bin/env python3

from importlib import metadata


VERSION = metadata.version("fermo_core")


if __name__ == "__main__":
    print(VERSION)
