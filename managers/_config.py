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