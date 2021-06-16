from __future__ import print_function

# STDLIB
import os.path
import subprocess

# get the auto update version for the call to teal help
from .version import __version_date__, __version__

# STSCI
from stsci.tools import parseinput
from .util import error_code

try:
    from stsci.tools import teal
    has_teal = True
except ImportError:
    has_teal = False
    print("Teal not available")

__taskname__ = "wf3rej"


def wf3rej(input, output="", crrejtab="", scalense="", initgues="",
           skysub="", crsigmas="", crradius=0, crthresh=0,
           badinpdq=0, crmask=False, shadcorr=False, verbose=False,
           log_func=print):
    """call the calwf3.e executable"""

    call_list = ["wf3rej.e"]
    return_code = None

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3rej does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3rej can only accept 1 file for"
                      "input at a time: {0}".format(infiles))

    for image in infiles:
        if not os.path.exists(image):
            raise IOError("Input file not found: {0}".format(image))

    call_list.append(input)

    if output:
        call_list.append(str(output))

    if verbose:
        call_list.append("-v")
        call_list.append("-t")

    if (shadcorr):
        call_list.append("-shadcorr")

    if (crmask):
        call_list.append("-crmask")

    if (crrejtab != ""):
        call_list += ["-table", crrejtab]

    if (scalense != ""):
        call_list += ["-scale", str(scalense)]

    if (initgues != ""):
        options = ["min", "med"]
        if initgues not in options:
            print("Invalid option for intigues")
            return ValueError
        else:
            call_list += ["-init", str(initgues)]

    if (skysub != ""):
        options = ["none", "mode", "median"]
        if skysub not in options:
            print(("Invalid skysub option: %s") % (skysub))
            print(options)
            return ValueError
        else:
            call_list += ["-sky", str(skysub)]

    if (crsigmas != ""):
        call_list += ["-sigmas", str(crsigmas)]

    if (crradius >= 0.):
        call_list += ["-radius", str(crradius)]
    else:
        print("Invalid crradius specified")
        return ValueError

    if (crthresh >= 0.):
        call_list += ["-thresh", str(crthresh)]
    else:
        print("Invalid crthresh specified")
        return ValueError

    if (badinpdq >= 0):
        call_list += ["-pdq", str(badinpdq)]

    else:
        print("Invalid DQ value specified")
        return ValueError

    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    ec = error_code(return_code)
    if return_code:
        if ec is None:
            print("Unknown return code found!")
            ec = return_code
        raise RuntimeError("wf3rej.e exited with code {}".format(ec))


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
    """Return documentation on the 'wf3ir' function. Required by TEAL."""

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
    """TEAL interface for the ``wf3rej`` function."""

    wf3rej(configobj['input'],
           output=configobj['output'],
           crrejtab=configobj['crrejtab'],
           scalense=configobj['scalense'],
           initgues=configobj['initgues'],
           skysub=configobj['skysub'],
           crsigmas=configobj['crsigmas'],
           crradius=configobj['crradius'],
           crthresh=configobj['crthresh'],
           badinpdq=configobj['badinpdq'],
           crmask=configobj['crmask'],
           shadcorr=configobj['shadcorr'],
           verbose=configobj['verbose'],)


# This replaces the help for the function which is also printed in the HTML
# and TEAL
wf3rej.__doc__ = getHelpAsString(docstring=True)
