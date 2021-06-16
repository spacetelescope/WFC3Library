from __future__ import print_function

# get the auto update version for the call to teal help
from .version import __version_date__, __version__

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput

try:
    from stsci.tools import teal
    has_teal = True
except ImportError:
    has_teal = False
    print("Teal not available")

__taskname__ = "wf3cte"


def wf3cte(input, out=None, parallel=True, verbose=False, log_func=print):

    """Run the ``wf3cte.e`` executable as from the shell."""

    call_list = ['wf3cte.e']

    if verbose:
        call_list.append('-v')

    if not parallel:
        call_list.append('-1')

    infiles, dummy_out = parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    if out:
        call_list.append(str(out))

    print(call_list)
    
    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    if return_code != 0:
        raise RuntimeError("wf3cte.e exited with code {}".format(return_code))


def help(file=None):
    helpstr = getHelpAsString(docstring=True)
    if file is None:
        print(helpstr)
    else:
        if os.path.exists(file):
            os.remove(file)
        f = open(file, mode='w')
        f.write(helpstr)
        f.close()


def getHelpAsString(docstring=False):
    """Return documentation on the 'wf3cte' function. Required by TEAL."""

    install_dir = os.path.dirname(__file__)
    htmlfile = os.path.join(install_dir, 'htmlhelp', __taskname__ + '.html')
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    if docstring or (not docstring and not os.path.exists(htmlfile)):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __version_date__]) + '\n\n'
        if os.path.exists(helpfile) and has_teal:
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
    else:
        helpString = 'file://' + htmlfile

    return helpString


def run(configobj=None):
    """
    TEAL interface for the ``wf3cte`` function.

    """
    wf3cte(configobj['input'],
           parallel=configobj['parallel'],
           verbose=configobj['verbose'],)

wf3cte.__doc__ = getHelpAsString(docstring=True)
