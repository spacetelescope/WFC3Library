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


If BLEVCORR is performed the output contains the overcan-trimmed region.

Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Running `wf3ccd` from a python terminal
=========================================

In Python without TEAL:

.. code-block:: python

    from wfc3tools import wf3ccd
    wf3ccd(filename)

In Python with TEAL:

.. code-block:: python

    from stsci.tools import teal
    from wfc3tools import wf3ccd
    teal.teal('wf3ccd')

In Pyraf:

.. code-block:: python

    import wfc3tools
    epar wf3ccd


Displaying output from wf3ccd in a Jupyter Notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When calling `wf3ccd` from a Jupyter notebook, informational text output from the underlying `wf3ccd.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3ccd`. As output is read from the underlying program, the `wf3ccd` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3ccd` to the Python logging system by passing the `logging.debug` function or similar.)

If `log_func=None` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.



Input Parameters for the Python interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    input: str
        Name of input files

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``)

    output: str
        Name of the output FITS file.

    dqicorr: str, "PERFORM/OMIT", optional
        Update the dq array from bad pixel table

    atodcorr: str, "PERFORM/OMIT", optional
        Analog to digital correction

    blevcorr: str, "PERFORM/OMIT", optional
        Subtract bias from overscan regions

    biascorr: str, "PERFORM/OMIT", optional
        Subtract bias image

    flashcorr: str, "PERFORM/OMIT", optional
        Subtract post-flash image

    verbose: bool, optional
        Print verbose time stamps?

    quiet: bool, optional
        Print messages only to trailer file?


Command Line Options for the wf3ccd executable
==============================================

.. code-block:: shell

    wf32ccd.e input output [-options]

input may be a single filename

Where the options include:

* -v: verbose
* -f: print time stamps
* -dqi: udpate the DQ array
* -atod: perform gain correction
* -blev: subtract bias from overscan
* -bias: perform bias correction
* -flash: remove post-flash image
