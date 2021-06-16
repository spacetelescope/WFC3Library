from __future__ import division, print_function

# get the auto update version
from .version import __version_date__, __version__

# STDLIB
import os
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import mode as mode

# STSCI
from stsci.tools import teal

__taskname__ = "pstat"

plt.ion()


def pstat(filename, extname="sci", units="counts", stat="midpt", title=None,
          xlabel=None, ylabel=None, plot=True, overplot=False):
    """A function to plot the statistics of one or more pixels up an IR ramp.

    Parameters
    ----------
    filename: string
       Input   MultiAccum   image  name  with  optional  image  section
       specification.  If no image section  is  specified,  the  entire image
       is  used.   This  should  be  either a _raw or _ima file, containing all
       the  data  from  multiple  readouts.   You  must specify  just  the
       file name and image section, with no extname designation.

    extname:  {"sci", "err", "dq"}
       Extension name (EXTNAME keyword value) of data to plot.

    units: {"counts", "rate"}
       Plot "sci" or  "err"  data  in  units  of  counts  or  countrate
       ("rate").   Input data can be in either unit; conversion will be
       performed automatically.  Ignored when  plotting  "dq",  "samp", or
       "time" data.

    stat: { "mean", "midpt", "mode", "stddev", "min", "max"}
       Type of statistic to compute.

    title: str
       Title  for  the  plot.   If  left  blank,  the name of the input image,
       appended with the extname and image section, is used.

    xlabel: str
       Label for the X-axis of the plot.  If  left  blank,  a  suitable default
       is generated.

    ylabel: str
       Label  for  the  Y-axis  of  the plot. If left blank, a suitable default
       based on the plot units and the extname of the  data  is generated.

    plot: Bool
       Set plot to false if you only want the data returned

    overplot: Bool
       If True, the results will be overplotted on the previous plot

    Returns
    -------
    xaxis: numpy.ndarray
       Array of x-axis values that will be plotted

    yaxis: numpuy.ndarray
       Array of y-axis values that will be plotted as specified by 'units'


    Notes
    -----
    Pixel values here are 0 based, not 1 based
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


def getHelpAsString(docstring=False):
    """Return documentation on the 'wf3ir' function. Required by TEAL."""

    install_dir = os.path.dirname(__file__)
    htmlfile = os.path.join(install_dir, 'htmlhelp', __taskname__ + '.html')
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    if docstring or (not docstring and not os.path.exists(htmlfile)):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __version_date__]) + '\n\n'
        if os.path.exists(helpfile):
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
    else:
        helpString = 'file://' + htmlfile

    return helpString


def help(file=None):
    """
    Print out syntax help for running wf3ir

    """

    helpstr = getHelpAsString(docstring=True)
    if file is None:
        print(helpstr)
    else:
        if os.path.exists(file):
            os.remove(file)
        f = open(file, mode='w')
        f.write(helpstr)
        f.close()


pstat.__doc__ = getHelpAsString(docstring=True)
