"""versionedmeta_test.py
Tests for VersionedMeta metaclass.
"""

# Header #
__package_name__ = "classversioning"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "0.8.0"


# Imports #
# Source Packages #
from classversioning.meta import VersionedMeta
from classversioning.testsuite import VersionedMetaTestSuite


# Definitions #
# Classes #
class TestVersionedMeta(VersionedMetaTestSuite):
    """Tests for VersionedMeta."""
    UnitTestMeta = VersionedMeta
