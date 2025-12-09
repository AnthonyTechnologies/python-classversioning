"""versionedclass_test.py
Tests for VersionedClass using the standard test suite.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from classversioning import TriNumberVersion, VersionedClass, VersionRegistry
from classversioning.testsuite import VersionedClassTestSuite


# Definitions #
# Classes #
class ExampleVersioning(VersionedClass):
    """A Version Class that establishes the type of class versioning the child classes will use."""
    class_registration = True
    class_registry_type = VersionRegistry
    VERSION_TYPE = TriNumberVersion

    @classmethod
    def get_version_from_object(cls, obj: Any) -> str:
        """Determines the version from an object instance.

        Args:
            obj: The object to inspect.

        Returns:
            The version string corresponding to the object type.
        """
        if isinstance(obj, int):
            return "1.0.0"
        elif isinstance(obj, str):
            return "1.1.0"
        else:
            return "2.0.0"


class Example_1_0_0(ExampleVersioning):
    """This class is the first of Examples version 1.0.0"""
    VERSION = TriNumberVersion(1, 0, 0)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the instance."""
        self.a = 1


class Example_1_1_0(Example_1_0_0):
    """This class inherits from 1.0.0"""
    VERSION = "1.1.0"  # type: ignore[assignment]


class Example_2_0_0(ExampleVersioning):
    """Reimplements the whole class."""
    VERSION = TriNumberVersion(2, 0, 0)


# Constants #
# Define cases separately to use in decorators
GET_CASES = [
    ("1.0.0", Example_1_0_0, True, None, False, None),
    ((1, 1, 0), Example_1_1_0, True, None, False, None),
    ("2.0.0", Example_2_0_0, True, None, False, None),
]

AUTO_VERSION_CASES = [
    (100, Example_1_0_0),
    ("Random", Example_1_1_0),
    (None, Example_2_0_0),
]

LATEST_CASES = [
    (None, Example_2_0_0, True),
]


# Classes #
class TestExampleVersionedClass(VersionedClassTestSuite):
    """Concrete test suite for ExampleVersioning hierarchy."""

    TestClass = ExampleVersioning

    # Define cases attributes (for completeness, though not used by base decorator directly)
    get_cases = GET_CASES
    registered_cases = GET_CASES
    auto_version_cases = AUTO_VERSION_CASES
    latest_cases = LATEST_CASES

    @pytest.fixture
    def test_object(self) -> Example_1_0_0:
        """Fixture for generic object tests (copy/pickle)."""
        return Example_1_0_0()

    # Re-parametrize tests
    @pytest.mark.parametrize(("key", "expected", "exact", "group", "sort", "module"), GET_CASES)
    def test_get_version_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: str | None,
    ) -> None:
        """Tests get_version_class method.

        Args:
            key: The key to search for.
            expected: The expected class to be returned.
            exact: Whether to search for an exact match.
            group: The group to search in.
            sort: Whether to sort the results.
            module: The module to search in.
        """
        super().test_get_version_class(key, expected, exact, group, sort, module)

    @pytest.mark.parametrize(("key", "expected", "exact", "group", "sort", "module"), GET_CASES)
    def test_get_registered_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: str | None,
    ) -> None:
        """Tests get_registered_class method.

        Args:
            key: The key to search for.
            expected: The expected class to be returned.
            exact: Whether to search for an exact match.
            group: The group to search in.
            sort: Whether to sort the results.
            module: The module to search in.
        """
        super().test_get_registered_class(key, expected, exact, group, sort, module)

    def test_abstract_methods(self) -> None:
        """Tests that abstract methods raise NotImplementedError when not overridden.

        Verifies that calling get_version_from_object on a class that hasn't implemented it
        raises NotImplementedError.
        """
        class Head(VersionedClass):
            pass
        with pytest.raises(NotImplementedError):
            Head.get_version_from_object("obj")

    def test_registry_calls(self) -> None:
        """Tests delegation of calls to the class registry.

        Verifies that get_version_class and get_latest_version_class raise ValueError if the registry is not set, and
        correctly delegate to the registry when it is set.
        """
        # Standard Libraries #
        from unittest.mock import patch

        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion
            class_registry: ClassVar[VersionRegistry | None] = None

        with pytest.raises(ValueError, match="Class registry is not set"):
            Head.get_version_class("1.0.0")

        with pytest.raises(ValueError, match="Class registry is not set"):
            Head.get_latest_version_class()

        registry = VersionRegistry(head_class=Head)
        Head.class_registry = registry

        class V1(Head):
            VERSION = TriNumberVersion(1)
        registry.register_class(V1)

        with patch.object(registry, "sort", wraps=registry.sort) as mock_sort:
            Head.get_version_class(TriNumberVersion(1), sort=True)
            mock_sort.assert_called_once()

        with patch.object(registry, "sort", wraps=registry.sort) as mock_sort:
            Head.get_latest_version_class(sort=True)
            mock_sort.assert_called_once()

        # Test defaults (group=None)
        assert Head.get_registered_class(TriNumberVersion(1), group=None) is V1
        assert Head.get_latest_version_class(group=None) is V1

        # Test defaults branches (group="default") explicitly
        assert Head.get_registered_class(TriNumberVersion(1), group="default") is V1
        assert Head.get_latest_version_class(group="default") is V1

        # Cover the "else" block in get_latest_version_class (when sort=False)
        # Already covered by defaults test implicitly (default sort is True/False?)
        # get_latest_version_class(..., sort=True) is called.
        # get_latest_version_class(..., sort=False) default.
        # We called it with defaults above.

    def test_init_subclass_cast(self) -> None:
        """Tests automatic version casting during subclass initialization.

        Verifies that if a subclass defines VERSION as a string (or castable type), it is automatically cast to the
        correct VERSION_TYPE during class initialization.
        """
        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion
            class_registry_type = VersionRegistry
            class_registration = True

        class VString(Head):
            VERSION = "1.0.0"  # type: ignore[assignment]

        assert isinstance(VString.VERSION, TriNumberVersion)
        assert VString.VERSION == TriNumberVersion(1, 0, 0)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
