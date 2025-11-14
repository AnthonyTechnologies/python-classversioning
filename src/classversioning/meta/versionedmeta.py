"""versionedmeta.py
A Meta Class that can compare the specified version of the classes.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


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
    """A Meta Class that can compare the specified version of the classes.

    Class Attributes:
        _VERSION_TYPE: The type of version this object will be.
        VERSION: The version of this class as a string.
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
        """Expands on equals comparison to include comparing the version.

        Args:
            other: The object to compare to this class.

        Returns:
            True if the other object is equivalent to this class, including version.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
        """Expands on not equals comparison to include comparing the version.

        Args:
            other: The object to compare to this class.

        Returns:
            True if the other object is not equivalent to this class, including version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
        """Creates the less than comparison which compares the version of this class.

        Args:
            other: The object to compare to this class.

        Returns:
            True if this object is less than to the other classes' version.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
        """Creates the greater than comparison which compares the version of this class.

        Args:
            other: The object to compare to this class.

        Returns:
            True if this object is greater than to the other classes' version.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
        """Creates the less than or equal to comparison which compares the version of this class.

        Args:
            other: The object to compare to this class.

        Returns:
            True if this object is less than or equal to the other classes' version.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
        """Creates the greater than or equal to comparison which compares the version of this class.

        Args:
            other: The object to compare to this class.

        Returns:
            True if this object is greater than or equal to the other classes' version.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
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
