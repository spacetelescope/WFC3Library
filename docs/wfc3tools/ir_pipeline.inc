.. _ir_pipeline:


IR Pipeline
===========

IR pipeline output files using the RAW file as input:

    * **flt.fits**: output calibrated, ramp-fitted exposure produced after CRCORR has been run
    * **ima.fits**: output ramp calibrated exposure. Remember that the signal rate recorded in each SCI extension of the ima file represents the average flux between that particular readout and the zero read.
    * **_crj.fits**: a cosmic-ray rejected sub-product produced from images in an association table
    * **.tra**: output text information about the processing


.. _irflow:

.. figure:: ../_static/wfc3_Ch33_5.png
    :align: center
    :alt: Flow diagram for IR data using wf3ir in calwf3

    Flow diagram for IR data using wf3ir in calwf3


Data Quality Initialization (DQICORR)
-------------------------------------

Initialize the data quality array for the image using the reference file specified in its header with BPIXTAB. The DQ array is no longer updated to reflect any TDF transition during the sample. If you want to update DQ pixel values yourself before running further processing, do it after this first step has been completed, remembering that the data in this extension is always in units of UNSIGNED INTEGER. The following table lists the DQ flag values and their meanings:


=============== ======  =======================================================
NAME            VALUE   DESCRIPTION
=============== ======  =======================================================
GOODPIXEL        0      OK
SOFTERR          1      Reed-Solomon decoding error
DATALOST         2      data replaced by fill value
DETECTORPROB     4      bad detector pixel or beyond aperture
DATAMASKED       8      masked by occulting bar
BADZERO          8      deviant IR zero-read pixel
HOTPIX           16     hot pixel
UNSTABLE         32     IR unstable pixel
WARMPIX          64     warm pixel
BADBIAS          128    bad bias value
SATPIXEL         256    full-well or a-to-d saturated pixel
BADFLAT          512    bad flatfield value
SPIKE            1024   CR spike detected during cridcalc IR
ZEROSIG          2048   IR zero-read signal correction
ne TBD           4096   reserved for Multidrizzle CR rej
DATAREJECT       8192   rejected during image combination UVIS, IR CR rejection
HIGH_CURVATURE   16384  pixel has more than max CR's
RESERVED2        32768  can't use
=============== ======  =======================================================


Estimate the signal in the zero read (ZSIGCORR)
-----------------------------------------------

This step measures the signal between the super zero read in the linearity reference file (NLINFILE) and the science zero read exposure, the steps are roughly as follows:

* copy the zero sig image from the linearity reference file
* compute any subarray offsets
* subtract the super zero read reference image from the zero read science image
* compute the noise in the zero image
* pixels which contain more than ZTHRESH*noise of detected signal are flagged and that signal is passed to the NLINCORR step to help judge saturation and linearity, avoiding reference pixels.
* low signal pixels are masked out by setting them to zero
* the NLINCOR file has an extension with saturation values for each pixel which is referenced here. Pixels which are saturated in the zeroth or first reads are flagged in the DQ and the number of found saturated pixels are reported.
* This step works poorly for bright targets which are already begining to saturate in the zeroth and first reads
* This step acutally subtractes the super zero read from the science zero read instead of calculating an estimated signal based on the first read and zero read + estimated exposure time between them so that the difference in readout time for subarrays is not an issue.

Bias Correction (BLEVCORR)
--------------------------

This step subtracts the bias level using the reference pixels around the perimeter of the detector, the boundries fo the reference pixels are defined in the OSCNTAB reference file. There are 5 reference pixels on each end of each row, but 1 is ignored on each side, for a total of 8 being used per row. The resistent mean of the standard deviation of all the reference pixels in the image is subtracted from the entire image and the value is stored in the MEANBLEV keyword in the output image header. The reference pixels are left in place in the IMA output image through processeing, but the final FLT image has been trimmed to just the science pixels.


Zero read subtraction (ZOFFCORR)
--------------------------------

The original zero read is subtracted from all groups in the science image, including the zeroth read itself, combining the DQ arrays with a logical OR. The ERR and SAMP arrays are unchanged and the TIME arrays are subtracted from each other. The exposure time for the group being corrected is reduced by an amount equal to the exposure time of the zero-read. At this point we've subtracted the mean bias using the reference pixels (BLEVCORR) and added back in the signal from the super zero read (done at the end of ZSIGCORR). What's left in the zero read of the science image is the superbias subtracted signal. The TIME and SAMP arrays are saved to the FLT image only AFTER the CRCORR step has been completed.


Error array initialization
--------------------------

The errors associated with the raw data are estimated according  to the noise model for the detector which currently includes a simple combination of detector readnoise and poisson noise from the pixel. Readnoise and gain are read from the CCDTAB reference file. The ERR array continues to be summed in quadrature as the SCI array is processed. Inside the final FLT image, the ERR array is calculated by CRCORR as the calculated uncertainty of the count-rate fit to the multiaccum samples.

.. math::

        \sigma_{IR} = \frac{\sqrt{(readnoise^{2}) + (counts * gain)}}{gain}


