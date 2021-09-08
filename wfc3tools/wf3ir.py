"""
wf3ir:

    Use this function to facilitate batch runs.

    This routine contains all the instrumental calibration steps for
    WFC3 IR channel images. The steps are:

        - DQICORR: initialize the data quality array
        - ZSIGCORR: estimate the amount of signal in the zeroth-read
        - BLEVCORR: subtract the bias level from the reference pixels
        - ZOFFCORR: subtract the zeroth read image
        - NLINCORR: correct for detector non-linear response
        - DARKCORR: subtract the dark current image
        - PHOTCORR: compute the photometric keyword values
        - UNITCORR: convert to units of count rate
        - CRCORR: fit accumulating signal and identify the cr hits
        - FLATCORR: divide by the flatfield images and apply gain conversion

    The output images include the calibrated image ramp (ima file) and the
    accumulated ramp image (flt file).

    Only those steps with a switch value of PERFORM in the input files
    will be executed, after which the switch will be set to COMPLETE in the
    corresponding output files.

*The wf3ir function can also be called directly from the OS command line:

    >>> wf32ir.e input output [-options]

    Where the OS options include:

        * -v: verbose
        * -t: print time stamps

"""

from __future__ import print_function

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def wf3ir(input, output=None, verbose=False, quiet=True, log_func=print):
    """
    Call the wf3ir.e executable.

    Parameters
    ----------
    input : str
        Name of input files, such as
        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``\*raw.fits``)
        - filename of an ASN table (``\*asn.fits``)
        - an at-file (``@input``)

    output : str, default=None
        Name of the output FITS file.

    verbose : bool, optional, default=False
        If True, print verbose time stamps.

    quiet : bool, optional, default=True
        If True, print messages only to trailer file.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import wf3ir
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3ir(filename)

    """

    call_list = ['wf3ir.e']
    return_code = None

    if verbose:
        call_list += ['-v', '-t']

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ir does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ir can only accept 1 file for"
                      "input at a time: {0}".format(infiles))

    for image in infiles:
        if not os.path.exists(image):
            raise IOError("Input file not found: {0}".format(image))

    call_list.append(input)

    if output:
        call_list.append(str(output))

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
        raise RuntimeError("wf3ir.e exited with code {}".format(ec))

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    wf3ir(sys.argv[1])
