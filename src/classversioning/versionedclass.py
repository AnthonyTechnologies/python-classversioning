"""versionedclass.py
A base class for versioned subclass hierarchies.

This module provides VersionedClass, an abstract base that associates each subclass with a version to enable comparison
and dispatch based on version. Typically, a concrete "head" class for a version schema should inherit directly from
VersionedClass, and concrete versioned implementations should inherit from that head class.
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
    """Abstract base class for versioned subclass hierarchies.

    Subclasses may specify a VERSION that is used for comparison and dispatch. A head class defines VERSION_TYPE, and
    concrete implementations inherit from the head and set VERSION accordingly.

    Attributes:
        class_registry: Registry of subclasses grouped by version.
        VERSION_TYPE: The version type for this hierarchy.
        VERSION: The version value associated with this class.
        _dispatch_kwarg: The keyword name used for dispatch during construction.
    """
    # Class Attributes #
    class_registry: ClassVar[VersionRegistry | None] = None
    default_group: ClassVar[str] = "default"

    VERSION_TYPE: ClassVar[type[Version] | None] = None
    VERSION: ClassVar[Version | None] = None

    _dispatch_kwarg: str = "obj"

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, group: str | None = None, **kwargs: Any) -> None:
        """Initializes a newly created subclass.

        Args:
            group: The group of versioned classes to register this subclass to.
            **kwargs: Additional keyword arguments for subclass creation.
        """
        # Cast VERSION to VERSION_TYPE #
        if cls.class_registration and not isinstance(cls.VERSION, cls.VERSION_TYPE):
            cls.VERSION = cls.VERSION_TYPE(cls.VERSION)

        # Register the Subclass #
        register_kwargs = {"group": (cls.default_group if group is None else group)}
        super().__init_subclass__(register_kwargs, **kwargs)

    @classmethod
    def get_class_information(cls, obj: Any, **kwargs: Any) -> tuple[Any]:
        """Gets the version from an object to dispatch to the correct subclass.

        Args:
             obj: The object to get the version from.
             **kwargs: Keyword arguments.

        Returns:
            A tuple containing the version of the object.
        """
        version = cls.get_version_from_object(obj)
        return (version,)

    # Registry
    @classmethod
    def get_registered_class(
        cls,
        version: Version | str | Iterable,
        exact: bool = False,
        group: str | None = None,
        sort: bool = False,
        module: str | None = None,
    ) -> "VersionedClass":
        """Gets a registered class based on the version.

        Args:
            version: The version key to search for the class with.
            exact: If True, require an exact version match; otherwise return the closest version.
            group: The group of versioned classes to search.
            sort: If True, sort the registry before getting the class.
            module: Optional module to import if the class is not found.

        Returns:
            The class matching the requested version.
        """
        if group is None:
            group = cls.default_group
        return cls.get_version_class(version, exact=exact, group=group, sort=sort, module=module)

    # Version
    @classmethod
    def get_version_from_object(cls, obj: Any) -> Version | str | Iterable:
        """Returns a version extracted from an object.

        This abstract method should be implemented by the head class to support dispatching to the proper versioned
        subclass based on the provided object. For example, the object could be a file, and this method would read the
        file and find the version.

        Args:
            obj: The object from which to extract the version.

        Returns:
            The version, or a value that can be cast to the version type.
        """
        raise NotImplementedError("This method needs to be set in the version head to dispatch the proper class.")

    @classmethod
    def get_version_class(
        cls,
        version: Version | str | Iterable,
        exact: bool = False,
        group: str | None = None,
        sort: bool = False,
        module: str | None = None,
    ) -> "VersionedClass":
        """Gets a class based on the requested version.

        Args:
            version: The version key to search for the class with.
            exact: If True, require an exact version match; otherwise return the closest version.
            group: The group of versioned classes to search.
            sort: If True, sort the registry before getting the class.
            module: Optional module to import if the class is not found.

        Returns:
            The class matching the requested version.
        """
        if group is None:
            group = cls.default_group

        if sort:
            cls.class_registry.sort(group)

        return cls.class_registry.get_class(version, exact=exact, group=group, module=module)

    @classmethod
    def get_latest_version_class(cls, group: str | None = None, sort: bool = False) -> "VersionedClass":
        """Gets the class with the latest available version.

        Args:
            group: The group of versioned classes to query.
            sort: If True, sort the registry before retrieving the class.

        Returns:
            The class associated with the latest version in the specified group.
        """
        if group is None:
            group = cls.default_group

        if sort:
            cls.class_registry.sort(group)

        return cls.class_registry.get_latest_version(group)
