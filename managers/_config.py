"""
    ./managers/_config.py

    Functions for accessing the configuration stored in medict.cfg.
    The user can edit the details about SQL and settings in the
    config file, as in, medict.cfg and the stored value are
    parsed using the configparser module.

    medict.cfg should follow ini like setting.
    See https://docs.python.org/3/library/configparser.html?highlight=configparser#supported-ini-file-structure
    for how to actually set it up.
"""

import os
import configparser
from pathlib import Path


cfg_file = Path(__file__).parent.parent / "medict.cfg"
config = configparser.ConfigParser()
config.read(cfg_file)


def get_sql_config():
    """Returns the Configuration of ``SQL`` section
    These configuration it returns can be accessed as
    dictionaries.
    """
    return config["sql"]


def get_settings_config():
    """Returns the Configuration of ''settings'' section
    These configuration it returns can be accessed as
    dictionaries.
    """
    return config["settings"]


def set_settings_config(d):
    if "theme" in d:
        config["settings"]["theme"] = d["theme"]
    if "fontsize" in d:
        print(d["fontsize"])
        config["settings"]["fontsize"] = d["fontsize"]
    with open(cfg_file, "w") as configfile:
        config.write(configfile)
