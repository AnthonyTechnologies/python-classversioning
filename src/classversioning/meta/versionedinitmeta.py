"""versionedinitmeta.py
A metaclass combining initialization hooks with version comparisons.

VersionedInitMeta merges the initialization behavior of InitMeta with the
version-aware comparison features provided by VersionedMeta.
"""

# Header #
__package_name__ = "classversioning"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "0.8.0"


# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects.metaclasses import InitMeta

# Local Packages #
from .versionedmeta import VersionedMeta


# Definitions #
# Meta Classes #
class VersionedInitMeta(InitMeta, VersionedMeta):
    """Metaclass combining initialization hooks with version comparisons.

    Merges the initialization behavior of InitMeta with the version-aware comparison features provided by VersionedMeta.
    """
