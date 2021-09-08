.. _sampinfo:

********
sampinfo
********

Sampinfo prints information about a  WFC3/IR  MultiAccum image,  including  exposure  time  information  for  the  individual samples (readouts).
The global information listed  (and  the  names of  the  header  keywords  from  which it is retrieved) includes:

* the total number of image extensions in the file (NEXTEND)
* the name  of the  MultiAccum  exposure  sample  sequence  (SAMP_SEQ)
* the  total number of samples, including the  "zeroth"  read  (NSAMP)
* the total  exposure  time of the observation (EXPTIME).

Information that is listed for each sample is the IMSET number (EXTVER),  the  sample number  (SAMPNUM),  the  sample time, which is the total accumulated exposure time for a sample (SAMPTIME),
and the delta time, which  is the  additional  exposure time accumulated since the previous sample (DELTATIM).

Note that the samples of a MultiAccum exposure  are  stored  in  the FITS  file  in  reverse  time  order. The initial, or "zeroth" read, appears  last  in  the  FITS  file,
with  IMSET=NSAMP,   SAMPNUM=0, SAMPTIME=0,  and  DELTATIM=0. The final read of the exposure appears first in the file  and  has  IMSET=1,  SAMPNUM=NSAMP-1  (SAMPNUM  is zero-indexed), and SAMPTIME=EXPTIME.


Parameters
==========

* imagelist : str or list
    The input can be a single image or list of images.

* add_keys : list, default=None
    A list of of additional keys for printing. If a key is not found in
    the sample, the global header will be checked. If a key is not found, the "NA" string will be printed.

* mean : bool, default=False
    If True, print the mean statistic.

* median : bool, default=False
    If True, print the median statistic.

Returns
=======

None


Usage
=====

.. code-block:: python

    from wfc3tools import sampinfo
    sampinfo(imagename)

Where imagename can be a single filename or a Python list() of names

To get the median value for each sample:

.. code-block:: python

    sampinfo(imagename, median=True)

To print additional keys for information:

.. code-block:: python

    sampinfo(imagename,add_keys=["DETECTOR"])

To get the average value for each sample:

.. code-block:: python

    sampinfo(imagename, mean=True)

Example Output
==============

Default output:

::

    In [3]: wfc3tools.sampinfo('ibcf02faq_raw.fits')
    IMAGE			NEXTEND	SAMP_SEQ	NSAMP	EXPTIME
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

Optional output:

::

    In [4]: wfc3tools.sampinfo('ibcf02faq_raw.fits',median=True)
    IMAGE			NEXTEND	SAMP_SEQ	NSAMP	EXPTIME
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
