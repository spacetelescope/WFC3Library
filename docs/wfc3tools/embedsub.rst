.. _embedsub:

********
embedsub
********

Given an image specified by the user which contains a subarray readout, return a full-frame image with the subarray implanted at the appropriate location.


Parameters
==========

* files : str or list
    The name of the image file containing the subarray. This can be a
    single filename or a list of files. The ippsoot will be used to
    construct the output filename. You should input an FLT image.


Returns
=======

* None


Usage
=====

.. code-block:: python

    from wfc3tools import embedsub
    embedsub(files)


Example Output
==============

This method calls wfc3tools.sub2full to calculation the subarray position on the full frame image.

.. code-block:: python

    embedsub('ic5p02eeq_flt.fits')
    Subarray image section [x1,x2,y1,y2] = [2828:3339,215:726]
    Image saved to: ic5p02eef_flt.fits
