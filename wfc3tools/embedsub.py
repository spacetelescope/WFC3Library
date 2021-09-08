"""
embedsub:

    Given an image specified by the user which contains a subarray readout,
    return a full-frame image with the subarray implanted at the appropriate
    location.

Parameters:

    files [file]
        Input image name or list of image names. The rootname will be used to
        create the output name.

Returns:

    Return the full-frame location of the subarray coordinates using a file
    specified by the user.

"""

from __future__ import absolute_import, division, print_function

# get the auto update version
from .sub2full import sub2full

# STDLIB
from astropy.io import fits
import os
import numpy

# STSCI
from stsci.tools import parseinput


def embedsub(files):
    """
    Return the full-frame location of the subarray.

    The output file will contain the subarray image placed inside the full
    frame extent of a regular image.

    Parameters
    ----------
    files : str or list
        The name of the image file containing the subarray. This can be a
        single filename or a list of files. The ippsoot will be used to
        construct the output filename. You should input an FLT image.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import embedsub
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> embedsub(filename)

    """
    uvis = False
    uvis_full_x = 2051
    uvis_full_y = 4096
    ir_full = 1014

    infiles, dummy_out = parseinput.parseinput(files)
    if len(infiles) < 1:
        return ValueError("Please input a valid HST filename")

    # process all the input subarrays
    for filename in infiles:

        # Make sure the input name conforms to normal style
        if '_flt' not in filename:
            print("Warning: Can't properly parse '%s'; Skipping" % files)

        # Extract the root name and build SPT and output file names
        root = filename[0:filename.find('_flt')]
        full = root[0:len(root)-1] + 'f_flt.fits'

        try:
            flt = fits.open(filename)
        except EnvironmentError:
            print("Problem opening fits file %s" % (filename))

        detector = flt[0].header['DETECTOR']
        if 'UVIS' in detector:
            uvis = True

        # compute subarray corners assuming the raw image location
        x1, x2, y1, y2 = sub2full(filename, fullExtent=True)[0]
        print("Subarray image section [x1,x2,y1,y2] = [%d:%d,%d:%d]" % (x1, x2,
                                                                        y1, y2))

        if uvis:
            xaxis = uvis_full_x
            yaxis = uvis_full_y
        else:
            xaxis = ir_full
            yaxis = ir_full

        # Now copy the subarray image data into full-chip data arrays;
        # The regions outside the subarray will be set to zero in the
        # SCI, ERR, SAMP, and TIME extensions, and to DQ=4.
        sci = numpy.zeros([xaxis, yaxis], dtype=numpy.float32)
        err = numpy.zeros([xaxis, yaxis], dtype=numpy.float32)
        dq = numpy.zeros([xaxis, yaxis], dtype=numpy.int16) + 4

        sci[y1-1:y2, x1-1:x2] = flt[1].data
        err[y1-1:y2, x1-1:x2] = flt[2].data
        dq[y1-1:y2, x1-1:x2] = flt[3].data

        if not uvis:
            samp = numpy.zeros([xaxis, yaxis], dtype=numpy.int16)
            time = numpy.zeros([xaxis,yaxis],dtype=numpy.float32)
            samp[y1-1:y2, x1-1:x2] = flt[4].data
            time[y1-1:y2,x1-1:x2] = flt[5].data

        # Reset a few WCS values to make them appropriate for a
        # full-chip image
        crpix1 = flt[1].header['CRPIX1']
        crpix2 = flt[1].header['CRPIX2']

        flt[1].header['sizaxis1'] = yaxis
        flt[1].header['sizaxis2'] = xaxis

        for i in range(1, 4):
            flt[i].header['crpix1'] = crpix1 + x1 - 1
            flt[i].header['crpix2'] = crpix2 + y1 - 1
            flt[i].header['ltv1']  = 0.0
            flt[i].header['ltv2']  = 0.0

        # set the header value of SUBARRAY to False since it's now
        # regular size image
        flt[0].header['SUBARRAY'] = False

        # Now write out the SCI, ERR, DQ extensions to the full-chip file
        hdulist = fits.HDUList()
        hdulist.append(fits.ImageHDU(flt[0].data, header=flt[0].header))
        hdulist.append(fits.ImageHDU(sci, header=flt[1].header, name='SCI'))
        hdulist.append(fits.ImageHDU(err, header=flt[2].header, name='ERR'))
        hdulist.append(fits.ImageHDU(dq, header=flt[3].header, name='DQ'))

        if not uvis:
            hdulist.append(fits.ImageHDU(dq, header=flt[4].header, name='SAMP'))
            hdulist.append(fits.ImageHDU(dq, header=flt[5].header, name='TIME'))

        hdulist.writeto(full, clobber=False)

        # close the input files
        flt.close()
        print("Image saved to: %s" % (full))

if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    embedsub(sys.argv[1])
