"""Licensed under a 3-clause BSD style license - see LICENSE.rst."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pytest
from wfc3tools import calwf3


def test_no_valid_input():
    """Run a very simple aliveness test."""
    with pytest.raises(IOError) as e:
        def cal():
            calwf3()
        cal()
    assert 'No valid image specified' in str(e.value)


def test_version_print():
    """Make sure no error results from version print."""
    def cal():
        calwf3(version=True)
    cal()
