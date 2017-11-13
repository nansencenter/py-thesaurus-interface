from __future__ import absolute_import
from os import environ

try:
    from xdg import (XDG_DATA_HOME)
except ImportError:
    XDG_DATA_HOME = '.'

import os

def _get_data_home():
    if os.name == 'nt':
        if "XDG_DATA_HOME" in environ:
            return environ.get("XDG_DATA_HOME")
        else:
            return environ.get("LOCALAPPDATA")
    else:
        return XDG_DATA_HOME

DATA_HOME = _get_data_home()
