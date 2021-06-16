.. _wf3ir:


*****
wf3ir
*****

Use this function to facilitate batch runs or for the TEAL interface.

This routine contains all the instrumental calibration steps for
WFC3 IR channel images. The steps are:

    * DQICORR - initialize the data quality array
    * ZSIGCORR - estimate the amount of signal in the zeroth-read
    * BLEVCORR - subtact the bias level from the reference pixels
    * ZOFFCORR - subtract the zeroth read image
    * NLINCORR - correct for detector non-linear response
    * DARKCORR - subtract the dark current image
    * PHOTCORR - compute the photometric keyword values
    * UNITCORR - convert to units of count rate
    * CRCORR - fit accumulating signal and identify the cr hits
    * FLATCORR - divide by the flatfield images and apply gain coversion

The output images include the calibrated image ramp (ima file)
and the accumulated ramp image (flt file)

Only those steps with a switch value of PERFORM in the input files
will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Running `wf3ir` from a python terminal
=========================================

In Python without TEAL:

.. code-block:: python

    from wfc3tools import wf3ir
    wf3ir(filename)

In Python with TEAL:

.. code-block:: python

    from stsci.tools import teal
    from wfc3tools import wf3ir
    teal.teal('wf3ir')

In Pyraf:

.. code-block:: python

    import wfc3tools
    epar wf3ir


Displaying output from wf3ir in a Jupyter Notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When calling `wf3ir` from a Jupyter notebook, informational text output from the underlying `wf3ir.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3ir`. As output is read from the underlying program, the `wf3ir` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3ir` to the Python logging system by passing the `logging.debug` function or similar.)

If log_func=None is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.



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

    verbose: bool, optional
        Print verbose time stamps?

    quiet: bool, optional
        Print messages only to trailer file?


Command Line Options for the wf3ir executable
=============================================

.. code-block:: shell

    wf32ir.e input output [-options]

input may be a single filename

Where the options include:

* -v: verbose
* -f: print time stamps
