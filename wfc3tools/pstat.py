"""
pstat:

    Plot statistics for a specified image section up the stack of an IR
    MultiAccum image.  Sections from any of the SCI, ERR, DQ, image extensions
    can be plotted.  A choice of  mean, median, mode, standard deviation,
    minimum, and maximum statistics is available. The total number of samples is
    determined from the primary header keyword NSAMP and all samples (excluding
    the zeroth-read) are plotted. The SCI, ERR, DQ statistics are plotted as a
    function of sample time. The sample times are read from the SAMPTIME
    keyword in the SCI header for each readout.

    SAMP and TIME aren't generally populated until the FLT image stage. To plot
    the samptime vs sample, use wfc3tools.pstat and the "time" extension.

Usage:

    >>> from wfc3tools import pstat
    >>> time, counts = pstat('ibh719grq_ima.fits')
    >>> time
    array([ 100.651947,   93.470573,   86.2892  ,   79.107826,   71.926453,
             64.745079,   57.563702,   50.382328,   43.200954,   36.019581,
             28.838205,   21.65683 ,   14.475455,    7.29408 ,    0.112705,
              0.      ])
    >>> counts
    array([ 171.85813415,  162.44643275,  148.99918831,  137.60458714,
            125.91510743,  114.71149769,  102.63038466,   90.97130078,
             78.26479365,   67.16825321,   53.6897243 ,   41.71639092,
             29.36628817,   16.47151355,   -0.20821257,    0.        ])

Warning:

    Note that the arrays are structured in SCI order, so the final exposure is the first element in the array.

"""

from __future__ import division, print_function

# STDLIB
import os
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import mode as mode

plt.ion()


