WFC3Library
===========
> [!WARNING]
> This library is deprecated and the repository has been archived.
>
>  For all properly maintained WFC3 notebooks, please see [HST Notebooks](https://github.com/spacetelescope/hst_notebooks).**

Here the user will find the latest Python-based software notebooks for the Wide
Field Camera 3 (WFC3) on the Hubble Space Telescope (HST). For our primary WFC3
user-support tools, see [wfc3tools](https://github.com/spacetelescope/wfc3tools) and 
[WFC3 Software Tools](https://www.stsci.edu/hst/instrumentation/wfc3/software-tools).

WFC3Library is the primary repository for Jupyter notebooks, including general tools, 
WFC3/IR, time variable background (TVB), and photometry. This repository contains the 
complementary notebooks mentioned in the [WFC3 Data Handbook](https://hst-docs.stsci.edu/wfc3dhb). 
These notebooks include:

General Tools:
- WFC3 Image Displayer and Analyzer
- Exception Report Checklist - WFC3
- Processing WFC3/UVIS Data with `calwf3` Using the v1.0 CTE-Correction

WFC3/IR:
- Masking Persistence in WFC3/IR Images
- How to use `wfc3_dash` on DASH data

WFC3/IR Time Variable Background (TVB):
- WFC3/IR IMA Visualization Tools with an Example of Time Variable Background
- Manual Recalibration of Images using `calwf3`: Turning off the WFC3/IR Linear Ramp Fit
- Correcting for Helium Line Emission Background in WFC3/IR Exposures using the "Flatten-Ramp" Technique
- Correcting for Scattered Light in WFC3/IR Exposures: Manually Subtracting Bad Reads
- Correcting for Scattered Light in WFC3/IR Exposures: Using `calwf3` to Mask Bad Reads

Photometry:
- WFC3/UVIS Filter Transformations with `stsynphot`
- Flux Unit Conversions with `synphot` and `stsynphot`
- Synthetic Photometry Examples for WFC3
- WFC3/UVIS Time-dependent Photometry
- Calculating WFC3 Zeropoints with `stsynphot`
- WFC3/UVIS Pixel Area Map Corrections for Subarrays

Each folder in `notebooks` has an individual `README.md` with further 
details and a HTML file that can be opened in a browser after cloning this 
repository. The HTML file is identical to the notebook, except they contain 
output plots and tables.

License
-------

WFC3Library is licensed under a 3-clause BSD style license (see the `LICENSE.txt` file).
