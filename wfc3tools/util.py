# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import print_function, division
import warnings
from .version import __version__

__all__ = ["display_help"]

try:
    from stsci.tools import teal
except:
    teal = None


def display_help():
    """ display local html help in a browser window"""
    url = "http://wfc3tools.readthedocs.io/"
    print(url)
    try:
        import webbrowser
        # grab the version that's installed
        if "dev" not in __version__:
            url += "en/{0:s}/".format(__version__)
        webbrowser.open(url)
    except ImportError:
        warnings.warn("webbrowser module not installed, see {0:s} help \
                       pages".format(url))


def error_code(code=None):
    """ return the error code text, or all if code is None."""

    codes = {2: "ERROR_RETURN",
             111: "OUT_OF_MEMORY",
             114: "OPEN_FAILED",
             115: "CAL_FILE_MISSING",
             116: "NOTHIN_TO_DO",
             117: "KEYWORD_MISSING",
             118: "ALLOCATION_PROBLEM",
             119: "HEADER_PROBLEM",
             120: "SIZE_MISMATCH",
             130: "CAL_STEP_NOT_DONE",
             141: "TABLE_ERROR",
             142: "COLUMN_NOT_FOUND",
             143: "ELEMENT_NOT_FOUND",
             144: "ROW_NOT_FOUND",
             151: "NO_GOOD_DATA",
             152: "NO_CHIP_FOUND",
             171: "REF_TOO_SMALL",
             999: "INTERNAL_ERROR",
             1001: "INVALID_EXPTIME",
             1011: "INVALID_FILENAME",
             1020: "WRITE_FAILED",
             1021: "INVALID_TEMP_FILE",
             1023: "FILE_NOT_READABLE",
             1025: "COPY_NOT_POSSIBLE",
             1111: "INVALID_VALUE",
             1030: "UNSUPPORTED_APERTURE",
             }

    if code is None:
        return codes
    elif code in codes:
        return codes[code]
    else:
        return None
