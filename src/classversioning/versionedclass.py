"""versionedclass.py
VersionedClass is an abstract class which has an associated version which can be used to compare against other
VersionedClasses. Typically, a base class for a version schema should directly inherit from VersionedClass then the
actual versions should inherit from that base class.
"""
# Package Header #
from .header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any, ClassVar, Iterable

# Third-Party Packages #
from baseobjects.versioning import Version
from baseobjects.classregistration import DispatchableClass

# Local Packages #
from .meta import VersionedMeta
from .versionregistry import VersionRegistry


# Definitions #
# Classes #
class VersionedClass(DispatchableClass, metaclass=VersionedMeta):
    """An abstract class allows child classes to specify its version which it can use to compare and dispatch.

    Class Attributes:
        class_registry: A registry of all subclasses and versions of this class.
        _dispatch_kwarg: The name of the kwarg to use for version dispatching when a new object is made.
        _registration: Specifies if versions will be tracked and will recurse to parent.
        _VERSION_TYPE: The type of version this object will be.
        VERSION: The version of this class as a string.
    """
    # Class Attributes #
    class_registry: ClassVar[VersionRegistry | None] = None

    VERSION_TYPE: ClassVar[type[Version] | None] = None
    VERSION: ClassVar[Version | None] = None

    _dispatch_kwarg: str = "obj"

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, namespace: str | None = None, name: str | None = None, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            **kwargs: Keyword arguments for creating a subclass.
        """
        super().__init_subclass__(namespace, name, **kwargs)

        # Add subclass to the registry.
        if cls.class_registration and not isinstance(cls.VERSION, cls.VERSION_TYPE):
            cls.VERSION = cls.VERSION_TYPE(cls.VERSION)

    # Registry
    @classmethod
    def register_class(cls, group: str = "default") -> None:
        """Registers this class with the given namespace and name.

        Args:
            group: The group of versioned classes to register this class to.
        """
        cls.class_registry.register_class(cls, group)

    @classmethod
    def get_registered_class(
        cls,
        version: Version | str | Iterable,
        exact: bool = False,
        group: str = "default",
        sort: bool = False,
        module: str | None = None,
    ) -> "VersionedClass":
        """Gets a class based on the version.

        Args:
            version: The key to search for the class with.
            group: The group of versioned classes to get.
            exact: Determines whether the exact version is need or return the closest version.
            sort: If True, sorts the registry before getting the class.
            module: The module to import if the class is not found.

        Returns:
            obj: The class found.
        """
        return cls.get_version_class(version, exact=exact, group=group, sort=sort, module=module)

    # Version
    @classmethod
    def get_version_from_object(cls, obj: Any) -> Version | str | Iterable:
        """An optional abstract method that must return a version from an object."""
        raise NotImplementedError("This method needs to be set in the version head to dispatch the propper class.")

    @classmethod
    def get_version_class(
        cls,
        version: Version | str | Iterable,
        exact: bool = False,
        group: str = "default",
        sort: bool = False,
        module: str | None = None,
    ) -> "VersionedClass":
        """Gets a class based on the version.

        Args:
            version: The key to search for the class with.
            group: The group of versioned classes to get.
            exact: Determines whether the exact version is need or return the closest version.
            sort: If True, sorts the registry before getting the class.
            module: The module to import if the class is not found.

        Returns:
            obj: The class found.
        """
        if sort:
            cls.class_registry.sort(group)

        return cls.class_registry.get_class(version, exact=exact, group=group, module=module)

    @classmethod
    def get_latest_version_class(cls, group: str = "default", sort: bool = False) -> "VersionedClass":
        """Gets a class based on the latest version.

        Args:
            group: The group of versioned classes to get.
            sort: If True, sorts the registry before getting the class.

        Returns:
            obj: The class found.
        """
        if sort:
            cls.class_registry.sort(group)

        return cls.class_registry.get_latest_version(group)
