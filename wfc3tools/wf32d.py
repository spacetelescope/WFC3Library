"""
wf32d:

    Use this function to facilitate batch runs.

    The wf32d primary functions include:

      - DARKCORR: dark current subtraction
      - FLATCORR: flat-fielding
      - PHOTCORR: photometric keyword calculations
      # Do we still need flux corr
      - FLUXCORR: photometric normalization of the UVIS1 and UVIS2 chips

    Only those steps with a switch value of PERFORM in the input files will be
    executed, after which the switch will be set to COMPLETE in the
    corresponding output files.

The wf32d function can also be called directly from the OS command line:

    >>> wf32d.e input output [-options]

    Where the OS options include:

        * -v: verbose
        * -t: print time stamps
        * -d: debug
        * -dark: perform dark subtraction
        * -dqi: update the DQ array
        * -flat: perform flat correction
        * -shad: perform shading correction
        * -phot: perform phot correction

"""

from __future__ import print_function

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def wf32d(input, output=None, dqicorr="PERFORM", darkcorr="PERFORM",
          flatcorr="PERFORM", shadcorr="PERFORM", photcorr="PERFORM",
          verbose=False, quiet=True, debug=False, log_func=print):
    """
    Call the wf32d.e executable.

    Parameters
    ----------
    input : str or list
        Name of input files, such as
        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``\*raw.fits``)
        - filename of an ASN table (``\*asn.fits``)
        - an at-file (``@input``)

    output : str, default=None
        Name of the output FITS file.

    dqicorr : str, optional, default="PERFORM"
        Update the dq array from bad pixel table. Allowed values are "PERFORM"
        and "OMIT".

    darkcorr : str, optional, default="PERFORM"
        Subtract the dark image. Allowed values are "PERFORM" and "OMIT".

    flatcorr : str, optional, default="PERFORM"
        Multiply by the flatfield image. Allowed values are "PERFORM" and
        "OMIT".

    shadcorr : str, optional, default="PERFORM"
        Correct for shutter shading (CCD). Allowed values are "PERFORM" and
        "OMIT".

    photcorr : str, optional, default="PERFORM"
        Update photometry keywords in the header. Allowed values are "PERFORM"
        and "OMIT".

    verbose : bool, optional, default=False
        If True, print verbose time stamps.

    quiet : bool, optional, default=True
        If True, print messages only to trailer file.

    debug : bool, optional, default=False
        If True, print debugging statements.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    DO WE STILL NEED THIS?
    fluxcorr : str, optional, default="PERFORM"
        Perform chip photometry normalization. Allowed values are "PERFORM" and
        "OMIT".

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import wf32d
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf32d(filename)

    """

    call_list = ['wf32d.e']
    return_code = None

    if verbose:
        call_list += ['-v', '-t']

    if debug:
        call_list.append('-d')

    if (darkcorr == "PERFORM"):
        call_list.append('-dark')

    if (dqicorr == "PERFORM"):
        call_list.append('-dqi')

    if (flatcorr == "PERFORM"):
        call_list.append('-flat')

    if (shadcorr == "PERFORM"):
        call_list.append('-shad')

    if (photcorr == "PERFORM"):
        call_list.append('-phot')

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf32d does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf32d can only accept 1 file for"
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
        raise RuntimeError("wf32d.e exited with code {}".format(ec))

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    wf32d(sys.argv[1])
