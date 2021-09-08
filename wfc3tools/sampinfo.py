"""
sampinfo:

    Sampinfo prints information about a WFC3/IR MultiAccum image, including
    exposure time information for the individual samples (readouts). The global
    information listed (and the names of the header keywords from which it is
    retrieved) includes:

        - the total number of image extensions in the file (NEXTEND)
        - the name  of the  MultiAccum  exposure  sample  sequence  (SAMP_SEQ)
        - the  total number of samples, including the  "zeroth"  read  (NSAMP)
        - the total  exposure  time of the observation (EXPTIME)

    Information that is listed for each sample is the IMSET number (EXTVER), the
    sample number (SAMPNUM), the sample time, which is the total accumulated
    exposure time for a sample (SAMPTIME), and the delta time, which is the
    additional exposure time accumulated since the previous sample (DELTATIM).

    Note that the samples of a MultiAccum exposure are stored in the FITS file
    in reverse time order. The initial, or "zeroth" read, appears last in the
    FITS file, with IMSET=NSAMP, SAMPNUM=0, SAMPTIME=0, and DELTATIM=0. The
    final read of the exposure appears first in the file and has IMSET=1,
    SAMPNUM=NSAMP-1 (SAMPNUM is zero-indexed), and SAMPTIME=EXPTIME.

Usage:

    >>> from wfc3tools import sampinfo
    >>> sampinfo('ibcf02faq_raw.fits')
    >>> IMAGE			NEXTEND	SAMP_SEQ	NSAMP	EXPTIME
        ibcf02faq_raw.fits	80	STEP50		16	499.234009

        IMSET	SAMPNUM	SAMPTIME	DELTATIM
        1	15	499.234009	50.000412
        2	14	449.233582	50.000412
        3	13	399.233154	50.000412
        4	12	349.232727	50.000412
        5	11	299.2323	50.000412
        6	10	249.231873	50.000412
        7	9	199.231461	50.000412
        8	8	149.231049	50.000412
        9	7	99.230637	50.000412
        10	6	49.230225	25.000511
        11	5	24.229715	12.500551
        12	4	11.729164	2.932291
        13	3	8.796873	2.932291
        14	2	5.864582	2.932291
        15	1	2.932291	2.932291
        16	0	0.0	0.0

    Include median:
    
        >>> sampinfo('ibcf02faq_raw.fits',median=True)
        >>> IMAGE			NEXTEND	SAMP_SEQ	NSAMP	EXPTIME
            ibcf02faq_raw.fits	80	STEP50		16	499.234009

            IMSET	SAMPNUM	SAMPTIME	DELTATIM
            1	15	499.234009	50.000412	MedPixel: 11384.0
            2	14	449.233582	50.000412	MedPixel: 11360.0
            3	13	399.233154	50.000412	MedPixel: 11335.0
            4	12	349.232727	50.000412	MedPixel: 11309.0
            5	11	299.2323	50.000412	MedPixel: 11283.0
            6	10	249.231873	50.000412	MedPixel: 11256.0
            7	9	199.231461	50.000412	MedPixel: 11228.0
            8	8	149.231049	50.000412	MedPixel: 11198.0
            9	7	99.230637	50.000412	MedPixel: 11166.0
            10	6	49.230225	25.000511	MedPixel: 11131.0
            11	5	24.229715	12.500551	MedPixel: 11111.0
            12	4	11.729164	2.932291	MedPixel: 11099.0
            13	3	8.796873	2.932291	MedPixel: 11097.0
            14	2	5.864582	2.932291	MedPixel: 11093.0
            15	1	2.932291	2.932291	MedPixel: 11090.0
            16	0	0.0	0.0	MedPixel: 11087.0

"""

from __future__ import absolute_import, print_function, division

# STDLIB
from astropy.io import fits
import os
import numpy as np

# STSCI
from stsci.tools import parseinput


def sampinfo(imagelist, add_keys=None, mean=False, median=False):
    """
    Print information for each sample in the image.

    Parameters
    ----------
    imagelist : str or list
        The input can be a single image or list of images.

    add_keys : list, default=None
        A list of of additional keys for printing. If a key is not found in
        the sample, the global header will be checked. If a key is not found, the "NA" string will be printed.

    mean : bool, default=False
        If True, print the mean statistic.

    median : bool, default=False
        If True, print the median statistic.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import sampinfo
    >>> imagename = 'ibcf02faq_raw.fits'
    >>> sampinfo(imagename)

    To get the median value for each sample:
        >>> sampinfo(imagename, median=True)

    To print additional keys for information:
        >>> sampinfo(imagename,add_keys=["DETECTOR"])

    To get the average value for each sample:
        >>> sampinfo(imagename, mean=True)

    """

    datamin = False
    datamax = False
    imlist = parseinput.parseinput(imagelist)

    # the default list of keys to print, regardless of detector type
    ir_list = ["SAMPTIME", "DELTATIM"]
    if add_keys:
        ir_list += add_keys

    # measure the min and max data
    if (mean):
        if (add_keys):
            if ("DATAMIN" not in add_keys):
                ir_list += ["DATAMIN"]
            if ("DATAMAX" not in add_keys):
                ir_list += ["DATAMAX"]
        else:
            ir_list += ["DATAMIN", "DATAMAX"]

    for image in imlist[0]:
        current = fits.open(image)
        header0 = current[0].header
        nextend = header0["NEXTEND"]
        try:
            nsamp = header0["NSAMP"]
        except KeyError as e:
            print(str(e))
            print("Task good for IR data only")
            break
        exptime = header0["EXPTIME"]
        samp_seq = header0["SAMP_SEQ"]

        print("IMAGE\t\t\tNEXTEND\tSAMP_SEQ\tNSAMP\tEXPTIME")
        print("%s\t%d\t%s\t\t%d\t%f\n" % (image, nextend, samp_seq,
                                          nsamp, exptime))
        printline = "IMSET\tSAMPNUM"

        for key in ir_list:
            printline += ("\t"+key)
        print(printline)

        # loop through all the samples for the image and print stuff as we go
        for samp in range(1, nsamp+1, 1):
            printline = ""
            printline += str(samp)
            printline += ("\t"+str(nsamp-samp))
            for key in ir_list:
                if "DATAMIN" in key:
                    datamin = True
                    dataminval = np.min(current["SCI", samp].data)
                if "DATAMAX" in key:
                    datamax = True
                    datamaxval = np.min(current["SCI", samp].data)
                try:
                    printline += ("\t"+str(current["SCI", samp].header[key]))
                except KeyError:
                    try:
                        printline += ("\t"+str(current[0].header[key]))
                    except KeyError as e:
                        printline += ("\tNA")
            if (datamin and datamax):
                printline += ("\tAvgPixel: "+str((dataminval+datamaxval)/2.))
            if (median):
                printline += ("\tMedPixel: "+str(np.median(current["SCI",
                                                           samp].data)))
            print(printline)
        current.close()

#check to see if this makes sense
if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    sampinfo(sys.argv[1])
