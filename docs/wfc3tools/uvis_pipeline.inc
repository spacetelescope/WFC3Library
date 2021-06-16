.. _uvis_pipeline:


UVIS Pipleline
==============


.. _calflow:

.. figure:: ../_static/calwf3_flow.png
    :align: center
    :alt: Flow diagram for ``calwf3`` data using

    Flow diagram for ``calwf3`` data. :ref:`wf3cte` occurs as the very first step, before :ref:`wf3ccd`.

As of `calwf3 v3.3`, the calwf3 pipeline processes all UVIS data twice, once with the CTE correction applied as the first step, and a second time without the CTE correction. A short description of the calibration steps, in the order they are performed:

* Calculate and remove and CTE found in the image (PCTECORR)
* Calculate a noise model for each pixel and record in the error array (ERR) of the image (NOISCORR)
* Initialize the data quality(DQ) array of the image (DQICORR)
* Correct fo A-toD conversion errors where necessary, currently skipped (ATODCORR)
* Subtract bias level determined from overscan regions (BLEVCORR)
* Subtract the bias image (BIASCORR)
* Detect and record SINK pixels in the DQ mask (performed if DQICORR is set to PERFORM)
* Perform unit conversion
* Subtract the post-flash image if applicable (FLSHCORR)
* Scale and subtract the dark image (DARKCORR)
* Perform flatfielding (FLATCORR)
* Perform shutter-shading correction where necessary, currently skipped (SHADCORR)
* Populate photometric header keywords (PHOTCORR)
* Correct chips to be on the same zeropoint (FLUXCORR)
* Calculate image statistics for the header


Correction For Charge Transfer Efficiency (PCTECORR)
----------------------------------------------------
The charge transfer (CTE) of the UVIS detector has been declining over time as on-orbit radiation damage creates charge traps in the CCDs. Faint sources in particular can suffer large flux losses or even be lost entirely if observtions are not planned and analyzed carefully. The CTE depends on the morphology of the source, the distribution of electrons in the field of view, and the population of charge traps in the detector column between the source and the transfer register. Further details of the current understanding of the state of the WFC3/UVIS charge transfer efficieny (CTE) are presented in `Section 5 <http://www.stsci.edu/hst/wfc3/documents/handbooks/currentIHB/c05_detector5.html#392274>`_  of the data handbook as well as on the `WFC3 CTE webpage <http://www.stsci.edu/hst/wfc3/ins_performance/CTE/>`_ .  The PCTECORR step aims to mitigate the flux loss incurred from CTE.

More information on this part of the pipeline can be found in the :ref:`wf3cte` documentation.


Error Array Initialization
--------------------------

The image error array is initialized. The function examines the RR extension of the input data to determine the state of the array. The input _raw image contains an empty ERR array. If the ERR array has already been expanded and contains values other than zero, then this function does nothing. Otherwise it will intialize the ERR array by assigning pixel values based on a simple noise model. The noise model uses the science (SCI) array and for each pixel calculates the error value :math:`\sigma` in units of DN:

.. math::

    \sigma_{CCD} = \sqrt{(SCI-bias)/(gain) + (readnoise/gain)^{2}}

The CCDTAB reference file contains the bias, gain and readnoise values used for each CCD aplifier quadrant used in this calculation. The table contains one row for each configuration that can be used during readouse, which is uniquely identified by the list of amplifiers (replicated in the CCDAMP header keyword), the particular chip being read out (CCDCHIP), the commanded gain (CCDGAIN), the commanded bias offset level (CCDOFST) and the pixel bin size (BINAXIS). These commanded values are used to find the table row that matches the characteristics of the image that is being processed and reads each amplifiers characteristics, including readnoise (READNSE), A-to-D gain (ATODGN) and the mean bias level (CCDBIAS).


Data Quality Array Initialization (DQICORR)
-------------------------------------------

This step initializas the data quality array by reading a table of known bad pixels for the detector, as stored in the Bad Pixel reference table BPIXTAB. The types of bad pixels that can be flagged are:

=============== ======  =======================================================
NAME            VALUE   DESCRIPTION
=============== ======  =======================================================
GOODPIXEL        0      OK
SOFTERR          1      Reed-Solomon decoding error
DATALOST         2      data replaced by fill value
DETECTORPROB     4      bad detector pixel or beyond aperture
DATAMASKED       8      masked by occulting bar
HOTPIX           16     hot pixel
CTETAIL          32     UVIS CTE tail
WARMPIX          64     warm pixel
BADBIAS          128    bad bias value
SATPIXEL         256    full-well or a-to-d saturated pixel
BADFLAT          512    bad flatfield value
TRAP             1024   UVIS charge trap, SINK pixel
ATODSAT          2048   a-to-d saturated pixel
ne TBD           4096   reserved for Multidrizzle CR rej
DATAREJECT       8192   rejected during image combination UVIS, IR CR rejection
CROSSTALK        16384  ghost or crosstalk
RESERVED2        32768  can't use
=============== ======  =======================================================