Detector Non-linearity Correction (NLINCORR)
--------------------------------------------

The integrated counts in the science images are corrected for the  non-linear response of the detectors, flagging pixels which extend into saturation (as defined in the saturation extension of the NLINFILE reference image. The observed response of the detector can be represented by two regimes:

* At low and intermediate signal levels the detector response deviates from the incident flux in a way that is correctable using the following expression

.. math::

        F_{c} = (1 + c_{1} + c_{2} \times F + c_{3}\times F^{2} + c_{4} \times F^{3}) \times F

where c1, c2, c3, and c4 are the correction coefficients, F is the uncorrected flux in DN and :math:`F_{c}` is the corrected flux. The current form of the correction uses a third-order polynomial, but the algoritm can handle an arbitrary number of coefficients. The number of coefficients and error terms are given by the values of the NCOEFF and NERR keywords in the header of the NLINFILE.

* At high signal levels, as saturation sets in, the response becomes highly non-linear and is not correctable to a scientifically useful degree.

The signal in the zero read is temporarily added back to the zeroth read image of the science data before the linearity correction is applied and before the saturation is judged. Once the correction has been applied the signal is once again removed. This only occurs if the ZSIGCORR step is set to PERFORM. Saturation values for each pixel are stored in the NODE extension of the NLINFILE. After each group is corrected, the routine also sets saturation flags in the next group for those pixels that are flagged as saturated in the current group. This is necessary because the SCI image value of saturated pixels will sometimes start to go back down in the subsequent reads after saturation occurs, which means they could go unflagged by normal checking techniques. The SAMP and TIME arrays are not modified during this step.

The format of the linearity reference file:


::

        EXT#  FITSNAME      FILENAME              EXTVE DIMENS       BITPI OBJECT

        0     u1k1727mi_lin u1k1727mi_lin.fits                       -32
        1       IMAGE       COEF                  1     1024x1024    -32
        2       IMAGE       COEF                  2     1024x1024    -32
        3       IMAGE       COEF                  3     1024x1024    -32
        4       IMAGE       COEF                  4     1024x1024    -32
        5       IMAGE       ERR                   1     1024x1024    -32
        6       IMAGE       ERR                   2     1024x1024    -32
        7       IMAGE       ERR                   3     1024x1024    -32
        8       IMAGE       ERR                   4     1024x1024    -32
        9       IMAGE       ERR                   5     1024x1024    -32
        10      IMAGE       ERR                   6     1024x1024    -32
        11      IMAGE       ERR                   7     1024x1024    -32
        12      IMAGE       ERR                   8     1024x1024    -32
        13      IMAGE       ERR                   9     1024x1024    -32
        14      IMAGE       ERR                   10    1024x1024    -32
        15      IMAGE       DQ                    1     1024x1024    -32
        16      IMAGE       NODE                  1     1024x1024    -64
        17      IMAGE       ZSCI                  1     1024x1024    -32
        18      IMAGE       ZERR                  1     1024x1024    -32



Dark Current Subtraction (DARKCORR)
-----------------------------------

The reference file listed under the DARKFILE header keyword is used to subtract the dark current from each sample. Due to potential non-linearities in some of the signal components, such as reet-related effecets in the first one or two reads of an exposure, the dark current subtraction is not aplied by simply scaling a generic reference dark image to the exposure time and then subtracting it. Instead, a library of dark current images is maintained that includes darks taken in each of the available predefined multiaccum sample sequences, as well as the available sub-array readout modes. The multiaccum dark reference file is subtracted read-by-read from the stack of science image readouts so that there is an exact match in the timings and other characteristics of the dark image and the science image. The subtraction does not include the reference pixel. The ERR and DQ arrays from the reference dark file are combined with the SCI and DQ arrays from the science image, but the SAMP and TIME arrays are unchanged. The mean of the dark image is saved to the MEANDARK keyword in the output science image header.



Photometry Keywords (PHOTCORR)
------------------------------

The PHOTCORR step is performed using tables of precomputed values instead of calls  to SYNPHOT. The correct table for a given image must be specified in the IMPHTTAB header keyword in order for calwf3 to perform the PHOTCORR step. The format of the file for the IR detectors is:

::

        EXT#  FITSNAME      FILENAME              EXTVE DIMENS       BITPI OBJECT

        0     wbj1825ri_imp wbj1825ri_imp.fits                       16
        1       BINTABLE    PHOTFLAM              1     5Fx38R
        2       BINTABLE    PHOTPLAM              1     5Fx38R
        3       BINTABLE    PHOTBW                1     5Fx38R

where each extension contains the photometry keyword information for that specific header keyword. The rows in the tables are split on observation mode.


* PHOTFLAM: the inverse sensistiy in units of :math:`ergs\ cm^{-2} A^{-1} electron^{-1}`
* PHOTPLAM: the bandpass pivot wavelength
* PHOTBW: the bandpass RMS width

Conversion to Signal Rate (UNITCORR)
------------------------------------

This step converts the science data from a time-integrated signal to a signal rate by dividing the SCI and ERR arrays for reach readout by the TIME array. No reference file is needed. The BUNIT keyword in the output data header reflects the appropriate data units. The FLATCORR keyword is checked to decide on  proper units for BUNIT and skip this step if "countrate" is found. If FLATCORR is set to "complete", then the units should be electrons, otherwise they are counts (the digitized signal from the FPA).



Fit accumulating signal and identify cosmic ray hits (CRCORR)
-------------------------------------------------------------

This step fits the accumulating signal up the image ramp and identifies cosmic-ray hits for each sample using the `Fixsen et al (2000) <http://adsabs.harvard.edu/abs/2000PASP..112.1350F>`_  methods.

.. note::

        With the release of `calwf3 v3.3`, the WFC3 Science Team requested that HST Data Processing also change the way IR SCAN data was processed in the pipeline. Specifically, that data processing set the value of CRCORR to OMIT.  CALWF3 performs up-the-ramp fitting during the CRCORR step, which for scan data  produces a minimally useful result. Setting CRCORR=OMIT stops the ramp fit from happening and instead produces an FLT output image which contains the first-minus-last read result. This by nature is not a count-rate image, but a count image if UNITCORR = OMIT. UNITCORR converts the image to count rates.  Additionally, if  FLATCORR is set to complete then the output units should be in electrons, otherwise they are in counts.



The ramp-fitting process is described below:


* An iterative fit to the accumulating sample time is calculated for each pixel
    * Finding a cosmic ray ends one interval and beins the next; the cosmic ray must be included in the next interval
        * intervals are first defined based on existing cosmic rays
            * CRSIGMAS from the  CRREJTAB reference file is used to set the rejection threshold
        * then each interval is fitted separately
        * then each interval is inspected for SPIKES
        * then each interval is inspected for more cosmic rays
    * If any SPIKES or cosmic rays are found then the entire procedure repeats, new intervals are defined, etc ...
    * After the iteration ends because no new SPIKES or cosmic rays are found, each interval is fitted separately once again, with optimum weighting, and then the results for each interval are combined to obtain  the final solution for the pixel.
    * The linearity fit includes readnoise in the sample weights and Poisson noise from the source in the final fit uncertainty
    * negative cosmic ray hits are detected and detected SPIKES have their 1024 bit flipped in the DQ extension
    * If the first read is saturated the output pixels are never zeroed out
        * The output pixel values in this case are the value in the input zeroth read image, regardless of whether the zero-read image was saturated. If it is saturated in the zero-read, the DQ flag will get carried over to the outpu DQ array to indicate that it's bad.

    * The DATAREJECT DQ flag is set for all samples following a hit. This is done so that anyone looking at the IMA file will know that the absolute value of the pixel is wrong after the firs t hit, but it smears the location of any hits which occurred in addition to the first one.
    * Pixels in the DQ image of the output IMA file are flagged with a value of 8192, the SCI and ERR image arrays are left unchanged
    * DQ values from any sample are carried through to the output pixel if a pixel has no good samples
* The UNSTABLE DQ flag is used to record pixels with higher than max allowed cosmic ray hits recorded.

The result of this step  is stored as a single imset in the output FLT file. In the FLT file, the SCI array contains the final slope computed for each pixel, the ERR array contains the estimated uncertainty in the slope, the SAMP array contains the number of non-flagged samples used to compute the slope, and the TIME array contains the total exposure time of those smaples. Pixels for which no unflagged sample exisists (dead pixels for example) still get a slope computed which is recorded in the SCI array of the output FLT image, but the DQ flags in the FLT will reflect their bad status.


Flatfield Correction (FLATCORR)
-------------------------------

This step corrects for sensativity variations across the detector by dividing the images by one or more reference flatfields (taken from the PFLTFILE, DFLTFILE or LFLTFILE header keywords). The mean gain from all the amps is used to convert to the image to units of electrons. Errors and DQ flags from the flatfields are combined with the science data errors and flag, the TIME and SAMP arrays are unchanged.


Calculation of image statistics
-------------------------------

The min, mean, maxmin and max SNR (for the SCI and ERR) for data values flagged as "good" in the DQ array (i.e. zero) are calculated and stored in the output SCI image header, the reference pixels are not used. This is performed for all samples in the IMA file as well as the FLT image but the input data is not modified in any way. Updated keywords in the science header include:

* NGOODPIX
* GOODMEAN
* GOODMIN
* GOODMAX
* SNRMEAN
* SNRMIN
* SNRMAX


Reject cosmic rays from multiple images (RPTCORR)
-------------------------------------------------
Reject cosmic rays from multiple images. REPEAT-OBS exposures get combined with :ref:`wf3rej`. The task uses the same statistical detection algorithm developed for ACS (acsrej), STIC (ocrrj) and WFPC2(crrej), providing a well-tested and robust procedure. CR-SPLIT is not used for the IR channel. All dithered observation get combined with Astrodrizzle  (see `Astrodrizzle <http://www.stsci.edu/hst/HST_overview/drizzlepac/>`_ ), which will also correct for geometric distortion.

.. warning::

     All WFC3 observations, not just dithered images, need to be processed with AstroDrizzle to correct for geometric distortion and pixel area effects.
