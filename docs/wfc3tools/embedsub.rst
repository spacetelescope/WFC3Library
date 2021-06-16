.. _embedsub:

********
embedsub
********

Given an image specified by the user which contains a subarray readout, return a full-frame image with the subarray implanted at the appropriate location.

Usage
=====

.. code-block:: python

    python
    from wfc3tools import embedsub
    embedsub(files)


Parameters
==========

    files [file]
        Input image name or list of image names. The rootname will be used to create the output name.



Returns
=======
Return the full-frame location of the subarray coordinates using a  file specified by the user.


Example Output
==============

This method calls wfc3tools.sub2full to calculation the subarray position on the full frame image.

This is the default output:

::

    wfc3tools.embedsub.embedsub('ic5p02eeq_flt.fits')
    Subarray image section [x1,x2,y1,y2] = [2828:3339,215:726]
    Image saved to: ic5p02eef_flt.fits