Sink Pixel Detection and Marking
--------------------------------

Sink pixels are a type of image defect. These pixels contain a number of charge traps and under-report the number of electrons that were generated in them during an exposure. These pixels can have an impact on nearby upstread or downstream pixels, though they often only impact one or two pixels when the background is high, they can impact up to 10 pixels if the background is low.

Flagging of SINK pixels in the DQ extension of calibrated images is controlled with the DQICORR header keyword, happens after the bias correction has been performed, and is done in the amp-rotated CDAB full image format used and described in the CTE correction. When set to perform, the sink pixels are located and flagged with help from the SNKCFILE reference image. Given the reference image, the procedure for flagging the sink pixel in science data involves:

* Extract the MJD of the science exposure
* Go through the reference image pixel by pixel looking for those pixels with values greater than 999, which indicates that the current pixel is a sink pixel. The value of this pixel in the reference file corresponds to the date at which this pixel exibited the sink behavior.
* If the turn on date of the sink pixel is after the exposure date of the science image, then we ignore the sink pixel in this exposure and move on to the next pixel
* If the turn on date of the sink pixel is before the exposure date of the science image, then this science pixel was compromised at the time of the exposure.The corresponding DQ extension pixel for this science pixel is flagged with the "charge trap" flag of 1024.
* If the pixel "below" the sink pixel in the long format image has a value of -1 in the reference image, then it is also flagged with the "charge trap" value in the DQ extension. We then proceed vertically "up" from the sink pixel and compare each pixel in the reference file to the value of the sink pixel in the science exposure at hand. If the value of the sink pixel in the exposure is below the value of the upstream pixel in the reference image, we flag that pixel with the "charge trap" value in the DQ extension. We continue to flag pixels until the value of the pixel in the reference image is zero or until the value of the sink pixel in the exposure is greater than the value of the upstream pixel in the reference image.


`WFC3 ISR 2014-19 <http://www.stsci.edu/hst/wfc3/documents/ISRs/WFC3-2014-19.pdf>`_ has a detailed analysis on detection of the sink pixels, while the strategy for flagging them is discussed in `WFC3 ISR 2014-22 <http://www.stsci.edu/hst/wfc3/documents/ISRs/WFC3-2014-22.pdf>`_ .

Sink pixels are currently only flagged in full frame science images, `calwf3v3.4` will also perform flagging in subarray images.
**The pipeline currently does no further analysis or correction on pixels which have been flagged as affected by sink pixels**



Unit Conversion to Electrons
----------------------------

The UVIS image is multiplied by gain right after BIASCORR, converting it to ELECTRONS. This step is no longer embedded within FLATCORR.


Bias Correction (BIASCORR)
--------------------------

This step subtracts the two dimensional bias struction from the image using the superbias reference image listed in the header keyword BIASFILE. The dimensions of the image are used to distinguish between full and sub-array images. Because the bias image is already overscan-subtracted, it will have a mean pixel value of less than one. The BIASFILE has the same dimensions as a full-size science image, complete with overscan regions. Only after completion of :ref:`wf3ccd` are the science images trimmed to their final calibrated size. The same reference image is used for full-frame and subarray images, `calwf3` will extract the matching region from the full-size bias file and apply it to the subarray image.


Overscan Bias Correction (BLEVCORR)
-----------------------------------

The location of the overscan regions in a raw image varies, depending upon the type of readout that is performed. The overscan regions are used to monitor the instrument as well as provide a measure of the bias level at the time the detector was exposed. The bias level which is calculated for subtraction is done on a line-by-line basis in the image. If the image has no overscan region the BIAS level to be subtracted is obtained from the CCDTAB reference file. Otherwise, the columns to use for the calculation are referenced in the OSCNTAB reference file. The OSCNTAB refers to all regions in pixel coordinates, even when the image is binned. A bias drift calculation is made if there are virtual overscan pixels which exist, if neither of the virtual overscan regions are specfied then the physical overscan region is used.

If there are two sections available to use for the line because only 1 amp was used then they are averaged. The parallel overscan region is split into two if there is more than one amp. If the virtual overscan is used, a straight line is fit as a function of the column number. The fit is evaluated for each line and then subtracted from the data.  Iterative sigma clipping is used to reject outliers from the array of bias values.

The mean value of all the bias levels which were subtracted is recorded in the SCI extension output header in MEANBLEV.

