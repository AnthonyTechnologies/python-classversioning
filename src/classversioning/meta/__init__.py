"""__init__.py
Meta classes for class versioning.

This subpackage exposes metaclasses that add version-aware behaviors to classes
in the classversioning library.
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
from .versionedmeta import VersionedMeta
from .versionedinitmeta import VersionedInitMeta
