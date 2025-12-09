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
from abc import ABCMeta
from typing import Any

# Third-Party Packages #
from baseobjects import BaseMeta  # type: ignore
from baseobjects.versioning import Version  # type: ignore


# Definitions #
# Classes #
class VersionedMeta(BaseMeta, ABCMeta):  # type: ignore
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
    def __hash__(cls) -> int:
        """Overrides hash to make the class hashable.

        Returns:
            The system ID of the class.
        """
        return id(cls)

    # Comparison
    def __eq__(cls, other: Any) -> bool:
        """Returns True if the classes are equal considering their versions.

        Args:
            other: The object to compare against this class.

        Returns:
            True if equivalent to this class, including version.
        """
        if isinstance(other, cls.__class__):
            if id(cls) == id(other):
                return True
            elif cls.VERSION is None:
                return False
            other = other.VERSION

        return bool(cls.VERSION == other)

    def __ne__(cls, other: Any) -> bool:
        """Returns True if the classes are not equal considering their versions.

        Args:
            other: The object to compare against this class.

        Returns:
            True if not equivalent to this class, including version.
        """
        if isinstance(other, cls.__class__):
            if id(cls) == id(other):
                return False
            elif cls.VERSION is None:
                return True
            other = other.VERSION

        return bool(cls.VERSION != other)

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
            if cls.VERSION is None:
                msg = f"'<' not supported between instances of '{cls!s}' and '{other!s}' (version is None)"
                raise TypeError(msg)
            if id(cls) == id(other):
                return False
            other = other.VERSION

        try:
            return bool(cls.VERSION < other)
        except TypeError as error:
            msg = f"'<' not supported between instances of '{cls!s}' and '{other!s}'"
            raise TypeError(msg) from error

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
            if cls.VERSION is None:
                msg = f"'>' not supported between instances of '{cls!s}' and '{other!s}' (version is None)"
                raise TypeError(msg)
            if id(cls) == id(other):
                return False
            other = other.VERSION

        try:
            return bool(cls.VERSION > other)
        except TypeError as error:
            msg = f"'>' not supported between instances of '{cls!s}' and '{other!s}'"
            raise TypeError(msg) from error

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
            if cls.VERSION is None:
                msg = f"'<=' not supported between instances of '{cls!s}' and '{other!s}' (version is None)"
                raise TypeError(msg)
            if id(cls) == id(other):
                return True
            other = other.VERSION

        try:
            return bool(cls.VERSION <= other)
        except TypeError as error:
            msg = f"'<=' not supported between instances of '{cls!s}' and '{other!s}'"
            raise TypeError(msg) from error

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
            if cls.VERSION is None:
                msg = f"'>=' not supported between instances of '{cls!s}' and '{other!s}' (version is None)"
                raise TypeError(msg)
            if id(cls) == id(other):
                return True
            other = other.VERSION

        try:
            return bool(cls.VERSION >= other)
        except TypeError as error:
            msg = f"'>=' not supported between instances of '{cls!s}' and '{other!s}'"
            raise TypeError(msg) from error