def pstat(filename, extname="sci", units="counts", stat="midpt", title=None,
          xlabel=None, ylabel=None, plot=True, overplot=False):
    """
    A function to plot the statistics of one or more pixels up an IR ramp.

    Parameters
    ----------
    filename : str
       Input MultiAccum image name with optional image section
       specification.  If no image section is specified, the entire image
       is used.  This should be either a _raw or _ima file, containing all
       the data from multiple readouts.  You must specify just the
       file name and image section, with no extname designation.

    extname :  str, default="sci"
       Extension name (EXTNAME keyword value) of data to plot. Allowed values
       are "sci", "err", and "dq".

    units : str, default="counts"
       Plot "sci" or "err" data in units of counts or countrate
       ("rate").  Input data can be in either unit; conversion will be
       performed automatically.  Ignored when plotting "dq", "samp", or
       "time" data. Allowed values are "counts" and "rate".

    stat : str, default="midpt"
       Type of statistic to compute. Allowed values are "mean", "midpt",
       "mode", "stddev", "min", and "max".

    title : str, default=None
       Title for the plot.  If left blank, the name of the input image,
       appended with the extname and image section, is used.

    xlabel : str, default=None
       Label for the X-axis of the plot.  If left blank, a suitable default
       is generated.

    ylabel : str, default=None
       Label for the Y-axis of the plot. If left blank, a suitable default
       based on the plot units and the extname of the data is generated.

    plot : bool, default=True
       If False, return data and do not plot.

    overplot : bool, default=False
       If True, the results will be overplotted on the previous plot.

    Returns
    -------
    xaxis : numpy.ndarray
       Array of x-axis values that will be plotted.

    yaxis : numpuy.ndarray
       Array of y-axis values that will be plotted as specified by 'units'.

    Notes
    -----
    Pixel values here are 0 based, not 1 based.

    Examples
    --------
    >>> from wfc3tools import pstat
    >>> time, counts = pstat('ibh719grq_ima.fits')

    """

    # pull the image extension from the filename string
    section_start = filename.find("[")
    all_pixels = False
    if (section_start < 0):
        all_pixels = True  # just give the data to np
        imagename = filename
    elif (section_start > 0):
        imagename = filename[:section_start]
        if (filename[section_start+1].isalpha()):
            print(filename[section_start+1])
            print("Please only specify a pixel range, not an extension \
                   in the filename")
            return 0, 0

    # check for a valid stat value
    valid_stats = ["midpt", "mean", "mode", "stddev", "min", "max"]
    if stat not in valid_stats:
        print("Invalid value given for stat: %s" % (valid_stats))
        return 0, 0

    valid_ext = ["sci", "err", "dq"]
    if extname.lower() not in valid_ext:
        print("Invalid value given for extname: %s" % (valid_ext))
        return 0, 0

    # use the entire image if no section specified
    if not all_pixels:
        # pull the section off
        section = filename[section_start+1:-1]
        comma = section.find(",")
        xsec = section[:comma]
        ysec = section[comma+1:]
        xs = xsec.find(":")
        if xs < 0:
            print("Invalid image section specified")
            return 0, 0
        try:
            xstart = int(xsec[: xs])
        except ValueError:
            print("Problem getting xstart")
            return
        try:
            xend = int(xsec[xs+1:])
        except ValueError:
            print("Problem getting xend")
            return

        ys = ysec.find(":")
        if (ys < 0):
            print("Invalid image section specified")
            return 0, 0
        try:
            ystart = int(ysec[:ys])
        except ValueError:
            print("Problems getting ystart")
            return
        try:
            yend = int(ysec[ys+1:])
        except ValueError:
            print("Problem getting yend")
            return

    with fits.open(imagename) as myfile:
        nsamp = myfile[0].header["NSAMP"]
        bunit = myfile[1].header["BUNIT"]  # must look at header for units
        yaxis = np.zeros(nsamp)
        xaxis = np.zeros(nsamp)

        if all_pixels:
            xstart = 0
            ystart = 0
            xend = myfile[1].header["NAXIS1"]  # full x size
            yend = myfile[1].header["NAXIS2"]  # full y size

        for i in range(1, nsamp, 1):
            if "midpt" in stat:
                yaxis[i-1] = np.median(myfile[extname.upper(), i].data[xstart:xend, ystart:yend])

            if "mean" in stat:
                yaxis[i-1] = np.mean(myfile[extname.upper(), i].data[xstart:xend, ystart:yend])

            if "mode" in stat:
                yaxis[i-1] = mode(myfile[extname.upper(),i].data[xstart:xend, ystart:yend],
                                    axis=None)[0]

            if "min" in stat:
                yaxis[i-1] = np.min(myfile[extname.upper(), i].data[xstart:xend, ystart:yend])

            if "max" in stat:
                yaxis[i-1] = np.max(myfile[extname.upper(), i].data[xstart:xend, ystart:yend])

            if "stddev" in stat:
                yaxis[i-1] = np.std(myfile[extname.upper(), i].data[xstart:xend, ystart:yend])

            exptime = myfile["SCI", i].header['SAMPTIME']
            xaxis[i-1] = exptime

            # convert to countrate
            if "rate" in units.lower() and "/" not in bunit.lower():
                yaxis[i-1] /= exptime
            # convert to counts
            if "counts" in units.lower() and "/" in bunit.lower():
                yaxis[i-1] *= exptime

    if plot:
        if not overplot:
            plt.clf()  # clear out any current plot
        if not ylabel:
            if "rate" in units.lower():
                if "/" in bunit.lower():
                    ylabel = bunit
                else:
                    ylabel = bunit + " per second"
            else:
                if "/" in bunit:
                    stop_index = bunit.find("/")
                    ylabel = bunit[:stop_index]
                else:
                    ylabel = bunit

        ylabel += ("   %s" % (stat))
        plt.ylabel(ylabel)

        if not xlabel:
            plt.xlabel("Sample time (s)")

        if not title:
            title = "%s   Pixel stats for [%d:%d,%d:%d]" % (filename, xstart,
                                                            xend, ystart, yend)
        plt.title(title)
        plt.plot(xaxis, yaxis, "+")
        plt.draw()

    return xaxis, yaxis

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    pstat(sys.argv[1])
