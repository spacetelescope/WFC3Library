WFC3Library
===========

.. image:: https://readthedocs.org/projects/wfc3tools/badge/?version=latest
    :target: http://wfc3tools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :target: http://www.astropy.org
    :alt: Powered by Astropy Badge

This repository contains wfc3tools with updated documentation.
For more information please see the `online documentation <http://wfc3tools.readthedocs.io/>`_.

In addition, WFC3 Library contains complimentary notebooks mentioned in the `WFC3 Data Handbook <https://hst-docs.stsci.edu/wfc3dhb>`_. These notebooks include:

- Manual Recalibration of Images using CALWF3
- WFC3 UVIS Filter Transformations with stsynphot
- Flux Unit Conversions with synphot and stsynphot
- Synphot and STSynphot Examples for WFC3
- WFC3 UVIS Time-dependent Photometry
- Calculating WFC3 Zeropoints with STSynphot

Each folder in `notebooks` has an individual README.md with further details.

Installation
------------

All notebooks require the same anaconda virtual environment named `wfc3_env`. To create the virtual environment, run this line in a terminal window:

::

    conda env create -f environment.yml

To activate `wfc3_env`, run this line in a terminal window:

::

    conda activate wfc3_env

With the environment activated, you will be able to complete the notebooks.

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
