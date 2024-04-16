"""This module stores the application's constant values."""

from typing import NamedTuple


class Constants(NamedTuple):
    """Creates all constants used in this module."""

    yml_schema_version = 1.0
    module_name = "autotwin.ensemble"
    module_short_name = "ensemble"
    module_prompt = module_name + ">"
