.. _wf3ccd:

******
wf3ccd
******

This routine contains the initial processing steps for all the WFC3 UVIS channel data. These steps are:

    * DQICORR - initializing the data quality array
    * ATODCORR - perform the a to d conversion correction
    * BLEVCORR - subtract the bias level from the overscan region
    * BIASCORR - subtract the bias image
    * FLSHCORR - subtract the post-flash image


`wf3ccd` first subtracts the bias and trims the overscan regions from the image. If an associated set of UVIS CR-SPLIT or REPEAT-OBS images is being processed,
all of the overscan-trimmed images are sent through `wf3rej` to be combined and receive cosmic-ray rejection. The resulting combined image then receives final calibration with `wf32d`,
which includes dark subtraction and flat-fielding. If there are multiple sets of CR-SPLIT or REPEAT-OBS images in an association, each set goes through the cycle of `wf3ccd`, `wf3rej`
and `wf32d` processing.


If BLEVCORR is performed, the output contains the overcan-trimmed region.

Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.


Displaying output from wf3ccd in a Jupyter Notebook
===================================================

When calling `wf3ccd` from a Jupyter notebook, informational text output from the underlying `wf3ccd.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3ccd`. As output is read from the underlying program, the `wf3ccd` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3ccd` to the Python logging system by passing the `logging.debug` function or similar.)

If `log_func=None` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.


Parameters
==========

    input : str or list
        Name of input files, such as

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``)

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
=======

    None


Usage
=====

.. code-block:: python

    from wfc3tools import wf3ccd
    wf3ccd(filename)


Command Line Options for the wf3ccd executable
==============================================

.. code-block:: shell

    wf32ccd.e input output [-options]

Input may be a single filename, and the options include:

* -v: verbose
* t: print time stamps
* -dqi: udpate the DQ array
* -atod: perform gain correction
* -blev: subtract bias from overscan
* -bias: perform bias correction
* -flash: remove post-flash image
