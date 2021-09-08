"""
wf3cte:

    The charge transfer efficiency (CTE) of the UVIS detector has inevitably
    been declining over time as on-orbit radiation damage creates charge traps
    in the CCDs. Faint sources in particular can suffer large flux losses or
    even be lost entirely if observations are not planned and analyzed
    carefully. The CTE loss will depend on the morphology of the source, the
    distribution of electrons in the field of view (from sources, background,
    cosmic rays, and hot pixels) and the population of charge traps in the
    detector column between the source and the transfer register. And the
    magnitude of the CTE loss increases continuously with time as new charge
    traps form.

    CTE is typically measured as a pixel-transfer efficiency, and would be unity
    for a perfect CCD. One indicator of CTE is the Extended Pixel Edge Response
    (EPER). Inefficient transfer of electrons in a flat-field exposure produces
    an exponential tail of charge in the overscan region. Analysis of monitoring
    observations through January 2013 shows that CTE continues to decline
    linearly over time (`WFC3 ISR 2013-03 <https://www.stsci.edu/files/live/
    sites/www/files/home/hst/instrumentation/wfc3/documentation/instrument-
    science-reports-isrs/_documents/2013/WFC3-2013-03.pdf>`_).

    The CTE correction step uses its own dark reference files which have
    themselves been corrected for CTE. The specific reference file used for any
    dataset may be found in the image header keyword DRKCFILE. This step also
    uses a special bias reference file as part of the CTE correction itself,
    referred to in the header by the BIACFILE keyword. This BIACFILE is only
    used to facilitate the CTE correction, the resulting corrected image then
    uses the normal BIASFILE to correct the science frame after the CTE
    correction has been performed. After the CTE correction has been performed
    and the data progresses through the rest of the pipeline, the special CTE
    corrected dark, DRKCFILE in the header, will be used for the dark current
    correction instead of the DARKFILE.

    There is a PCTETAB refrence file which contains extensions of calibration
    images and tables of parameters used during the CTE correction stage. The
    header of this file also contains parameters for the CTE correction
    algorithm. These parameters, and important scalars which are used to
    correct the data are stored in the output image headers. Users who wish to use other settings for the CTE correction algorithm can adjust the pertinent keywords in their dataset header and `calwf3` will show them preference.

    See the UVIS2.0 reference ISR 2016-01 for more information (https://
    www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/wfc3/
    documentation/instrument-science-reports-isrs/_documents/2016/WFC3-2016-
    01.pdf).

    This routine performs the CTE correction on raw data files. The calibration
    step keyword is PCTECORR; if this is set to PERFORM, then the CTE correction
    will be applied to the dataset. Some caveats for its use:

        - CTE corrections can ONLY be performed on RAW data which has not been
        calibrated in any way.
        - Data which have already been through BLEVCORR, BIASCORR or DARKCORR
        will be rejected.
        - The CTE correction step in the pipeline is implemented for FULL FRAME
        images only in v3.3, but v3.4 will also correct the CTE in the
        following subarray apertures, the primary distinction being that these
        apertures have physical overscan pixels included which are used to
        calculate a secondary bias subtraction for the image before the CTE is
        measured; a future version of `calwf3` may enable CTE corrections for
        the remaining subarrays which don't have physical overscan pixels, but
        is still being validated by the science team.

    The standalone call will produce a RAC fits file by default. This contains
    only the CTE corrected data, no other calibrations have been performed.

    For more information the the WFC3 CTE please see `the WFC3 CTE webpage
    <https://www.stsci.edu/hst/instrumentation/wfc3/performance/cte>`_ .

The wf3cte function can also be called directly from the OS command line:

    >>> wf3cte.e input  [-options]

    Where the OS options include:

        * -v: verbose
        * -1: turn off multiprocessing

"""

from __future__ import print_function

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput


def wf3cte(input, output=None, parallel=True, verbose=False, log_func=print):
    """
    Run the ``wf3cte.e`` executable as from the shell.

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

    parallel : bool, default=True
        If True, run the code with OpemMP parallel processing turned on for the
        UVIS CTE correction.

    verbose: bool, optional, default=False
        If True, print verbose time stamps.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import wf3cte
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3cte(filename)

    """

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

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    wf3cte(sys.argv[1])
