"""__init__.py
Tools for creating versioned class hierarchies.

A VersionedClass is structured so that subclasses can optionally define a version which can be used to compare with
other subclasses and for dispatch. The framework can also be used by instances of these classes, but it is primarily
focused on versioning classes. Versioning is useful for creating classes that interface with data structures that change
frequently while maintaining support for previous versions. For example, a file format may change how data is stored, but
you might have both new and previous versions. In this case, an appropriate class addressing each version can be chosen
based on the class' version.
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
from baseobjects.versioning import *
from .meta import *
from .versionregistry import VersionRegistry
from .versionedclass import VersionedClass
