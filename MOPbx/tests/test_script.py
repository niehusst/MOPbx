import pytest
from MOPbx.src.mopbx import main

"""
To test:

* empty .strings files removed from file system (and pbx)
* remove .strings files from fs where source xib not present in fs (and pbx)
* rm pbx refs to files not in fs
* clean pbx/fs not changed


test mode should return string (or write local file?) that we can compare to a corresponding manually fixed pbx (stored outside the ios proj) AND not delete any files that it would have, and rather just store them in array w/o rm them
"""


def test_example():
    assert 2+2 == 4