::

        parallel readout direction, amp A
        |
        |
        v
        (VX1,VX2)     (VX2,VY2)
        A       /         \     B
        -----/-----------+---
        |   |/     |      |   | } TRIMY2
        |   +------+------    |
        |   |      |      |   | <--- serial readout direction, amp A
        |   |      |      |   |
        | - | -----+------|---|<-- AMPY
        |   |      |      |   |
        |   |      |      |   |
        |   |      |      |   |
        |    ------+------    |
        |   |      |      |   | } TRIMY1
        ---------------------
        C /  \      ^       / \ D
        A1  A2     |      B1  B2
          AMPX

        A,B,C,D   - Amps
        AMPX 	  - First column affected by second AMP
        AMPY 	  - First line affected by second set of AMPS
        (VX1,VY1) - image coordinates of virtual overscan region origin
        (VX2,VY2) - image coordinates of top corner of virtual overscan region
        A1,A2 	  - beginning and ending columns for leading bias section
            (BIASSECTA1,BIASSECTA2 from OSCNTAB)
        B1,B2 	  - beginning and ending columns for trailing bias section
            (BIASSECTB1,BIASSECTB2 from OSCNTAB)
        TRIMX1    - Number of columns to trim off beginning of each line,
            contains A1,A2
        TRIMX2    - Number of columns to trim off end of each line,
            contains B1,B2
        TRIMY1    - Number of lines to trim off beginning of each column
        TRIMY2    - Number of line to trim off end of each column




Dark Current Subtraction (DARKCORR)
-----------------------------------

The reference file listed under the DARKFILE header keyword is used as the reference dark image.

In the UVIS, the dark image is scaled by EXPTIME and FLASHDUR.

The reference file pointed to with DARKFILE is used for the non-CTE corrected data.

The reference file pointed to with DRKCFILE is used for the CTE corrected data

Shutter Shading Correction (SHADCORR)
-------------------------------------

This step corrects the science image for differential exposure time across the detector cased by the amount of time it takes for the shutter to completely open and close, which is a potentially signiciant effect only for images with very short exposure times (less than ~5 seconds). Pixels are corrected based on the exposure time using the relation:

.. math::

    corrected = uncorrected \times EXPTIME \div (EXPTIME + SHADFILE)


WFC3 tests have shown that the shutter shading effect is insignificant (< 1%), even for the shortest allowed UVIS exposure time of 0.5 seconds (see `WFC3 ISR 2007-17 <http://www.stsci.edu/hst/wfc3/documents/ISRs/WFC3-2007-17.pdf>`_). Therefore this step is **ALWAYS set to OMIT** in `calwf3`.


Post-Flash Correction (UVIS ONLY) (FLSHCORR)
--------------------------------------------

WFC3 has post-flash capability to provide a means of mitigating the effects of Charge Transfer Efficiency (CTE) degredation.  When FLSHCORR=PERFORM, this routine subtracts the post-flash reference image, FLSHFILE, from the science image after DARKCORR in the WF32D step. The success of the post-flash operation during the exposure is first verified by checking the keyword FLASHSTA. The FLSHFILE is renormalized to the appropriate post-flash current level (LOW, MED, HIGH) recorded in the FLASHCUR keyword, and the flash duration (FLASHDUR) and is then subtracted from the science image. The mean value of the scaled post-flash image is written to MEANFLSH in the output SCI extension header. Different members of an association can have different values of SHUTRPOS because it varies by exposure, and this is fine for calibration because the references files are populated separately for each exposure.

=========   =======================================================================================================================
KEYWORD     DESCRIPTION
=========   =======================================================================================================================
FLSHDUR     is the length of time of the flash exposure
FLSHCUR     is the current that was used to the lamp as calculated by TRANS, which also calculates FLASHEXP, (ZERO, LOW, MED,HIGH)
FLSHFILE    is the flash reference file, which has an illumination pattern for each shutter
SHUTRPOS    says which shutter was used
FLASHSTA    indicates an interrupted exposure (ABORTED, SUCCESSFUL, NOT PERFORMED)
FLASHLVL    post flash level in electrons
MEANFLSH    the mean level which `calwf3` calculated and then subtracted
=========   =======================================================================================================================


Futher reading:
    * `WFC3 Post-Flash Calibration ISR <http://www.stsci.edu/hst/wfc3/documents/ISRs/WFC3-2013-12.pdf>`_
    * `CTE-Loss Mitigation Before Data Acquisition <http://www.stsci.edu/hst/wfc3/documents/handbooks/currentIHB/c06_uvis10.html#439394>`_

