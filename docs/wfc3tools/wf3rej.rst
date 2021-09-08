.. _wf3rej:

******
wf3rej
******

Use this function to facilitate batch runs.


Displaying output from wf3rej in a Jupyter Notebook
===================================================

When calling `wf3rej` from a Jupyter notebook, informational text output from the underlying `wf3rej.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3rej`. As output is read from the underlying program, the `wf3rej` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3rej` to the Python logging system by passing the logging.debug function or similar.)

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
=======

    None


Usage
=====

.. code-block:: python

    from wfc3tools import wf3rej
    wf3rej(filename)


Command Line Options for the wf3rej executable
==============================================

.. code-block:: shell

    wf3rej.e input output [-options]

Input may be a single filename, and the options include:

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
