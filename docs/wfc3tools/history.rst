.. _software-history:

*****************************************
Software Update History for HSTCAL.CALWF3
*****************************************

.. warning:: IRAF version of WFC3 no longer maintained or delivered, use WFC3TOOLS in HSTCAL or call the executable from your operating system command line. With version 3.3 the pipeline now produces two versions of each calibrated file, one set with the CTE correction applied and one set without the CTE correction applied

**Updates for Version 3.4.1 10-Apr-2017 - MLS**
    - Fixed missed init for header vars in cte code

**Updates for Version 3.4.1 02-Apr-2017 - MLS**
    - Fixed logic brackets in subarray prescan bias call which didn't explicitly do the gain correction in the if loop, see Issue #55
    - Fixed double statement, see Issue #63

**Updates for Version 3.4.1 27-Mar-2017 - MLS**
    - Update photometry keyword descriptions for UVIS

**Updates for Version 3.4 26-Sep-2016 MLS**
    - Fixed memory allocation around some print statements

**Updates for Version 3.4 20-Sep-2016 MLS**
    - Moved the init for the CTE params back to the top of the code, it had gotten moved below the header update for the information

**Updates for Version 3.4 14-Sep-2016 MLS**
    - CTE subarrays enabled for user supported subarrays with physical overscan

**Updates for Version 3.4 6-Sep-2016 MLS**
    - Sink pixel flagging for subarray appears correct now

**Updates for Version 3.4 18-July-2016 MLS**
    - CTE and Sink Pixel implementation for subarrays submitted by Brechmos for review

**Updates for Version 3.3 28-Jan-2016 MLS**
    * Removed the call to WF3Dth for the CTE data. This is essentially useless since the DTH step has been replaced with astrodrizzle, the only function it has it to concatinate the SPT files from the association members into a new spt file with the product/subproduct name. This is already done for the non-cte processed data, there is no difference between the cte and non-cte SPT files, they are only related to the RAW input file.

**Updates for Version 3.3 22-Jan-2016 MLS**
    * Noticed I missed renaming the crc file with the call to WF3DTH and was setting the input to the crj suffix, but also needed updates to GetAsnTable to include crc filename population for subproducts and sending the correct subproduct through processing, it was always using crj
    * some code cleanup as I went
    * trailer file concatination update, but it's still not entirely correct

**Updates for Version 3.3 19-Jan-2016 MLS**
    * Updates to fix trailer file output information. Part of the problem is the change in name of the output RAC_TMP file, the functions which create input and output trailer file naming conventions look for the dot to separate extensions so I need to change some expectations.
    * Update to check for the raw header value of PCTENSMD and update the cte parameter table accordingly (though only a value of 0 is valid right now)

**Updates for Version 3.3 08-Jan-2016 MLS**
    * changed the name of the output rac file to rac_tmp so that archive could handle deleting it better

**Updates for Version 3.3 05-Nov-2015 MLS**
    * removed explicit downcasts and added calloc returns in procccd

**Updates for Version 3.3 04-Nov-2015 MLS**
    * add more explicity initializations where I could find them

**Updates for Version 3.3 24-Oct-2015 MLS**
    * The nightly build is specifying a higher level of optimization through to the compiler than the debug mode that I have been using for my testing. Building calwf3 with the lower optimization produced no errors or warnings and ran through cleanly, but the high optimization brought on a segfault inside the CTE code in the first openmp section. This was only happening on the Linux cluster, the MAC builds showed no issue. The problem area seemed to be a set of arrays which would rather be doubles than floats. I also changed the remaining floats to doubles, where I could, and removed more of the memcpy statements, making them regular array assignments.
    * I also removed a superfluous openmp print statement from maincte.c and cleaned up some more informational print statements.
    * I added a time measurement, with verbose on the code prints how long the CTE section took to run, with the specification of number of threads/cpus.


**Updates for Version 3.3 21-Oct-2015 MLS**
    * Editing text for the screen and trailer files
    * Formally removed the rac file before the routine ends since archive isn't expecting it

**Updates for Version 3.3 16-Oct-2015 MLS**
    * machine dependent bug, some images were getting nan values on linux machines
    * I also removed the temporary image saves we were using for the CTE routines

**Updates for Version 3.3 29-Sep-2015 MLS**
    * bug in original fortran code fixed; the final RAC image should be made by subtracting the CHG image (the net cte effect) from the original non-BIC subtracted raw data. This should remove the additional bias signature that Matthew was seeing in the stacked dark frames. It should NOT make a significant change in the overall output of the code since bias levels are low to begin with.
    * I also changed the way the code uses the SCLBYCOL reference file (as called in Jays fortran). The way the fortran code is structured, the reference file information never actually gets used in the calculation. This doesn't make a numerical difference at the moment because the reference file values are all ones, ie. there is no additional scaling done on the CTE pixel other than by using the CTE scaling fraction and the column location. However, if the science team ever delivers a new reference file which has these values updated, they wont actually get used by the code unless this change is implemented.
    * Reformatted some code for readability, and fixed SEGFAULT error in reference file checking when iref environment variable not set by user, so can't find file (also when can't find file in general). I made RefExist exit clean the first time it found a missing file, HSTIO was barfing any other way.

**Updates for Version 3.3 24-Sep-2015 MLS**
    * fix for machine dependent precision bug

**Updates for Version 3.3 03-Sep-2015 MLS**
    * One more precision change needed for the nans in the readnoise section

**Updates for Version 3.3 28-Aug-2015 MLS**
    * These updates appear to fix the nan issue in the readnoise step that we ran into with some images
    * I also made the cte code a bit more tidy and organized

**Updates for Version 3.3 25-Aug-2015 MLS**
    * changed pow() to powf() in the readnoise calculation to deal with memory overrun producing nans in some cases

**Updates for Version 3.3 24-Aug-2015 MLS**
    * updated the mac os version check in wscript to use sw_vers, the old way was returning junk and we need it for adding the 64bit flags to the compile
    * added some initializations the clang compiler complained about

**Updates for Version 3.3 20-Aug-2015 MLS**
    * I changed a float to double in wf3cte readnoise section for added precision
    * moved GetGlobalInfo and checkGlobal info higher in the code to reject non-wfc3 datasets
    * moved a delete section further out in the logic and that seemed to fix #1220, tests on cte and non-cte data seemed happy

**Updates for Version 3.3 18-Aug-2015 MLS**
    * BuildDthInput has to create the input filename from the asn root, but this can be either FLT or FLC now, have to figure out which one to use.
    * Had to add separate DTH pass for IR data and double DTH pass for UVIS data because the input filename for RPTCORR/EXPCORR associations are built in the code from the data rootnames in the ASN table. So the UVIS data coming out of procccd has to take a double pass through DTH when PCTECORR is PERFORM.
    * changed the checking order for subarrays in the PCTECORR routine so that it errors out cleanly (has to do with 1 group of images for subarrays)
    * added the check for INSTRUMENT == WFC3 back to the code, actually related to a user complainging that calwf3 didn't tell them it couldn't reduce ACS data.
    * had to update the procir call to wf3rej_0 signature for the asn update I added to uvis
    * updated the mainrej.e calls which were segfaulting (calling wf3rej standalone on input list of images)
    * added dynamic memory allocation for trailer file list to initrejtrl
    * updated text in wf3rej to report that Astrodrizzle should be used to align images instead of PyDrizzle since that's how it's advertised to users
    * found a problem (even in the released version of calwf3) with output file for associations with multiple products, created #1220

