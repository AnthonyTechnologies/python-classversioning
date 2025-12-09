"""__init__.py
Reusable test suites for the classversioning project.

Leave one blank line. These suites are thin wrappers built on baseobjects.testsuite base classes so that downstream
projects can subclass and supply concrete example classes and cases.
"""

# Header #
__package_name__ = "classversioning"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "0.8.0"


# Imports #
# Local Packages #
from .versionedclasstestsuite import VersionedClassTestSuite
from .versionedmetatestsuite import VersionedMetaTestSuite
from .versionregistrytestsuite import VersionRegistryTestSuite

__all__ = ["VersionRegistryTestSuite", "VersionedClassTestSuite", "VersionedMetaTestSuite"]
