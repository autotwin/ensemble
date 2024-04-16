"""Holds constants used across the module."""

from importlib.metadata import version

import ensemble.constants as cs


CLI_DOCS = """
-----------------
autotwin.ensemble
-----------------

ensemble
    (this command)

process <pathfile>.yml
    Process the .yml input file.
    Example:
        process tests/files/getting_started.yml # TODO

pytest
    Runs the test suite (non-verbose option).

pytest -v
    Runs the test suite (verbose option).

validate <pathfile>.yml # TODO
    Validate the .yml input file against the module's schema.

version
    Prints the semantic version of the current installation.
"""


def ensemble():
    """Prints the command line documentation to the command window."""
    print(CLI_DOCS)


def module_version():
    """Prints the module version and the yml_schema_version."""

    module_name = cs.Constants.module_short_name
    ver = version(module_name)
    print(f"\nmodule version: {ver}")
    print(f"  yml_schema_version: {cs.Constants.yml_schema_version}\n")
