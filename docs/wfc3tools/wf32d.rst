.. _wf32d:


*****
wf32d
*****

Use this function to facilitate batch runs.

The wf32d primary functions include:

  * DARKCORR: dark current subtraction
  * FLATCORR: flat-fielding
  * PHOTCORR: photometric keyword calculations
  * FLUXCORR: photometric normalization of the UVIS1 and UVIS2 chips

Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.


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


Returns
=======

    None


Usage
=====

.. code-block:: python

    from wfc3tools import wf32d
    wf32d(filename)


Command Line Options for the wf32d executable
=============================================

.. code-block:: shell

    wf32d.e input output [-options]

Input may be a single filename, and the options include:

* -v: verbose
* -t: print time stamps
* -d: debug
* -dark: perform dark subtraction
* -dqi: update the DQ array
* -flat: perform flat correction
* -shad: perform shading correction
* -phot: perform phot correction
