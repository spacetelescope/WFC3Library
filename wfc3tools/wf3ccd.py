"""
wf3ccd:

    This routine contains the initial processing steps for all the WFC3 UVIS
    channel data. These steps are:

        - DQICORR: initializing the data quality array
        - ATODCORR: perform the a to d conversion correction
        - BLEVCORR: subtract the bias level from the overscan region
        - BIASCORR: subtract the bias image
        - FLSHCORR: subtract the post-flash image

    ``wf3ccd`` first subtracts the bias and trims the overscan regions from the
    image. If an associated set of UVIS CR-SPLIT or REPEAT-OBS images is being
    processed, all of the overscan-trimmed images are sent through ``wf3rej``to
    be combined and receive cosmic-ray rejection. The resulting combined image
    then receives final calibration with ``wf32d``, which includes dark
    subtraction and flat-fielding. If there are multiple sets of CR-SPLIT or
    REPEAT-OBS images in an association, each set goes through the cycle of
    ``wf3ccd``, ``wf3rej`` and ``wf32d`` processing.

    If BLEVCORR is performed the output contains the overcan-trimmed region.

    Only those steps with a switch value of PERFORM in the input files will be
    executed, after which the switch will be set to COMPLETE in the
    corresponding output files.

The wf3ccd function can also be called directly from the OS command line:

    >>> wf32ccd.e input output [-options]

    Where the OS options include:

        * -v: verbose
        * -t: print time stamps
        * -dqi: udpate the DQ array
        * -atod: perform gain correction
        * -blev: subtract bias from overscan
        * -bias: perform bias correction
        * -flash: remove post-flash image

"""

from __future__ import print_function

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def wf3ccd(input, output=None, dqicorr="PERFORM", atodcorr="PERFORM",
           blevcorr="PERFORM", biascorr="PERFORM", flashcorr="PERFORM",
           verbose=False, quiet=True, log_func=print):
    """
    Run the ``wf3ccd.e`` executable as from the shell.

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

    atodcorr : str, optional, default="PERFORM"
        Analog to digital correction. Allowed values are "PERFORM" and "OMIT".

    blevcorr : str, optional, default="PERFORM"
        Subtract bias from overscan regions. Allowed values are "PERFORM" and
        "OMIT".

    biascorr : str, optional, default="PERFORM"
        Subtract bias image. Allowed values are "PERFORM" and "OMIT".

    flashcorr : str, optional, default="PERFORM"
        Subtract post-flash image. Allowed values are "PERFORM" and "OMIT".

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
    >>> from wfc3tools import wf3ccd
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3ccd(filename)

    """

    call_list = ['wf3ccd.e']
    return_code = None

    if verbose:
        call_list += ['-v', '-t']

    if (dqicorr == "PERFORM"):
        call_list.append('-dqi')

    if (atodcorr == "PERFORM"):
        call_list.append('-atod')

    if (blevcorr == "PERFORM"):
        call_list.append('-blev')

    if (biascorr == "PERFORM"):
        call_list.append('-bias')

    if (flashcorr == "PERFORM"):
        call_list.append('-flash')

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ccd does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ccd can only accept 1 file for"
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
        raise RuntimeError("wf3ccd.e exited with code {}".format(ec))

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    wf3ccd(sys.argv[1])
