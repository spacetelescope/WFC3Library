"""The wfc3tools package holds Python tasks useful for analyzing WFC3 data.

These tasks include:

Utility and library functions used by these tasks are also included in this
module.


"""
from __future__ import absolute_import, print_function

from .calwf3 import calwf3
from .wf32d import wf32d
from .wf3ccd import wf3ccd
from .wf3ir import wf3ir
from .wf3rej import wf3rej
from .wf3cte import wf3cte
from .sampinfo import sampinfo
from .pstack import pstack
from .pstat import pstat
from .sub2full import sub2full
from .embedsub import embedsub
from .util import *
from .version import *

import os

# These lines allow TEAL to print out the names of TEAL-enabled tasks
# upon importing this package.
try:
    from stsci.tools import teal
    teal.print_tasknames(__name__, os.path.dirname(__file__))
except (ImportError, UnboundLocalError):
    print("Teal not installed, gui param editing disabled")
