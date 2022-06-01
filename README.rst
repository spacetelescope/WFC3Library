WFC3Library
===========

.. image:: https://readthedocs.org/projects/wfc3tools/badge/?version=latest
    :target: http://wfc3tools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

Here the user will find the latest Python-based software notebooks for the Wide Field Camera 3 (WFC3) on the Hubble Space Telescope (HST). For our primary WFC3 user-support tools, see `wfc3tools <https://github.com/spacetelescope/wfc3tools>`_ and `WFC3 Software Tools <https://www.stsci.edu/hst/instrumentation/wfc3/software-tools>`_.

WFC3Library is the primary repository for new notebooks, including color correction, photometric tools, spectroscopic tools, and other analysis. This repository contains the complementary notebooks mentioned in the `WFC3 Data Handbook <https://hst-docs.stsci.edu/wfc3dhb>`_. These notebooks include:

- Manual Recalibration of Images using CALWF3
- WFC3/UVIS Filter Transformations with stsynphot
- Flux Unit Conversions with synphot and stsynphot
- Synthetic Photometry Examples for WFC3
- WFC3/UVIS Time-dependent Photometry
- Calculating WFC3 Zeropoints with STSynphot
- WFC3 Image Displayer and Analyzer
- Masking Persistence in WFC3/IR Images
- How to use `wfc3_dash` on DASH data
- Processing WFC3/UVIS Data with CALWF3 Using the v1.0 CTE-Correction
- Exception Report Checklist - WFC3

Each folder in ``notebooks`` has an individual ``README.md`` with further details and a HTML file that can be opened in a browser after cloning this repository. The HTML file is identical to the notebook, except they contain output plots and tables.

Installation
------------

All notebooks require the same anaconda virtual environment named ``wfc3_env``. To create the virtual environment, run this line in a terminal window:

::

    conda env create -f environment.yml

To activate ``wfc3_env``, run this line in a terminal window:

::

    conda activate wfc3_env

In addition, the individual ``README.md`` files in ``notebooks`` may have further installation instructions. Please read them to run the notebooks properly.

With the environment activated and additional libraries installed based on the individual ``README.md`` files, you will be able to complete the notebooks.

Contributing
------------

Please open a new issue or new pull request for bugs, feedback, or new features
you would like to see.   If there is an issue you would like to work on, please
leave a comment and we will be happy to assist.   New contributions and
contributors are very welcome!

WFC3Library follows the `Astropy Code of Conduct`_ and strives to provide a
welcoming community to all of our users and contributors.

Want more information about how to make a contribution?  Take a look at
the the astropy `contributing`_ and `developer`_ documentation.


License
-------

WFC3Library is licensed under a 3-clause BSD style license (see the ``LICENSE.txt`` file).

.. _contributing: http://docs.astropy.org/en/stable/index.html#contributing
.. _developer: http://docs.astropy.org/en/stable/index.html#developer-documentation
.. _Astropy Code of Conduct:  http://www.astropy.org/about.html#codeofconduct
