"""versionregistry.py
A registry for grouping and retrieving versioned classes.

VersionRegistry stores versioned classes in groups so their versions are not mixed. For example, two different file
formats may both use the same Version type; this registry keeps their class versions separate.
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
import bisect
from importlib import import_module
from typing import TYPE_CHECKING, Any
from warnings import warn

# Third-Party Packages #
from baseobjects import SEARCHSENTINEL
from baseobjects.classregistration import BaseClassRegistry

if TYPE_CHECKING:  # Avoid circular imports but retain type checking.
    # Local Packages #
    from .versionedclass import VersionedClass


# Definitions #
# Classes #
class VersionRegistry(BaseClassRegistry):
    """A dictionary-like registry that holds versioned classes.

    Keys represent groups of related classes so their versions are not mixed. Each group's value is a list of classes
    ordered by their version.
    """

    # Attributes #
    head_class: type[VersionedClass] | None

    # Instance Methods #
    def _load_module(self, module: str) -> bool:
        """Loads a module if it exists.

        Args:
            module: The name of the module to load.

        Returns:
            True if the module was successfully imported, False otherwise.
        """
        try:
            import_module(module)
        except Exception as e:
            msg = f"Failed to import module '{module}' with error: {e}, skipping."
            warn(msg, stacklevel=2)
            return False
        else:
            return True

    # Registry
    def register_class(self, cls: Any, group: str | None = "default", *args: Any, **kwargs: Any) -> None:
        """Adds a versioned class to the registry.

        Args:
            cls: The versioned class to add to the registry.
            group: The group name under which to register the class.
            *args: Positional arguments to pass to the registry.
            **kwargs: Keyword arguments to pass to the registry.

        Raises:
            TypeError: If the class version type is incompatible with the registry head class.
        """
        if group is None:
            group = "default"

        if (
            self.head_class is not None
            and self.head_class.VERSION_TYPE is not None
            and not isinstance(cls.VERSION, self.head_class.VERSION_TYPE)
        ):
            msg = (
                f"The registered class {cls!s} has a version type of {cls.VERSION.VERSION_TYPE!s} "
                f"which is not compatible with the registry's head class {self.head_class!s}."
            )
            raise TypeError(msg)

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
        """Gets a class from the registry based on the requested version.

        Args:
            key: The key to search for (e.g., a version or value castable to the version type).
            exact: If True, require an exact version match; otherwise return the closest version.
            group: The group of versioned classes to search.
            module: Optional module to import if the version does not exist yet in the registry.
            default: A default value to return if a class cannot be found.

        Returns:
            The versioned class corresponding to the requested version.

        Raises:
            KeyError: If the group does not exist and no default is provided.
            ValueError: If no suitable version exists and no default is provided.
        """
        # Get Versions
        if (group_versions := self.data.get(group, None)) is None and module is not None and self._load_module(module):
            group_versions = self.data.get(group, None)

        if group_versions is None:
            if default is SEARCHSENTINEL:
                msg = f"Group '{group}' not found."
                raise KeyError(msg)
            return default

        # Ensure key is the correct type
        if (
            self.head_class is not None
            and self.head_class.VERSION_TYPE is not None
            and not isinstance(key, self.head_class.VERSION_TYPE)
        ):
            key = self.head_class.VERSION_TYPE.cast(key)

        # Search for version
        index = -1
        if exact:
            try:
                index = group_versions.index(key)
            except ValueError:
                if module is not None and self._load_module(module):
                    try:
                        index = group_versions.index(key)
                    except ValueError:
                        index = -1
                else:
                    index = -1

        if not exact:
            index = bisect.bisect_right(group_versions, key) - 1
            if index < 0 and module is not None and self._load_module(module):
                index = bisect.bisect_right(group_versions, key) - 1

        if index < 0:
            if default is SEARCHSENTINEL:
                if exact:
                    msg = f"Exact version {key!s} not found."
                else:
                    msg = f"Version needs to be greater than {group_versions[0]!s}, {key!s} is not."
                raise ValueError(msg)
            return default
        else:
            return group_versions[index]

    def get_latest_version(self, group: str = "default", default: Any = SEARCHSENTINEL) -> Any:
        """Gets the latest versioned class from the registry.

        Args:
            group: The group of versioned classes to get.
            default: A default value to return if a class cannot be found.

        Returns:
            The class with the latest version for the specified group, or `default` if none exists.

        Raises:
            KeyError: If the group does not exist and no default is provided.
        """
        versions = self.data.get(group, None)
        if versions:
            return versions[-1]

        if default is SEARCHSENTINEL:
            msg = f"Group '{group}' not found or empty."
            raise KeyError(msg)
        return default

    def get_version_type(self) -> type | None:
        """Gets the type of version being used.

        Returns:
            The version type used by the head class for this registry.
        """
        if self.head_class is None:
            return None
        return self.head_class.VERSION_TYPE

    def sort(self, group: str = "default", **kwargs: Any) -> None:
        """Sorts the registry.

        Args:
            group: The group of versioned classes to sort.
            **kwargs: Keyword arguments that are passed to the list sort function.
        """
        self.data[group].sort(**kwargs)