**Updates for Version 3.3 12-Aug-2015 MLS**
    * fix for #1215 binned data detection for sink pixel seg faults

**Updates for Version 3.3 11-Aug-2015 MLS**
    * nrej initialized in wf3rej so that REJ_RATE reported consistently correct, see #1214
    * fix for #1216, the BIACFILE name was not being populated for bias images with BIASCORR == OMIT
    * I also went ahead and added a clean exit for images going to PCTECORR which already have BIASCORR complete

**Updates for Version 3.3  21-July-2015 MLS**
    * Debugged version of the CTE code committed.
    * see #1193 ticket for extensive changes

**Updates for Version 3.3  31-May-2015 MLS**
    * UVIS 2.0 added, including CTE correction, Sink Pixel and Photometry updates
    * (#1011) New photometry correction for UVIS. This includes a delivery of new flatfields for all filters in CDBS as well as a new IMPHTTAB. The new calibration step is controlled by the FLUXCORR keyword in the image header.
    * (#1154) CTE correction for all UVIS data. This is done in conjunction with a full run through of the pipeline code without the CTE correction applied. This correction is for the same reasons as in ACS, but the CTE correction method and code are different, and they are applied to the raw file instead of later in the processing. Some sections of the CTE code support parallel processing with OpenMP. The default for calwf3 is to use all available processors. To restrict processing to 1 cpu use the flag -1 in the call to calwf3.e  The cte processing is controlled with the PCTECORR keyword.
    * Sink pixels added to the science image DQ mask using the SNKCFILE reference image. This image has 2 extensions, each in the pre-overscan trimmed format. This step is performed if DQICORR is PERFORM, and is done before BLEVCORR while the science image is still untrimmed.
    * see #1193 for more detailed information on all the updates


**Updates for  Version 3.2.1 08-Dec-2014 MLS:**
    * The FLUXCORR step has been updated, changing how the data is processed in the flow of the pipeline. It was discovered that a chain of requirements meant that the values from the IMPHTTAB were not being read or updated correctly. This is a multifold problem which starts with the way that the IMPHTTAB is read and how it is constructed. Since the file, and it's calling functions, are common to all instruments, the best way around it was to move where the fluxcorr step was done in the pipeline to OUTSIDE the main wf32d loop. The step then reads in the FLT file which was written out and updates the SCI,1 data and headers with the photometry keyword information.


**Updates for  Version 3.2 09-Dec-2013 MLS:**
    * A new calibration step was added to the UVIS process, FLUXCORR, can now be run at the end of regular processing. It will scale the chip2 image using the new PHTFLAM1 and PHTFLAM2 values in the IMPHTAB. New flatfields for all filters, as well as a new IMPHTTAB will be delivered by the team for this step to be completely implemented. This is a significant version increase since I had to modify the globablly access GetPhotTab to read the new WFC3 imphttab correctly, as well as touch many routines in the calwf3 process.( see tickets #1088, #1011, #1025)


**Updates for Version 3.1.6 15-Nov-2013 MLS:**
    * Fixed a file i/o issue after change in cfitsio interaction (see #970, #1073 and #1069)

**Updates for Version 3.1.5 30-Sep-2013 MLS:**
    * Fixed the individual task executables for wf3ir, wf3ccd, wf32d to properly used the user specfied output filename when they are called standalone

**Updates for Version 3.1.4 09-Sep-2013 MLS:**
    * Added a couple new functions to deal with user specified subarrays when they start in amp A or C and continue to B or D. In these cases the virtual overscan from the reference postflash file must be avoided, and just incrementing the starting pixel for the array in not a good solution.

**Updates for  Version 3.1.3  26-Mar-2013 MLS:**
    * Updated the postflash routine to apply the correct offset for all amps when a user specified subarray is used (no GO users are allowed to do this)
    * Some unrelated files will change because I formatted the indentation to make the code easier to decipher

**Updates for Version 3.1.2 11-Feb-2013 - MLS:**
    * Updated the bias subtraction to check for CCDAMP values of SINGLE_AMP and SINGLE_OR_ALL in the reference bias file image when a full frame reference file  and a  user specified subarray are used so that the correct overscan region is ignored
    * Removed check for TDFTRANS per team request, see #980, I'm keeping the same version as the previous change because I havent delivered it yet

**Updates for Version 3.1.1 2-Jan-2013 - MLS:**
    * File I/O in acsrej updated to avoid problems with CFITSIO upcasting file permissions to read/write when not needed. This will allow the hstio code to remove logic that allowed the old code to work but caused problems for CADC when CFITSIO opened ref files in read/write mode because of that hstio logic.

**Updates for version 3.1 31-Dec-2012 MLS:**
    * fixed TrlBufInit problem so it initializes correctly (r21162)

**Updates for version 3.1 28-Dec-2012 MLS:**
    * Updated to account for a memory leak on linux machines during BuildDth  when RPTCORR is off and a new spt is being constructed (#967)

.. warning:: HST CAL DELIVERED, STSDAS+IRAF version no longer maintained, use WFC3TOOLS in HSTCAL


**Updates 18Oct 2012 - MLS - Version 2.7.1**
    * fixed a memory leak in cridcalc that was occuring on linux machines and only affected IR data.
    * version date and number updated

**Updates for version 2.7 21-May-2012 MLS:**
   * cridcal.c/wf3dq.h:
      * update to help negative cr detections (fabs the comparison)
      * updated the spike flag to 1024 so that those pixels weren't ignored in the rejection routinea
      * Use zero read pixel value for WF3 IR ramp fitting when saturated
   * do2d.c, cr_scaling.c:
       * update for BUNIT keyword value so it's not case sensitive, BUNIT value now stored as ELECTRONS instead of electrons as well
   * wf32d: version update to 07may2012
   * wf3rej.cl: version update to 07may2012
   * wf3version.h: version update to 07may2012
   * wf3main.c: new option r added to print current version and exit

**Updates for version 2.6.3 23-Mar-2012 (HAB):**
    * calwf3.cl: Increment version to 23Mar2012.
    * wf3version.h: Increment version to 2.6.3 and date to 23-Mar-2012.
    * calwf3/calwf3.c: Upgraded the BuildDthInput function to build file list from names of individual association members when a CRJ sub-product has not been created. (PR 70922; Trac #869)
    * calwf3/procir.c:  Updated to set CRJ sub-product status to PRESENT after running wf3rej, and report RPTCORR switch status via trlmessage when wf3rej is not run. (PR 70922; Trac #869)

**Updates for version 2.6.2 27-Jan-2012 MLS:**
    * calwf3.cl:  Increment version to 27Jan2012.
    * wf3version.h:  Increment version to 2.6.2 and date to 27-Jan-2012.
    * wf3rej/rej.h: Decreased MAX_FILES from 250 to 120 because OPUS is still getting  errors when trying to process this many images.

**Updates for version 2.6.1 24-Jan-2012 MLS:**
     * calwf3.cl: Increment version to 24Jan2012.
     * wf3version.h: Increment version to 2.6.1 and date to 24-Jan-2012.
     * calwf3/procir.c: Added a check for the number of images present when RPTCORR=PERFORM so that wf3rej is not run for singletons.

**Updates for version 2.6 - 15-Dec-2011 (HAB):**
    * calwf3.cl:    Increment version to 15Dec2011.
    * wf3version.h:   Increment version to 2.6 and date to 15-Dec-2011.
    * wf3rej/cr_scaling.c: Upgraded to read BUNIT keyword value from first SCI extension header of each input image. (PR 69969; Trac #814)
    * wf3rej/rej_do.c: Upgraded to pass new bunit array to and from all functions that need  it, in order to handle input data that are in count rates. (PR 69969; Trac #814)
    * wf3rej/rej_init.c:  Upgraded to rescale input data that are in units of count rates.(PR 69969; Trac #814)
    * wf3rej/rej_loop.c: Upgraded to rescale input data that are in units of count rates. (PR 69969; Trac #814)
    * wf3rej/rej_sky.c: Upgraded to rescale input data that are in units of count rates. (PR 69969; Trac #814)

**Updates for version 2.5.1 - 09-Dec-2011 (HAB):**
    * calwf3.cl: Increment version to 09Dec2011.
    * wf3version.h: Increment version to 2.5.1 and date to 09-Dec-2011.
    * calwf3/procir.c: Modified the logic that controls the rptcorr processing so that it's based on the setting of the RPTCORR  header keyword switch, instead of just always applying it to every repeat-obs association. (PR 69952; Trac #807)

**Updates for version 2.5 - 01-Oct-2011 (HAB):**
    * calwf3.cl: Increment version to 01Oct2011.
    * wf3version.h: Increment version to 2.5 and date to 01-Oct-2011.
    * wf3ir/cridcalc.c: Fixed fitsamps routine to correctly accumulate int_time in odd cases where the 1st or 2nd read is bad. (PR 69230; Trac #770)
    * wf3ir/rej.h: Increase MAX_FILES from 120 to 250. (PR 63555)
    * wf3rej/rej.h: Increased MAX_FILES from 120 to 250. (PR 63555)

**Updates for version 2.4.1 - 02-Aug-2011 (HAB):**
    * calwf3.cl: Increment version to 02Aug2011.
    * wf3version.h: Increment version to 2.4.1 and date to 02-Aug-2011.
    * lib/wf3info.c: Fixed the logic in the CheckGain routine so that the ref image gets closed before returning when keyval=-1. (PR 68983; Trac #745)
    * wf3ir/cridcalc.c: Updated crrej to free memory for tot_ADUs before returning. (PR 68993; Trac #748)

**Updates for version 2.4 - 17-Jun-2011 (HAB):**
    * calwf3.cl: Increment version to 17Jun2011.
    * wf3version.h: Increment version to 2.4 and date to 17-Jun-2011.
    * calwf3/procccd.c: Modified logic involved in handling error returns from WF3Rej so that WF32d processing still takes place for individual exposures if EXPSCORR=PERFORM. (PR 68593; Trac #722)
    * wf3rej/rej_init.c: Added missing call to free(ipts) at end.
    * wf3rej/wf3rej.c: Fixed error status return from rej_do so that original status gets passed up for use in caller. (PR 68593; Trac #722)

**Updates for version 2.3 - 15-Mar-2011 (HAB):**
    * calwf3.cl: Increment version to 15Mar2011.
    * wf3version.h: Increment version to 2.3 and date to 15-Mar-2011.
    * calwf3/calwf3.c: Modified CopyFFile routine to update the FILENAME keyword in created output file. (PR 67225; Trac #646)
    * wf3ir/doir.c: No longer load dark ref file for zsigcorr. (PR 67728; Trac #681)
    * wf3ir/getirflags.c: Removed zsigcorr checks in checkDark routine, because zsigcorr no longer uses the dark. (PR 67728; Trac #681)
    * wf3ir/zsigcorr.c: Modified zsigcorr routine to just subtract the super-zero read image from the science zero read image to estimate zero read signal, rather than scaling the difference between the first and zero reads in the science image. This avoids problems with zoer read exposure time in subarray exposures. Also eliminated use of dark image.	(PR 67728; Trac #681)

**Updates for Version 2.2 - 01-Dec-2010 (HAB):**
    * calwf3.cl: Increment version to 01Dec2010.
    * wf3version.h: Increment version to 2.2 and date to 01-Dec-2010.
    * calwf3/calwf3.c: Modified CalWf3Run and BuildDthInput to skip processing for sub-products that have < 2 members present, because no sub-product is produced in this case. (PR 66366; Trac #622)
    * calwf3/getreffiles.c: Modified GetIRRef to correctly check all IR switches, so that re-entrant processing works correctly. (PR 66081; Trac #608)
    * calwf3/wf3dth.c: Modified InitDthTrl to return with no action if the input member list is empty, to handle missing asn members. (PR 66366; Trac #622)
    * calwf3/wf3table.c: Modified GetAsnTable to turn off CRCORR/RPTCORR if there aren't any sub-products with > 1 member. (PR 66366; Trac #622)
    * lib/tabpedigree.c: When tbtopn has a failure, reset status to zero before returning, so that calling routines have a chance to print error messages before shutting down. (PR 65410; Trac #578)
    * lib/trlbuf.c: Modified WriteTrlFile to check for non-null pointer before trying to close trailer file (PR 66366; Trac #622).
    * wf3ir/cridcalc.c: Changed crrej to always call EstimateDarkandGlow, regardless of darkcorr setting, because for WFC3 we use a static dark value and therefore don't need access to the darkfile. (PR 66081; Trac #608)
    * wf3ir/doir.c: Upgraded crimage header updates to include check of flatcorr status when updating BUNIT values. Also modified noisMsg routine to print  noiscorr switch value and have trailer message printed from noiscorr routine itself. Both changes are to support re-entrant processing. (PR 66081; Trac #608)
    * wf3ir/getirflags.c: Fixed a reference to dqicorr in checkCRRej that should've been crcorr.
    * wf3ir/getirsw.c: Modified GetSw routine to not reset cal switches to OMIT if they have a value other than PERFORM, in order to support re-entrant processing where some switches are COMPLETE. (PR 66081; Trac #608)
    * wf3ir/groupinfo.c: Upgraded getDataUnits routine to recognize BUNIT values of ELECTRONS, to support re-entrant processing. (PR 66081; Trac #608)
    * wf3ir/irhist.c: Upgraded noisIRHistory routine to first check setting of noiscorr switch before adding history keyword, to support re-entrant processing. (PR 66081; Trac #608)
    * wf3ir/noiscalc.c: Modified doNoisIR to print trailer message and noiscorr value, and also give a message saying that noiscorr is skipped if noiscalc returns with an error. Noiscalc was modified to see if the ERR array is already populated before doing the calculation, to support re-entrant processing. (Pr 66081; Trac #608)
    * wf3ir/pixcheck.c: Updated the WFC3 IR DQ value assignments. (PR 66080; Trac #607)
    * wf3ir/unitcorr.c: Upgraded unitcorr routine to check flatcorr status to decide proper units for BUNIT keyword value update, to support re-entrant processing. (PR 66081; Trac #608)
    * wf3ir/zsigcorr.c: Modified to no longer call pixOK function before operating on a pixel. Instead, do the calculation for all pixels. (PR 66080; Trac #607)

**Updates for Version 2.1 - 15 May 2010 (HAB):**
    * calwf3.cl, wf32d.cl, wf3ccd.cl, wf3rej.cl, wf3ir.cl: Increment version to 07May2010.
    * wf3version.h: Increment version to 2.1 and date to 07-May-2010.
    * calwf3/procccd.c: Modified logic and processing flow so that if CRCORR=PERFORM and EXPSCORR=PERFORM, run wf32d on the individual exposures *after* crcorr is complete, so that CR flags inserted into blv_tmp files by crcorr will show up in final flt images produced by wf32d. (PR 64963; Trac #545)
    * wf3rej.cl: Modified to place the user-supplied crsigmas param string in quotes when appending to the command line, so that embedded blanks don't cause problems for the parser. (PR 64941; Trac #544)
    * wf3rej/readpar.c: Updated the strtor routine to match the one in the calstis lib, which skips over leading and embedded blanks in the string. (PR 64941; Trac #544)
    * wf3ir/darkcorr.c: Updated the darkcorr routine to compute and populate the MEANDARK keyword. (PR 65151; Trac #560)
    * wf3ir/doir.c: Swapped the execution order of darkcorr and nlincorr, so now nlincorr goes first. (PR 64854; Trac #536)

**Updates for Version 2.0 - 08 Mar 2010 (HAB):**
    * calwf3.cl, wf32d.cl, wf3ir.cl, wf3rej: Increment version to 08Mar2010.
    * wf3version.h: Increment version to 2.0 and date to 08-Mar-2010.
    * calwf3/wf3dth.c: Eliminated the creation of dummy drz products. Now done with PyDrizzle. (PR 64261; Trac #495)
    * lib/mkspt.c: Modified to allow for the case where there are no input spt files, in which case don't try to create or update the output spt header. (PR 64260; Trac #494)
    * wf32d/doflat.c: Modified divFlat to use mean_gain for all images, including grisms. (PR 64259; Trac #493)
    * wf3ir/blevcorr.c: Swapping order of zsig and blev such that zsig occurs first requires sending zoff image to blevcorr to be processed. (PR 64262; Trac #496)
    * wf3ir/cridcalc.c:
        * Added check for pixels already saturated in zeroth read (detected by zsigcorr), in which case outputs set to zero.
        * Switch from using commanded ccdgain to  mean_gain.
        * Modified linfit to include readnoise in sample weights and Poisson noise from source in final fit uncertainty.
        * Added SPIKE_THRESH in RejSpikes to use a separate  rejection threshold from CR thresh.
        * Updated hardwired dark and readnoise to use SMOV results. Some general cleanup. (PR 64630; Trac #518)
    * wf3ir/doir.c:
        * Changed order of processing so that doZsig is called before doBlev. This also requires passing zoff image to doBlev to get processed. (PR 64262; Trac #496)
	    * Compute zero-read sample time (sampzero) here instead of in zsigcorr. (PR 63711; Trac #457)
    * wf3ir/flatcorr.c: Modified mult_gain to use mean_gain for all images, including grisms. (PR 64259; Trac #493)
    * wf3ir/refdata.c:	Fixed initialization of maxcrsplit variable.
    * wf3ir/unitcorr.c: No longer need to check status of ZSIGCORR before using sampzero, because sampzero is always computed in doIR. (PR 63711; Trac #457)
    * wf3ir/zsigcorr.c:
        * Set ZEROSIG DQ values along with SATPIXEL flags. Set and count pixels as saturated in first read if they're saturated in zeroth read. Only check for saturation in first read if not already flagged as saturated in zeroth. For pixels saturated in zeroth or first reads, recompute zsig from difference of zeroth read and super-zero zsci. 	(PR 64262; Trac #496)
	    * Moved computation of sampzero into doIR. (PR 63711; Trac #457)

**Updates for Version 1.8.1 - 27 Oct 2009 (HAB):**
    * calwf3.cl, wf3ir.cl: Increment version to 27Oct2009.
    * wf3version.h: Increment version to 1.8.1 and date to 27-Oct-2009.
    * wf3ir/cridcalc.c: Fixed the crrej routine to use the logical OR of all input flags for the output DQ flag value for pixels that have all samples rejected, instead of simply flagging them all as SATURATED.	(PR 63806; Trac #459)

**Updates for Version 1.8  - 26 Oct 2009 (HAB):**
    * calwf3.cl: Increment version to 26Oct2009.
    * wf3version.h: Increment version to 1.8 and date to 26-Oct-2009.
    * wf3info.h: Added new "mean_gain" parameter to WF3Info structure. (PR 63788; Trac #458)
    * lib/getccdtab.c: Added computation of mean_gain to GetCCDTab. (PR 63788; Trac #458)
    * lib/wf3info.c: Added initialization of new mean_gain parameter. (PR 63788; Trac #458)
    * wf32d/doflat.c: Upgraded divFlat to use mean_gain when applying gain calibration, except for grism images, which still use the amp-dependent gain values.(PR 63788; Trac #458)
    * wf3ir/flatcorr.c: Upgraded mult_gain to use mean_gain when applying gain calibration, except for grism images, which still use the amp-dependent gain values. (PR 63788; Trac #458)

**Updates for Version 1.7  - 14 Oct 2009 (HAB):**
    * calwf3.cl: Increment version to 14Oct2009.
    * wf3version.h: Increment version to 1.7 and date to 14-Oct-2009.
    * wf3ir/cridcalc.c: Updated the crrej routine to use the badinpdq value from the CRREJTAB to set the DQIGNORE constant, which is used to reject samples, rather  than having it hardwired to a value in the code. The hardwired value  had been set to just SATPIXEL, which meant that pixels flagged with other values such as DETECTORPROB (4), BADZERO (8), HOTPIX (16), and UNSTABLE (32) were not being blanked out in the output flt image. (PR 63556; Trac ticket #454)
    * wf3ir/refdata.c: Updated the crrpar_in routine to report the value of badinpdq, now that it's being used in cridcalc. (PR 63556; Trac ticket #454)

**Updates for Version 1.6  - 17 Aug 2009 (HAB):**
    * calwf3.cl: Increment version to 17Aug2009.
    * wf3version.h: Increment version to 1.6 and date to 17-Aug-2009.
    * calwf3/wf3dth.c: Updated to set NEXTEND=3 in header of dummy drz file for IR images. (PR 63286; Trac ticket #436)
    * ib/mkspt.c: Updated mkNewSpt to count total number of input spt extensions before updating NEXTEND in output spt file. (PR 63286; Trac ticket #436)
    * wf3ir/flatcorr.c: Updated flatcorr routine to set BUNIT to electrons after gain correction has been applied. (PR 63063; Trac ticket #435)
    * wf3rej/cr_history.c: Updated to set NEXTEND=3 in header of output crj file for IR images. (PR 63286; Trac ticket #436)

**Updates for Version 1.5  - 24 Jun 2009 (HAB):**
    * calwf3.cl: Increment version to 24Jun2009.
    * wf3version.h: Increment version to 1.5 and date to 24-Jun-2009.
    * calwf3/procccd.c: Added logic to always use CRCORR=PERFORM internally for both CRJ and RPT associations, instead of using CRCORR for one and RPTCORR for the other.
    * wf3rej/rej_check.c:	Added logic to getampxy routine to reset ampx/ampy to correct values for IR subarray images. (PR 62948; Trac ticket #424)
    * wf3rej/rej_sky.c: Commented out print statement that had inadvertanly been left active in a previous delivery that was only intended for debugging use.

**Updates for Version 1.4.1  - 27 Apr 2009 (HAB):**
    * calwf3.cl: Increment version to 27Apr2009.
    * wf3version.h:	Increment version to 1.4.1 and date to 27-Apr-2009.
    * wf3ccd/doblev.c: Added verbose mode print statements to indicate the overscan column limits being used in the overscan calculations. (Trac ticket #405)
    * wf3ccd/findover.c: Fixed the logic that was used to compute the biassect values when dealing with a subarray that includes the physical overscan on the amp B/D edge of the image. (Trac ticket #405)

**Updates for Version 1.4  - 14 Apr 2009 (HAB):**
    * calwf3.cl: Increment version to 14Apr2009.
    * wf3version.h: Increment version to 1.4 and date to 14-Apr-2009.
    * lib/interpinfo.c: Added checks to make sure pixel fractions "q" and "p" come out between 0.0 and 1.0. (Trac ticket #325)
    * lib/unbin2d.c: Added checks to make sure pixel fractions "q" and "p" come out between 0.0 and 1.0. (Trac ticket #325)
    * lib/unbinline.c: Added checks to make sure argument of sqrt() is positive. (Trac #325)
    * wf32d/doflat.c: Fixed bugs that were causing the routine to crash when trying to interpolate a binned LFLTFILE and also added the capability to do a direct division into science image if they are the same size. Added forced return if LFLTFILE is binned, until we upgrade the interpolation routines to work better. (Trac ticket #325)
    * wf3ir/refdata.c: Fixed bugs in crrpar_in routine for calls to c_tbegti to read value of  IRRAMP column in each row of the crrejtab. (Trac ticket #392)
    * wf3ir/resistmean.c: Upgraded computations of mean and standard deviation to use double precision variables. Original single-precision calculations were giving different results on different computer platforms. Also did some	general code clean-up. (Trac ticket #391)

**Updates for Version 1.3  - 13 Mar 2009 (HAB):**
    * calwf3.cl: Increment version to 13Mar2009.
    * wf3version.h: Increment version to 1.3 and date to 13-Mar-2009.
    * wf3info.h: Added "crrej" to WF3Info structure for the CRREJTAB ref table, now that it's being used within calwf3 in wf3ir/cridcalc step. Previously, it was only accessed from within wf3rej. (Trac ticket #352)
    * wf3ccd/dobias.c: Updated to compute correct x-offset values for subarrays in the amp B and D quadrants, which need to take into account the columns of serial virtual overscan that are in the middle of a 4-amp bias reference  image. (Trac ticket #378)
    * wf3ir/cridcalc.c:
        * Added use of CRREJTAB to allow user input of CR rejection threshold instead of having it hardwired in the code.
        * Decreased max_CRs from 6 to 4. Reinstated old loop limits code that excludes reference pixels from ramp fitting. Fixed bug in logic that identifies pixels already saturated in first read.
        * Don't set HIGH_CURVATURE flag in ouput DQ  arrays, use UNSTABLE instead, and change messages to say UNSTABLE.
        * Also don't set ZEROSIG value in output crimage (flt file) DQ array, because those pixels are still OK (assuming no other flag also set).
        * Removed  unnecessary call to EstimateDarkandGlow at end of processing.
        * Fixed  calculation of output SAMP and TIME values.
        * Fixed bug in logic that  identifies pixels with only 1 good sample.
        * Fixed bug in computation of  "firstgood" and "lastgood" assignments for pixels with no acceptable samples.  (Trac tickets #352, 365, 376, 377, 381)
    * wf3ir/getirflags.c: Added new checkCRRej routine to check for the existence and correctness of the CRREJTAB ref table, for use in CRCORR. (Trac ticket #352)
    * wf3ir/refdata.c: Added crrpar_in routine to load parameters from CRREJTAB ref table, for use in CRCORR. (Trac ticket #352)

**Updates for Version 1.2a  - 20 Feb 2009 (HAB):**
    * calwf3.cl: Increment version to 20Feb2009.
    * wf3version.h: Increment version to 1.2a and date to 20-Feb-2009.
    * wf3rej/rej_loop.c: Fixed bug in test to exclude flagged pixels from being tested for CR's so that pixels previously marked as SPILL still get tested to see if  they qualify as a CR. (PR 62005)

**Updates for Version 1.2  - 29 Jan 2009 (HAB):**
    * calwf3.cl: Increment version to 29Jan2009.
    * wf3version.h: Increment version to 1.2 and date to 29-Jan-2009.
    * wf3.h: Added new parameter "type" to RefImage and RefTab structures, which contains the value of the FILETYPE keyword for each reference file. (PR 61608)
    * wf3dq.h: New WFC3 UVIS and IR DQ flag assignments. (PR 61741)
    * lib/div1d.c: Changed CALIBDEFECT macro to BADFLAT, to coincide with WFC3 DQ assignment changes. (PR 61741)
    * lib/getkeys.c: Eliminated use of default values for FILTER and CCDGAIN keywords, which means it will now be an error if they are missing. (PR 61608)
    * lib/imgpedigree.c: Upgraded to retrieve FILETYPE along with PEDIGREE/DESCRIP keywords.  (PR 61608)
    * lib/tabpedigree.c: Upgraded to retrieve FILETYPE along with PEDIGREE/DESCRIP keywords, and to retrieve these keywords from the primary HDU, not the table HDU. (PR 61608)
    * lib/trlbuf.c: Fixed bug in CloseTrlBuf causing an IRAF segv, which was due to a  call to fclose with a NULL pointer as argument. Removed the call. (PR 61164)
    * lib/wf3info.c: Added initialization of new 'type' parameter in InitRefImg and InitRefTab. Also added new CheckImgType, CheckTabType, CheckFilter, CheckDetector, and CheckGain routines. (PR 61608)
    * lib/whicherror.c: Added case of an invalid ref file to error message. (PR 61608)
    * wf32d/dophot.c: Added computation of PHOTFNU keyword value, to be consistent with IR photcorr process. Also removed some old ACS-specific code that is not used for WFC3. (PR 61138)
    * wf32d/get2dflags.c: Upgraded all the checkNNNN routines to verify correct FILETYPE for each reference file, as well as correct selection criteria such as DETECTOR, FILTER, and CCDGAIN. (PR 61608)
    * wf32d/photmode.c: Modified construction of photmode string to use separate UVIS1/UVIS2 keywords for the CCD chips, to add the new "cal" keyword for UVIS exposures, and to remove the "DN" keyword for IR exposures because  they're now in units of electrons. (PR 61497)
    * wf3ccd/blevdrift.c: Upgraded the cleanDriftFit routine to only use the good values returned by VMedianY in the computation of statistics and rejection of outliers in the array of bias values. Also added checks for potential divide-by-zero conditions. (PR 61698)
    * wf3ccd/doblev.c: Upgraded the cleanBiasFit routine to only use the good values returned by FindBlev in the computation of statistics and rejection of outliers in the array of bias values. Also added checks for potential divide-by-zero conditions. (PR 61698)
    * wf3ccd/getflags.c: Upgraded all the checkNNNN routines to verify the correct FILETYPE for reference file, as well as correct selection criteria such as DETECTOR, FILTER, and CCDGAIN. (PR 61608)
    * wf3ir/cridcalc.c: Reinstated code that had been inadvertantly removed from the calnica code ported to calwf3, which propogates CR DQ flags to all samples  following a hit. (PR 61425)
    * wf3ir/dqicorr.c: Updated to check for missing CCDGAIN and CCDAMP columns in BPIXTAB and default to a match with the science data (same logic as in lib/dodqi.c). (PR 61436)
    * wf3ir/flatcorr.c: Fixed bug in mult_gain routine that was doing out of bounds array access for subarray images. (PR 61428)
    * wf3ir/getirflags.c: Upgraded all of the checkNNNN routines to verify the correct FILETYPE for each reference file, as well as verifying a match with selection criteria such as DETECTOR and FILTER. (PR 61608)
    * wf3ir/refdata.c: Removed FILTER check from getFlatImage because that's now handled by checkFlat in getIRFlags. (PR 61608)
    * wf3ir/zsigcorr.c: Fixed bug in zsigcorr routine to compute correct zeroth read exposure time for subarray images, rather than using SAMPZERO keyword value, which is only correct for full-frame images. (PR 61347)
    * wf3rej/rej_loop.c: Fixed problems with DQ flags written to input and output DQ arrays, including not setting any SPILL flags (CR only), not setting CR flags in the ouput CRJ file for pixels that had at least 1 good input, and not propagating CR flags set for one input file into the remaining files in the input list. (PR 61819)

**Updates for Version 1.1  - 10 Oct 2008 (HAB):**
    * calwf3.cl: Increment version to 10Oct2008.
    * wf3version.h: Increment version to 1.1 and date to 10-Oct-2008.
    * calwf3/procccd.c: Fixed handling of EXPSCORR=PERFORM so that WF32D gets called for all images, and fixed save_tmp setting so that blv_tmp files get deleted after EXPSCORR processing.
    * wf32d/doflat.c: Added 'applygain' switch to divFlat to turn on/off the gain correction so that the gain will only be used to correct one ref file and not both, otherwise the gain will be applied twice to the science data.
    * wf3ccd/blevdrift.c:
        * Added new routine cleanDriftFit to reject outliers from parallel overscan array before fitting (as in serial routine cleanBiasFit).
	    * Added readnoise as an input argument to use in cleanDriftFit.
    * wf3ccd/blevfit.c: Modified fit report in BlevFit to indicate that results are for the serial overscan fit.
    * wf3ccd/doblev.c: Added readnoise as an input argument to BlevDrift. Modified cleanBiasFit to use different clip values on each pass through data.
    * wf3ir/flatcorr.c: Upgraded to convert data to units of electrons by multiplying by the gain after flat field has been applied. Uses new function "mult_gain".
    * wf3rej/rej_sky.c: Added capabilities for "mean" sky calculation, using resistmean.

**Updates for Version 1.0  - 11 Sep 2008 (HAB):**
    * calwf3.cl: Increment version to 11Sep2008.
    * wf3version.h: Increment version to 1.0 and date to 11-Sep-2008.
    * wf3info.h: Added ncoeff and nerr to NlinData structure.
    * wf3sizes.h: Removed this old include file, which isn't used anywhere.
    * wf3ir/blevcorr.c: Modified to use statistics from all ref pixels in each readout, rather than working quad-by-quad. Uses new statistics module "resistmean".
    * wf3ir/mkpkg: Added new module "resistmean.c" to library list.
    * wf3ir/nlincorr.c: Modified to use 3rd-order coeffs and new ncoeff, nerr members of NlinData struct.
    * wf3ir/refdata.c: Modified getNlinData and freeNlinData to use new ncoeff, nerr members of NlinData struct.
    * wf3ir/resistmean.c: New statistics module to compute resistant mean.

**Updates for Version 0.99 - 28 Aug 2008 (HAB):**
    * calwf3.cl: Increment version to 28Aug2008.
    * wf3version.h: Increment version to 0.99 and date to 28-Aug-2008.
    * calwf3/wf3init.c: Changed all occurences of "_dth" to "_drz".
    * calwf3/wf3table.c: Changed all occurences of "_dth" to "_drz".
    * lib/detnsegn.c: Removed unnecessary old ACS/HRC code and added WFC3/IR functionality.
    * lib/findroot.c: Changed all occurences of "_dth" to "_drz".
    * lib/getccdtab.c: Modified to only reset ampx for UVIS subarrays, not for IR.
    * lib/mkspt.c: Changed all occurences of "_dth" to "_drz".
    * wf3ir/doir.c: Added call to GetGrp at beginning of processing to load LTV offsets.
    * wf3ir/noiscalc.c: Upgraded to use separate gain and readnoise values for each amp quadrant of the images. Includes support for IR subarrays.
    * wf3rej/rej_do.c: Set non_zero=nimgs for case where all images have exptime=0, so that they'll still process using exptimes reset to 1.
    * wf3rej/rej_init.c: Fixed indexing of SQ(noise.val[0]) to SQ(noise.val[k]) in loop over amps so that appropriate readnoise values get used for each amp.

**Updates for Version 0.95 - 21 Jul 2008 (MS):**
    * calwf3.cl: Increment version to 21Jul2008.
    * wf3version.h: Increment version to 0.96 and date to 21-Jul-2008.
    * wf3ir/cridcal.c: Major rewrite to incorporate new CR rejection and err computation methods from latest calnica/n_cridcalc.c.

**Updates for Version 0.9 - 19 Jun 2008 (HAB):**
    * calwf3.cl: Increment version to 19Jun2008.
    * wf3version.h: Increment version to 0.9 and date to 19-Jun-2008.
    * calwf3/procir.c: Added logic and supporting functionality to call WF3Rej_0 to combine IR Repeat-Obs images into a crj product.
    * calwf3/wf3dth.c:  Restored old acsdth code for creating dummy dth output products, until  MultiDrizzle capability is added to WFC3 pipeline.
    * lib/mkspt.c: Corrected the calculation of the number of extensions in output spt files for WFC3 (IR files have a pair of extensions for each nsamp).
    * wf3rej/cr_history.c: Update RPTCORR, instead of CRCORR, for IR images. Required adding detector as input argument.
    * wf3rej/rej_do.c: Pass detector to cr_history.
    * wf3rej/rej_sky.c: Avoid arithmetic overflow in binning calculations.
    * wf3rej/wf3rej.c: Various updates to properly ID and handle IR images.

**Updates for Version 0.8 - 21 Dec 2007 (HAB):**
    * calwf3.cl: Increment version to 21Dec2007.
    * wf3dq.h: Change ZEROSIG DQ value from 4096 to 64, to leave 4096 free for Multidrizzle CR flag.
    * wf3version.h: Increment version to 0.8 and date to 21-Dec-2007. lib/dodqi.c: Use new FirstLast routine (provided by P. Hodge) to fix problems with indexing in binned images.
    * lib/mkspt.c: Added handling of SNAP1 extensions, in addition to UDL extensions, including appropriate mods to output NEXTEND.
    * wf3ir/blevcorr.c: Removed code put in place in previous version to swap quad indexes for images processed before a certain date, because all old images have now been reprocessed to latest orientation. Also updated quad numbering scheme to latest (1 in upperleft and going counter-clockwise from there).
    * wf3rej/rej_init.c, rej_loop.c, rej_sky.c: Added calls to hstio getHeader before each call to getShortLine, in order to prevent getShortLine from crashing on null input DQ arrays. In order to handle null arrays, getShortLine needs to access the image header.

**Updates for Version 0.7 - 09 May 2007 (HAB):**
    * calwf3.cl: Increment version to 09May2007.
    * wf3info.h: Added "subtype" to WF3Info structure for use with IR subarrays.
    * wf3version.h: Increment version to 0.7 and date to 09-May-2007.
    * calwf3/getinfo.c: Changed default gain for IR channel from 2.0 to 2.5 in GetIRInfo routine.
    * lib/dodqi.c: Modified to allow for wildcard values in BPIXTAB Amp, Gain, and Chip columns (following CALACS change).
    * lib/getkeys.c: Updated default gain for IR channel from 2.0 to 2.5. Added 'subtype' to list of IR keywords loaded. Changed default sampzero value to 2.911755 sec.
    * wf32d/do2d.c: Modified call to PhotMode to use science extension header, rather than primary header, because that's where phot keywords are.
    * wf32d/photmode.c:
        * Changed UVIS channel detector keyword to always use "UVIS1".
        * Changed use of "A2Dx" gain keyword to "DN" and eliminated use of it for UVIS images because flatfielding leaves them in units of electrons, not counts.
    * wf3ir/darkcorr.c: Eliminated use of RebinRef, because we don't want to extract subarrays from a full-frame dark ref image, we want to instead  use a matching subarray dark ref image.
    * wf3ir/getirflags.c: Added logic to checkDark to turn off zsigcorr if dark=dummy.
    * wf3ir/imageio.c:
        * Enhanced copyGroup to only copy filename if input name is not Null.
	    * Added new putCalDataSect routine.
    * wf3ir/refdata.c:
        * Reduced ALLOWDIFF from 0.1 to 0.01 for use with IR subarray  exptimes.
        * Added check for SUBTYPE in getDarkInfo.
    * wf3ir/wf3ir.c: Added use of new putCalDataSect routine to write out calibrated  images that have the ref pixels trimmed off.

**Updates for Version 0.61 - 01 Aug 2006 (HAB):**
    * calwf3.cl: Increment version to 01Aug2006.
    * wf3version.h: Increment version to 0.61 and date to 01-Aug-2006.
    * wf3ccd/doblev.c: Fixed logic used to select the appropriate readnoise value to pass to the FitToOverscan routine and to convert the readnoise value to units of DN, so that it matches the science data.
    * wf3ir/blevcorr.c: Enhanced the blevcorr routine to swap the quad indexes around for raw images generated before and after the date on which OPUS starting transposing the raw IR images.
    * wf3ir/flatcorr.c: Switched routine from multiplying by (inverse) flats to dividing by flats.
    * wf3ir/math.c: Upgraded adiv and adiv_noref routines to avoid divide by zero errors when computing output err values.

**Updates for Version 0.6 - 17 Jul 2006 (HAB):****
    * calwf3.cl: Increment version to 17Jul2006.
    * wf3version.h: Increment version to 0.6 and date to 17-Jul-2006.
    * calwf3/calwf3.c: CalWf3Run routine modified to remove updateAsnStat routine, because only OPUS should update the ASN_STAT keyword in asn tables.
    * calwf3/procccd.c: ProcessCCD routine modified to use new "wf3rej_msgtext" string variable to hold (potentially) very long list of input file names for printing. Sometimes too long for regular MsgText string variable.
    * calwf3/refexist.c: RefExist routine modified to include check for ref file names that are null (""), in addition to existing check for "N/A".
    * calwf3/wf3dth.c: InitDthTrl routine modified to fix "trl_in" memory allocation problem for holding long list of trailer file names.
    * calwf3/wf3table.c: getAsnTable routine modified to only populate sub-products if at least one input exists for that product.
    * lib/dodqi.c: DoDQI routine modified to properly handle binned images, and to adjust flagged pixel coords read from BPIXTAB for presence of serial virtual overscan in WFC3 raw images.
    * lib/mkoutname.c: MkOutName routine modified to include calls to "free", to free local memory before all error returns.
    * wf3ccd/blevdrift.c: VMedianY routine modified to fix bug in "if"-statement logic being  used to reject flagged pixels from the parallel overscan region. Flawed logic was allowing flagged pixels to remain in computation.
    * wf3ccd/findblev.c: FindBlev routine modified to fix bug in "if"-statement logic being used to reject flagged pixels from the serial overscan regions. Flawed logic was allowing flagged pixels to remain in computation.


**Updates for Version 0.5 - 08 Nov 2005 (HAB):**
    * calwf3.cl: Increment version to 08Nov2005.
    * wf3version.h: Increment version to 0.5 and date to 08-Nov-2005.
    * wf32d/do2d.c: Modified logic in OscnTrimmed routine to make it compatible with WFC3 binned images.
    * wf3ir/blevcorr.c: Fixed bug in calculation of j2 loop limit for reference pixel regions for quads 3 and 4.
    * wf3ir/nlincorr.c: Fixed bug in calculation of nlin ref image pixel indexes.
    * wf3ir/noiscalc.c: Fixed bug in noise computation by adding use of "noise2" variable to temporarily store value of readnoise-squared.
    * wf3ir/zsigcorr.c: Fixed bug in calculation of nlin ref image pixel indexes.

**Updates for Version 0.4 - 14 Feb 2005 (HAB):**
    * calwf3.cl: Increment version to 14Feb2005.
    * wf3rej.cl: Increment version to 14Feb2005.
    * wf3version.h: Increment version to 0.4 and date to 14-Feb-2005.
    * wf3ccd/findover.c: Enhanced FindOverscan routine to handle IR images differently than UVIS, selecting oscntab row based on image size (nx,ny) instead of binning.
    * wf3ir/blevcorr.c: Enhanced to set reference pixel statistics computation limits based on biassect values in oscntab, rather than image trim values.
    * wf3rej/wf3rej.c: Fixed memory reallocation in InitRejTrl that was causing a crash for very large numbers of input images. Made reallocation increment much larger, so that it doesn't get called repeatedly.

**Updates for Version 0.3 - 20 Feb 2004 (HAB):**
    * calwf3.cl: Increment version to 0.3.
    * wf3.h: Added ATOD_SATURATE macro definition.
    * wf3dq.h: Added ATODSAT dq value of 2048 and changed existing ZEROSIG from 2048 to 4096.
    * wf3version.h: Incremented version to 0.3 and date to 20-Feb-2004.
    * lib/dodqi.c:  Modified to make CCDAMP and CCDGAIN columns optional when looking for matching rows in BPIXTAB. Added handling of new ATODSAT dq flag.
    * lib/donoise.c: Fixed use of amp boundaries to take into account WFC3 serial virtual overscan regions.
    * lib/getccdtab.c: Changed use of wf3->binaxis to wf3->bin to make it work properly for binned science images.
    * lib/getgrp.c: Eliminated the ACS practice of hardwiring wf3->bin to 1 and instead populate it by reading BINAXIS keywords from sci extension header.
    * lib/getkeys.c: Eliminated attempt to read BINAXIS keywords from primary header because for WFC3 they're in the sci extension header.
    * lib/loadhead.c: Minor code cleanup.
    * wf3ccd/doblev.c:
        * Implemented limit on sdev to be sqrt(mean) for first pass in CleanBiasFit and use readnoise as value of sdev for second pass.
        * Added readnoise ('rn') as input to cleanBiasFit.
    * wf3ccd/doccd.c: Minor comment change.
    * wf3rej/rej_loop.c: Commented out unused LoadHdr function declaration. Removed SQ(scale*val) from sumvar computation. Changed AllocBitBuff to work with arbitrary buffer sizes rather than only those evenly divisible by 8.

**Updates for Version 0.2 - 28 Oct 2003 (HAB):**
    * wf3info.h:
        * Changed datatype of 'ccdgain' from int to float.
	    * Added 'blev(NAMPS)' to WF3Info struct so WF3CCD can remember all blev values for all extensions/amps.
        * Added 'expscorr' to WF3Info struct for use in WF32D.
    * wf3version.h: Incremented version to 0.2 and date to 28-Oct-2003.
    * wf3wild.h: Added 'FLT_WILDCARD' and 'FLT_IGNORE' macros for use in floating-pt get/put keyword functions.
    * calwf3/calwf3.h: Changed datatype of 'scigain' from int to float.
    * calwf3/calwf3.c: Removed unique code for RPTCORR processing and made it same as CRCORR for UVIS images.
    * calwf3/getinfo.c: Changed datatype of 'scigain' values from int to float.
    * calwf3/getrefffiles.c: Load 'CRREJTAB' ref table if RPTCORR is turned on (to make it same as CRCORR for UVIS images).
    * calwf3/getswitches.c: Changed to handle RPTCORR switch the same as CRCORR for UVIS images.
    * calwf3/procccd.c:
        * Changed to handle RPTCORR processing same as CRCORR for UVIS images.
	    * Added check on status value returned from WF3Rej. If set to 'NO_GOOD_DATA', it will reset 'wf3hdr->sci_basic_2d' to 'SKIPPED' so that no further processing will be performed. It then resets the status value to 'WF3_OK' for continuing normally.
    * calwf3/wf3table.c: Changed to handle RPTCORR processing same as CRCORR for UVIS images.
    * lib/wf3info.c: Added initialization of new wf3->blev array.
    * lib/dodqi.c: Updated to treat commanded gain values as float datatype instead of int.
    * lib/donoise.c: Added logic to use Amp C/D bias values from new blev array for UVIS Chip 2 instead of relying on 'AMPY' logic.
    * lib/getccdtab.c: Updated to treat commanded gain values as float datatype instead of int.
    * lib/getkeys.c: Updated to treat commanded gain values as float datatype instead of int.
    * lib/mkspt.c: Updated a couple of printf statements to use trlmessage so that the comments on creating the SPT file also make it to the trailer file.
    * lib/sameint.c: Added new 'SameFlt' routine for use with gain keyword values.
    * lib/trlbuf.c: Increased 'trldata' buffer size from 'SZ_FNAME' to 'SZ_LINE'.
    * lib/key.c: Changed putKeyBool function type from Bool to int.
    * wf32d/wf32d.c: Added 'expscorr' switch as command-line argument for wf32d.
    * wf32d/do2d.c: Update final state of 'expscorr' switch in output header.
    * wf32d/photmode.c: Updated to treat gain values as float datatype instead of int.
    * wf3ccd/wf3ccd.c: Populate BIASLEV[abcd] keywords in output header using new 'BiasKeywords' function.
    * wf3ccd/blevfit.c: Added BlevResults function to return the values of the slope and intercept computed for the bias fit. Also, the fit reports the values to the user in a trailer message.
    * wf3ccd/doatod.c: Updated to treat commanded gain values as float datatype instead of int.
    * wf3ccd/doblev.c:
        * Added 'cleanBiasFit' routine to do sigma-clipping on bias measurements before computing fit.
        * Set default ccdbias value to be AMP C/D value for UVIS Chip 2 data where no overscan was available for computing the bias level.
        * Modified to load the 'biassect' array with indexes corresponding to the serial physical overscan regions, instead of serial virtual overscan regions, when processing UVIS subarray images (which have noserial virtual overscan).
    * wf3ccd/doccd.c:
        * Added processing msg's giving info on bias levels for each amp.
	    * Upgraded to do correct overscan trimming of output image for UVIS subarray modes, in which there's no serial virtual overscan to remove, and variable amounts of serial physical overscan.
    * wf3ccd/findover.c: Modified to zero-out all serial and parallel virtual biassect and  trim values when processing UVIS subarray images (which don't have any virtual overscan). Also fixed a bug in which one of the biassect values was not being converted from 1-indexed to 0-indexed in the case of subarray images.
    * wf3ir/dqicorr.c: Updated to treat commanded gain values as float datatype instead of int.
    * wf3ir/getirflags.c: Modified to load DARKCORR and NLINCORR switch settings and DARKFILE and NLINFILE ref file info if ZSIGCORR is set to PERFORM.
    * wf3ir/nlincorr.c: Modified to use just 1 node array from the NLINFILE ref data, which is the saturation value. There won't be another node array specifying the lower bound of the nlin correction as with NICMOS.
    * wf3ir/refdata.c:
        * Modified to load just 1 node array from the NLINFILE ref file.
        * Also modified to combine all of the PFLT, DFLT, and LFLT ref file data (if present) into a master flat, as is done for UVIS processing.
    * wf3ir/zsigcorr.c: Modified to use just 1 node array from the NLINFILE ref data, which is the saturation value.
    * wf3rej/wf3rej.c: Added call to 'mkNewSpt' within error condition for wf3rej_do to always produce a new SPT file for product when possible. This also involved remembering the value of the error condition, setting it to WF3_OK, calling 'mkNewSpt', then resetting to old value in order to allow 'mkNewSpt' to work successfully.
    * wf3rej/rej_do.c:
        * Added code to count number of inputs with exptime>0. If some are zero, new code will insure that first good image gets used to initialize the initial guess image.
        * Revised to handle cases where 0,1,or more input are valid. If none have exptime>0, skips wf3rej_loop altogether and output a blank image with DQ values of 1 and ERR values of 0 with the exception of the 0,0 pixel, which have values of 8 and 	-1 respectively, to forces HSTIO to write out the image arrays. It now returns status=NO_GOOD_DATA if there are no inputs with  exptime>0.
    * wf3rej/rej_init.c:
        * Added code to count number of inputs with exptime>0.
        * Also now checks whether exptime!=0 when building initial guess image.
    * wf3rej/rej_loop.c: Added code to avoid crashing when exp[n]=0 for an input image. It will now skip all the detection code when exp[n]=0.
    * wf3rej/cr_scaling.c: Added trailer file comments to better describe how exptime=0 cases are handled.

**Updates for Version 0.1 - 26 Nov 2002 (HAB):**
    * Initial installation of baseline CALWF3 into stlocal$testwf3 pkg.
