.. _wf3rej:

******
wf3rej
******

This calls the wf3rej executable. Use this function to
facilitate batch runs or for the TEAL interface.

Running `wf3rej` from a python terminal
=========================================

In Python without TEAL:

.. code-block:: python

    from wfc3tools import wf3rej
    wf3rej(filename)

In Python with TEAL:

.. code-block:: python

    from stsci.tools import teal
    from wfc3tools import wf3rej
    teal.teal('wf3rej')

In Pyraf:

.. code-block:: python

    import wfc3tools
    epar wf3rej


Displaying output from wf3rej in a Jupyter Notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When calling `wf3rej` from a Jupyter notebook, informational text output from the underlying `wf3rej.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3rej`. As output is read from the underlying program, the `wf3rej` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3rej` to the Python logging system by passing the logging.debug function or similar.)

If `log_func=None` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.



Input Parameters for the Python interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

input : str, Name of input files

      - a single filename (``iaa012wdq_raw.fits``)
      - a Python list of filenames
      - a partial filename with wildcards (``\*raw.fits``)
      - filename of an ASN table (``\*asn.fits``)
      - an at-file (``@input``)

output: string
    Name of the output FITS file.

crrejtab: string
    reference file name

scalense: string
    scale factor applied to noise

initgues: string
    intial value estimate scheme (min|med)

skysub: string
    how to compute the sky (none|mode|mean)

crsigmas: string
    rejection levels in each iteration

crradius: float
    cosmic ray expansion radius in pixels

crthresh: float
    rejection propagation threshold

badinpdq: int
    data quality flag bits to reject

crmask: bool
    flag CR in input DQ imageS?

shadcorr: bool
    perform shading shutter correction?

verbose: bool, optional
    Print verbose time stamps?


Command Line Options for the wf3rej executable
==============================================

.. code-block:: shell

    wf3rej.e input output [-options]

Input can be a single file

Where the options include:

* t: print the timestamps
* v: verbose
* shadcorr: perform shading shutter correction?
* crmask: flag CR in input DQ images?
* table <filename>: the crrejtab filename
* scale <number>: scale factor for noise
* init <med|min>: initial value estimate scheme
* sky <none|median|mode>: how to compute sky
* sigmas: rejection leves for each iteration
* radius <number>: CR expansion radius
* thresh <number> : rejection propagation threshold
* pdq <number>: data quality flag bits to reject
