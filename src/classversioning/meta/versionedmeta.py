"""versionedmeta.py
A metaclass that enables version-aware class comparisons.

VersionedMeta classes are augmented so they may be ordered based on a class attribute, VERSION. It enables comparing
classes (and versions) using standard comparison operators, provided a VERSION_TYPE and VERSION are defined in the
class.
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
from typing import Any

# Third-Party Packages #
from baseobjects import BaseMeta
from baseobjects.versioning import Version

# Local Packages #


# Definitions #
# Classes #
class VersionedMeta(BaseMeta):
    """A metaclass that enables version-aware class comparisons.

    Classes using this metaclass can define a version type and a version value to support ordering and equality
    comparisons using standard operators.

    Attributes:
        VERSION_TYPE: The concrete version type used by classes (e.g., Version).
        VERSION: The version value associated with the class (an instance of VERSION_TYPE).
    """
    VERSION_TYPE: type | None = None
    VERSION: Version | None = None

    # Magic Methods
    # Representation
    def __hash__(self) -> int:
        """Overrides hash to make the class hashable.

        Returns:
            The system ID of the class.
        """
        return id(self)

    # Comparison
    def __eq__(cls, other: Any) -> bool:
        """Returns True if the classes are equal considering their versions.

        Args:
            other: The object to compare against this class.

        Returns:
            True if equivalent to this class, including version.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if id(cls) == id(object):
                return True
            elif cls.VERSION_TYPE != other.VERSION_TYPE:
                return False
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        elif cls.VERSION is not None:
            try:
                other_version = cls.VERSION.cast(other)
            except TypeError:
                return super().__eq__(other)
        else:
            return super().__eq__(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION == other_version
        else:
            raise TypeError(f"'==' not supported between instances of '{str(cls)}' and '{str(other)}'")

    def __ne__(cls, other: Any) -> bool:
        """Returns True if the classes are not equal considering their versions.

        Args:
            other: The object to compare against this class.

        Returns:
            True if not equivalent to this class, including version.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if cls.VERSION_TYPE != other.VERSION_TYPE:
                super().__ne__(other)
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        elif cls.VERSION is not None:
            try:
                other_version = cls.VERSION.cast(other)
            except TypeError:
                return super().__ne__(other)
        else:
            return super().__ne__(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION != other_version
        else:
            raise TypeError(f"'!=' not supported between instances of '{str(cls)}' and '{str(other)}'")

    def __lt__(cls, other: Any) -> bool:
        """Returns True if this class's version is less than the other's.

        Args:
            other: The object to compare against this class.

        Returns:
            True if this class's version is less than other.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if cls.VERSION_TYPE != other.VERSION_TYPE:
                raise TypeError(f"'<' not supported between instances of '{str(cls)}' and '{str(other)}'")
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        else:
            other_version = cls.VERSION.cast(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION < other_version
        else:
            raise TypeError(f"'<' not supported between instances of '{str(cls)}' and '{str(other)}'")

    def __gt__(cls, other: Any) -> bool:
        """Returns True if this class's version is greater than the other's.

        Args:
            other: The object to compare against this class.

        Returns:
            True if this class's version is greater than other.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if cls.VERSION_TYPE != other.VERSION_TYPE:
                raise TypeError(f"'>' not supported between instances of '{str(cls)}' and '{str(other)}'")
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        else:
            other_version = cls.VERSION.cast(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION > other_version
        else:
            raise TypeError(f"'>' not supported between instances of '{str(cls)}' and '{str(other)}'")

    def __le__(cls, other: Any) -> bool:
        """Returns True if this class's version is <= the other's.

        Args:
            other: The object to compare against this class.

        Returns:
            True if this class's version is less than or equal to other.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if cls.VERSION_TYPE != other.VERSION_TYPE:
                raise TypeError(f"'<=' not supported between instances of '{str(cls)}' and '{str(other)}'")
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        else:
            other_version = cls.VERSION.cast(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION <= other_version
        else:
            raise TypeError(f"'<=' not supported between instances of '{str(cls)}' and '{str(other)}'")

    def __ge__(cls, other: Any) -> bool:
        """Returns True if this class's version is >= the other's.

        Args:
            other: The object to compare against this class.

        Returns:
            True if this class's version is greater than or equal to other.

        Raises:
            TypeError: If other is not a comparable type.
        """
        if isinstance(other, cls.__class__):
            if cls.VERSION_TYPE != other.VERSION_TYPE:
                raise TypeError(f"'>=' not supported between instances of '{str(cls)}' and '{str(other)}'")
            other_version = other.VERSION
        elif isinstance(other, Version):
            other_version = other
        else:
            other_version = cls.VERSION.cast(other)

        if isinstance(other_version, type(cls.VERSION)):
            return cls.VERSION >= other_version
        else:
            raise TypeError(f"'>=' not supported between instances of '{str(cls)}' and '{str(other)}'")