FLATCORR
--------
Correct the image for pixel quantum efficiency using the reference image specified by the FLATFILE keyword in the header.
Conversion from DN to ELECTRONS no longer depends on FLATCORR=PERFORM, all images are converted appropriately.

This actually consists of correction using up to 3 reference flat images:

* PFLTCORR: apply a pixel-to-pixel flat (ground flats)
* DFLTCORR: apply a delta flat, applies any needed changes to the small-scale PFLTFILE
* LFLTCORR: apply a low order flat, correcting for large scale sensativity variations (on-orbit)

The pipeline is currently only using the P-flats. If two or more reference files are specified, they are read in line-by-line and multiplied together to form a combined flatfield correction image.

Subarray science images use the same reference file as the full-frame images; `calwf3` will extract the appropriate region from the reference file and apply it to the subarray input image.

Photometry Keywords (PHOTCORR)
------------------------------

The PHOTCORR step is performed using tables of precomputed values instead of calls to SYNPHOT, it uses the reference table specified in the IMPHTTAB header keyword. Each DETECTOR uses a different table.

If you do not wish to use this feature, set the header keyword PHOTCORR to OMIT. However, if you intend to use the FLUXCORR step, then PHOTCORR must be set to PERFORM as well.


* PHOTFNU: the inverse sensitivity in units of :math: Jansky sec electron^{-1}`
* PHOTFLAM: the inverse sensistiy in units of :math:`ergs\  cm^{-2} A^{-1} electron^{-1}`
* PHOTPLAM: the bandpass pivot wavelength
* PHOTBW: the bandpass RMS width
* PHTFLAM1: the inverse sensistiy in units of :math:`ergs cm^{-2} A^{-1} electron^{-1}`
* PHTFLAM2: the inverse sensistiy in units of :math:`ergs cm^{-2} A^{-1} electron^{-1}`



For versions 3.3 and beyond, the value PHOTFNU is calculated specific for each UVIS chip, see the section on FLUXCORR for more information.

The SCI headers for each chip contain the PHOTFNU keyword, which is valid for its respective chip, where PHOTFNU is calculated as:

For UVIS 1:  :math:`photfnu = 3.33564e^{4} * PHTFLAM1 * PHOTPLAM^{2}`

For UVIS 2:  :math:`photfnu = 3.33564e^{4} * PHTFLAM2 * PHOTPLAM^{2}`



The IMPHTTAB file format for WFC3 UVIS is as follows:

::

        EXT#  FITSNAME      FILENAME              EXTVE DIMENS       BITPI OBJECT

        0     z7n21066i_imp z7n21066i_imp.fits                       16
        1       BINTABLE    PHOTFLAM              1     5Fx256R
        2       BINTABLE    PHOTPLAM              1     5Fx256R
        3       BINTABLE    PHOTBW                1     5Fx256R
        4       BINTABLE    PHTFLAM1              1     5Fx256R
        5       BINTABLE    PHTFLAM2              1     5Fx256R


where each extension contains the photometry keyword information for that specific header keyword. The rows inside the tables are split on observation mode.



Flux normalization for UVIS1 and UVIS2 (FLUXCORR)
-------------------------------------------------
The FLUXCORR step was added in calwf3 v3.1.2 as a way to scale the UVIS chips
so that the flux correction over both chips is uniform. This requires new keywords
which specify new PHOTFLAM values to use for each chip as well as a keyword to specify the scaling factor
for the chips. New flatfields must be used and will replace the old flatfields in CDBS but the change will
not be noticable to users. Users should be aware that flatfield images used in conjunction with v3.2.1
of the software should not be used with older versions as the data, and vice versa will be scaled incorrectly.

The new keywords include:

* PHTFLAM1: The FLAM for UVIS 1
* PHTFLAM2: The FLAM for UVIS 2
* PHTRATIO: The ratio: PHTFLAM2 / PHTFLAM1, which is calculated by calwf3 and is multiplied with UVIS2 (SCI,1 in the data file)

.. note::

    In order for FLUXCORR to work properly the value of PHOTCORR must also be set to PERFORM since this populates
    the header of the data with the keywords FLUXCORR requires to compute the PHTRATIO.

This step is performed by default in the pipeline and the PHOTFLAM keyword will be valid for both chips after the correction has been applied.


Cosmic-ray rejection
--------------------
Associations with more than one member, which have been associated using either CR-SPLIT or REPEAT-OBS, will be combined using :ref:`wf3rej`. The task uses the same statistical detection algorithm developed for ACS (acsrej), STIC (ocrrj) and WFPC2(crrej), providing a well-tested and robust procedure. The DRZ and DRC products will be created from the association, with `Astrodrizzle <http://www.stsci.edu/hst/HST_overview/drizzlepac/>`_, which will also correct for geometric distortion.
