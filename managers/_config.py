"""
    _config.py
    ~~~~~~~~~~

    Accessing the configuration stored in ``medict.cfg``.
    The user can edit the details about SQL and FTP in the
    config file, as in, ``medict.cfg`` and the stored value are
    parsed using the ``configparser`` module.

    ``medict.cfg`` should follow ``ini`` like setting.
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


def get_ftp_config():
    """Returns the Configuration of ``ftp`` section
    These configuration it returns can be accessed as
    dictionaries.
    """
    return config["ftp"]


def get_settings_config():
    """Returns the Configuration of ''settings'' section
    These configuration it returns can be accessed as
    dictionaries.
    """
    return config["settings"]


def set_settings_config(d):
    config["settings"]["theme"] = d["theme"]
    with open(cfg_file, "w") as configfile:
        config.write(configfile)
