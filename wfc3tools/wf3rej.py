"""
wf3rej:

    This calls the wf3rej executable. Use this function to facilitate batch
    runs.

The wf3rej executable can also be called directly from the OS command line
prompt:

    >>> wf3rej.e input output [-options]

    Input can be a single file, or a comma-delimited list of files.

    Where the OS options include:

        * -v: verbose
        * -t: print the timestamps
        * -shadcorr: perform shading shutter correction
        * -crmask: flag CR in input DQ images
        * -table <filename>: the crrejtab filename
        * -scale <number>: scale factor for noise
        * -init <med|min>: initial value estimate scheme
        * -sky <none|median|mode>: how to compute sky
        * -sigmas: rejection levels for each iteration
        * -radius <number>: CR expansion radius
        * -thresh <number> : rejection propagation threshold
        * -pdq <number>: data quality flag bits to reject

"""

from __future__ import print_function

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def wf3rej(input, output="", crrejtab="", scalense="", initgues="",
           skysub="", crsigmas="", crradius=0, crthresh=0,
           badinpdq=0, crmask=False, shadcorr=False, verbose=False,
           log_func=print):
    """
    Call the calwf3.e executable.

    Parameters
    ----------
    input : str or list
        Name of input files, such as
        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``\*raw.fits``)
        - filename of an ASN table (``\*asn.fits``)
        - an at-file (``@input``)

    output : str, default=""
        Name of the output FITS file.

    crrejtab : str, default=""
        Reference file name.

    scalense : str, default="" (IS THIS A FLOAT)
        Scale factor applied to noise.

    initgues : str, default=""
        Initial value estimate scheme (min|med).

    skysub : str, default=""
        How to compute the sky (none|mode|mean).

    crsigmas : str, default="" (IS THIS A FLOAT)
        Rejection levels in each iteration.

    crradius : float, default=0
        Cosmic ray expansion radius in pixels.

    crthresh : float, default=0
        Rejection propagation threshold.

    badinpdq : int, default=0
        Data quality flag bits to reject.

    crmask : bool, default=False
        If True, flag CR in input DQ images.

    shadcorr : bool, default=False
        If True, perform shading shutter correction.

    verbose : bool, optional, default=False
        If True, Print verbose time stamps.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import wf3rej
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3rej(filename)

    """

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

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    wf3rej(sys.argv[1])
