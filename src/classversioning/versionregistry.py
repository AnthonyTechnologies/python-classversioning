"""versionregistry.py
VersionRegistry creates registries of the Versions which keep track of several versioning schemas. For example, there
could be two different file types that both use TriNumberVersions, this registry keeps the class versions from these
different files separate from each other.
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
import bisect
from importlib import import_module
from typing import Any
from warnings import warn

# Third-Party Packages #
from baseobjects import SEARCHSENTINEL
from baseobjects.classregistration import BaseClassRegistry

# Local Packages #


# Definitions #
# Constants #
# Classes #
class VersionRegistry(BaseClassRegistry):
    """A dictionary like class that holds versioned objects.

    The keys distinguish different types of objects from one another, so their version are not mixed together. The items
    are lists containing the versioned objects in order by version.
    """

    # Instance Methods #
    # Registry
    def register_class(self, cls: type, group: str = "default") -> None:
        """Adds a versioned item into the registry.

        Args
            cls: The versioned cls to add to the registry.
            type_: The type of versioned object to add.
        """
        if self.head_class is not None and not isinstance(cls.VERSION, self.head_class.VERSION_TYPE):
            raise TypeError(
                f"The registered class {str(cls)} has a version type of {str(cls.VERSION.VERSION_TYPE)} "
                f"which is not compatible with the registry's head class {str(self.head_class)}."
            )

        if (versions := self.data.get(group, None)) is not None:
            bisect.insort(versions, cls)
        else:
            self.data[group] = [cls]
    
    def get_class(
        self,
        key: Any,
        exact: bool = False,
        group: str = "default",
        module: str | None = None,
        default: Any = SEARCHSENTINEL,
    ) -> Any:
        """Gets an object from the registry based on the type and version of object.

        Args:
            key: The key to search for the versioned object with.
            exact: Determines whether the exact version is need or return the closest version.
            group: The group of versioned classes to get.
            module: The module to import if the version does not exist.
            default: A default object to return if a version cannot be found.

        Returns
            obj: The versioned object.

        Raises
            ValueError: If there is no closest version.
        """
        # Get Versions
        if (group_versions := self.data.get(group, None)) is None and module is not None:
            try:
                import_module(module)
            except Exception as e:
                warn(f"Failed to import module '{module}' with error: {e}, skipping.")
            else:
                group_versions = self.data.get(group, None)

        if group_versions is None:
            if default is SEARCHSENTINEL:
                raise KeyError(f"Group '{group}' not found.")
            else:
                return default

        # Ensure key is the correct type
        if not isinstance(key, self.head_class.VERSION_TYPE):
            key = self.head_class.VERSION_TYPE.cast(key)

        # Search for version
        index = group_versions.index(key) if exact else bisect.bisect_left(group_versions, key)
        if index < 0:
            try:
                import_module(module)
            except Exception as e:
                warn(f"Failed to import module '{module}' with error: {e}, skipping.")
            else:
                index = group_versions.index(key) if exact else bisect.bisect_left(group_versions, key)

        if index < 0:
            if default is SEARCHSENTINEL:
                raise ValueError(f"Version needs to be greater than {str(group_versions[0])}, {str(key)} is not.")
            else:
                return default
        else:
            return group_versions[index]

    def get_latest_version(self, group: str = "defualt", default: Any = SEARCHSENTINEL) -> Any:
        """Gets an object from the registry based on the type and the latest version of that object.

        Args:
            group: The group of versioned classes to get.
            default: A default object to return if a version cannot be found.

        Returns
            obj: The versioned object.
        """
        versions = self.data.get(group, None)
        return versions[-1] if versions or default is SEARCHSENTINEL else default

    def get_version_type(self) -> type:
        """Gets the type of version being used.

        Returns:
            The type of version being used.
        """
        return self.head_class.VERSION_TYPE

    def sort(self, group: str = "default", **kwargs: Any) -> None:
        """Sorts the registry.

        Args:
            group: The group of versioned classes to sort.
            **kwargs: Keyword arguments that are passed to the list sort function.
        """
        self.data[group].sort(**kwargs)
