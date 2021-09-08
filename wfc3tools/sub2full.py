"""
sub2full:

    Given an image specified by the user which contains a subarray readout,
    return the location of the corner of the subarray in a full frame reference
    image (including the full physical extent of the chip), in 1-indexed
    pixels. If the user supplies an X and Y coordinate, then the translated
    location of that point will be returned.

Usage:

    >>> from wfc3tools import sub2full
    >>> sub2full('ibbso1fdq_flt.fits')
    >>> [(3584.0, 1539)]

    Specify a list of images:

        >>> im = ['ic5p02e0q_spt.fits',
                'ic5p02e1q_spt.fits',
                'ic5p02e2q_spt.fits',
                'ic5p02e3q_spt.fits',
                'ic5p02e4q_spt.fits']

        >>> sub2full(im)
        >>> [(1062.0, 1363),
            (1062.0, 1363),
            (1410.0, 1243),
            (1410.0, 1243),
            (1402.0, 1539)]

    Return the full extent of the subarray:

        >>> sub2full('ibbso1fdq_flt.fits',fullExtent=True)
        >>> [(3584.0, 4096, 1539, 2050)]

"""

from __future__ import division, print_function

# STDLIB
from astropy.io import fits
import os
from stsci.tools import parseinput


def sub2full(filename, x=None, y=None, fullExtent=False):
    """
    PUT IN A SIMPLE EXPLANATION OF FUNCTION.

    Parameters
    ----------
    filename : str or list
        Input image name or list of image names. The rootname will be used to
        find the _SPT files in the same directory, the SPT file has all the
        necessary information for the transform.

    x : int, optional, default=None
        Specify an x coordinate in the subarray to translate. If an x and y are
        specified, the fullExtent option is turned off and only the translated
        x,y coords are returned.

    y : int, optional, default=None
        Specify a y coordinate in the subarray to translate. If an x and y are
        specified, the fullExtent option is turned off and only the translated
        x,y coords are returned.

    fullExtent : bool, optional, default=False
        If True, the returned values will include the full extent of the
        subarray in the reference image, for example: (x0,x1,y0,y1).

    Returns
    -------
    coords : list
        A list of tuples which specify the translated coordinates, either
        (x0,y0) for each image or the full extent sections.

    Examples
    --------
    >>> from wfc3tools import sub2full
    >>> filename = 'ibbso1fdq_flt.fits'
    >>> coords = sub2full(filename, x=None, y=None, fullExtent=False)

    """

    infiles, dummy_out = parseinput.parseinput(filename)
    if len(infiles) < 1:
        return ValueError("Please input a valid HST filename")

    coords = list()

    for f in infiles:
        spt = f[0:9] + '_spt.fits'
        uvis_x_size = 2051
        serial_over = 25.0
        ir_overscan = 5.0

        # open up our image files
        try:
            fd2 = fits.open(spt)
        except (ValueError, IOError) as e:
            raise ValueError('%s ' % (e))

        # check for required keywords and close the images
        try:
            detector = fd2[0].header['SS_DTCTR']
            subarray = fd2[0].header['SS_SUBAR']
            xcorner = int(fd2[1].header['XCORNER'])
            ycorner = int(fd2[1].header['YCORNER'])
            numrows = int(fd2[1].header['NUMROWS'])
            numcols = int(fd2[1].header['NUMCOLS'])
            fd2.close()
        except KeyError as e:
            raise KeyError("Required header keyword missing; %s" % (e))

        if "NO" in subarray:
            raise ValueError("Image is not a subarray: %s" % (f))

        sizaxis1 = numcols
        sizaxis2 = numrows

        if (xcorner == 0 and ycorner == 0):
            cornera1 = 0
            cornera2 = 0
            cornera1a = cornera1 + 1
            cornera1b = cornera1a + sizaxis1 - 1
            cornera2a = cornera2 + 1
            cornera2b = cornera2a + sizaxis2 - 1
        else:
            if 'UVIS' in detector:
                cornera1 = ycorner
                cornera2 = uvis_x_size - xcorner - sizaxis2
                if xcorner >= uvis_x_size:
                    cornera2 = cornera2 + uvis_x_size

                cornera1a = cornera1 + 1 - serial_over
                cornera1b = cornera1a + sizaxis1 - 1
                cornera2a = cornera2 + 1
                cornera2b = cornera2a + sizaxis2 - 1

                if cornera1a < 1:
                    cornera1a = 1
                if cornera1b > 4096:
                    cornera1b = 4096

            else:
                cornera1 = ycorner - ir_overscan
                cornera2 = xcorner - ir_overscan
                cornera1a = cornera1 + 1
                cornera1b = cornera1a + sizaxis1 - 11
                cornera2a = cornera2 + 1
                cornera2b = cornera2a + sizaxis2 - 11

        if (x or y):
            if ((not isinstance(x, int) or (not isinstance(y, int)))):
                raise ValueError("Must input integer value for x and y ")
            else:
                cornera1a = cornera1a + x
                cornera2a = cornera2a + y
                fullExtent = False

        if (fullExtent):
            coords.append((int(cornera1a), int(cornera1b), int(cornera2a),
                           int(cornera2b)))
        else:
            coords.append((int(cornera1a), int(cornera2a)))

    # return the tuple list of coordinates
    return coords

if __name__ == "main":
    """called from system shell, return the default corner locations """
    import sys
    sub2full(sys.argv[1])
