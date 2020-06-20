import sys

from .csvmanager import CSVManager

if sys.platform != "darwin":
    from .sqlview import SQLManager
