"""versionregistrytestsuite.py
Reusable pytest test suite for VersionRegistry.
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
from collections.abc import Iterable
from typing import Any, ClassVar
from unittest.mock import patch

# Third-Party Packages #
import pytest
from baseobjects.testsuite import BaseClassRegistryTestSuite  # type: ignore
from baseobjects.versioning import TriNumberVersion, Version  # type: ignore

# Local Packages #
from ..versionedclass import VersionedClass
from ..versionregistry import VersionRegistry


# Definitions #
# Classes
class VersionRegistryTestSuite(BaseClassRegistryTestSuite):
    """Reusable base tests for VersionRegistry.

    This test suite validates the core behaviors of a VersionRegistry implementation. It ensures the registry reports
    the correct version type for its head class, can retrieve registered classes by key with both exact and inexact
    matching, returns the latest version for a given group, and that its internal sort is stable and orders classes by
    ascending version while preserving the latest class per group.
    """

    # Attributes #
    TestClass: type[VersionRegistry] = VersionRegistry

    # Tests #
    register_cases: ClassVar[Iterable[str | None]] = (None, "other")

    @pytest.mark.parametrize("group", register_cases)
    def test_register_class(self, group: str | None, *args: Any, **kwargs: Any) -> None:
        """Tests the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            group: The group name under which to register the class.
            *args: Positional arguments to pass to use in testing the register_class method.
            **kwargs: Keyword arguments to pass to use in testing the register_class method.
        """

        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion

        class C1(Head):
            VERSION = TriNumberVersion(1, 0, 0)

        class C2(Head):
            VERSION = TriNumberVersion(2, 0, 0)

        class_registry = self.TestClass(head_class=Head)
        class_registry.register_class(C2, group=group)
        class_registry.register_class(C1, group=group)

        # Validate
        assert class_registry[group][0] is C1
        assert class_registry[group][1] is C2

    get_cases: ClassVar[Iterable[tuple[Any, type[VersionedClass] | None, bool, str, Any]]] = ()

    @pytest.mark.parametrize(("key", "expected", "exact", "group", "default"), get_cases)
    def test_get_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str,
        default: Any,
    ) -> None:
        """Tests the get_class method.

        Args:
            key: The lookup key, typically a version value or versioned class.
            expected: The VersionedClass type expected to be returned by the registry.
            exact: Whether to require an exact key match; otherwise, the best match may be returned.
            group: The registry group to query.
            default: The default value to return if a class cannot be found.

        Raises:
            ValueError: If the registry is not set.
        """
        class_registry = self.create_test_registry()
        class_registry.register_class(self.ExampleClass2, group=group)
        class_registry.register_class(self.ExampleClass1, group=group)

        if default is None:
            try:
                cls = class_registry.get_class(key, exact=exact, group=group)
            except ValueError as error:
                if expected is not None:
                    raise error
                cls = None
        else:
            cls = class_registry.get_class(key, exact=exact, group=group, default=default)
        assert cls is expected

    latest_cases: ClassVar[Iterable[tuple[str, type[VersionedClass]]]] = ()

    @pytest.mark.parametrize(("group", "expected"), latest_cases)
    def test_get_latest_version(self, group: str, expected: type[VersionedClass]) -> None:
        """Tests the get_latest_version method.

        Args:
            group: The group of versioned classes to query.
            expected: The expected latest versioned class.
        """
        class_registry = self.create_test_registry()
        class_registry.register_class(self.ExampleClass2, group=group)
        class_registry.register_class(self.ExampleClass1, group=group)
        cls = class_registry.get_latest_version(group)
        assert cls is expected

    def test_sort(self) -> None:
        """Tests the sort method.

        Verifies that:
        - Classes are ordered by ascending VERSION within a group after sorting.
        - Sorting is stable for classes with equal VERSION values (preserves registration order among equals).
        - The latest class per group remains the max VERSION after sorting.
        """

        # Define a minimal versioned hierarchy local to this test
        class Head(VersionedClass):
            """Head class that defines the version type for this hierarchy."""

            VERSION_TYPE = TriNumberVersion

        class V1(Head, group="default"):
            VERSION = TriNumberVersion(1)

        class V3(Head, group="default"):
            VERSION = TriNumberVersion(3)

        class V2_a(Head, group="default"):
            VERSION = TriNumberVersion(2)

        class V2_b(Head, group="default"):
            VERSION = TriNumberVersion(2)

        # Create a registry for this head and register classes out of order
        registry = self.TestClass(head_class=Head)

        # Register in non-sorted order, with equal-version classes in a specific order to test stability
        registry.register_class(V3)
        registry.register_class(V1)
        registry.register_class(V2_a)
        registry.register_class(V2_b)

        # Explicitly sort (should be idempotent given insort, but we validate sort method behavior)
        registry.sort("default")

        # Validate ascending order and stability between equal versions (V2_a before V2_b)
        assert registry["default"] == [V1, V2_a, V2_b, V3]

        # Latest version in the group should be V3
        assert registry.get_latest_version("default") is V3

    def test_registry_incompatible_version_type(self) -> None:
        """Tests registration of a class with an incompatible version type.

        Verifies that attempting to register a class with a version type incompatible with the registry's head class
        raises a TypeError.
        """

        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion

        registry = self.TestClass(head_class=Head)

        class ConcreteVersion(Version):
            def __init__(self, v: Any) -> None:
                self.v = v
                self.VERSION_TYPE = ConcreteVersion

            def __eq__(self, other: Any) -> bool:
                return bool(self.v == other.v)

            def __lt__(self, other: Any) -> bool:
                return bool(self.v < other.v)

            def __str__(self) -> str:
                return str(self.v)

            def __hash__(self) -> int:
                return hash(self.v)

            def __ge__(self, other: Any) -> bool:
                return bool(self.v >= other.v)

            def __gt__(self, other: Any) -> bool:
                return bool(self.v > other.v)

            def __le__(self, other: Any) -> bool:
                return bool(self.v <= other.v)

            def __ne__(self, other: Any) -> bool:
                return bool(self.v != other.v)

            def list(self) -> list[Any]:
                return [self.v]

            def tuple(self) -> tuple[Any, ...]:
                return (self.v,)

            def construct(self, *args: Any, **kwargs: Any) -> None:
                pass

            def str(self) -> str:
                return str(self.v)

        class WrongVer(VersionedClass):
            VERSION_TYPE = ConcreteVersion
            VERSION = ConcreteVersion("1")

        with pytest.raises(TypeError, match="not compatible"):
            registry.register_class(WrongVer)

    def test_missing_group_error(self) -> None:
        """Tests that accessing a non-existent group raises KeyError."""
        registry = self.TestClass()
        with pytest.raises(KeyError, match="Group 'missing' not found"):
            registry.get_class("1.0.0", group="missing")

    def test_default_return_missing_group(self) -> None:
        """Tests that default value is returned when group is missing."""
        registry = self.TestClass()
        assert registry.get_class("missing", default="def") == "def"

    def test_default_return_empty_group(self) -> None:
        """Tests that default value is returned when group exists but is empty."""
        registry = self.TestClass()
        registry.data["group"] = []
        assert registry.get_class("missing", group="group", default="def") == "def"

    def test_get_version_type_with_head_class(self) -> None:
        """Tests get_version_type returns correct type from head class."""

        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion

        registry = self.TestClass(head_class=Head)
        assert registry.get_version_type() is TriNumberVersion

    def test_get_version_type_no_head_class(self) -> None:
        """Tests get_version_type returns None when no head class is set."""
        registry = self.TestClass(head_class=None)
        assert registry.get_version_type() is None

    def test_register_class_default_group(self) -> None:
        """Tests registration of class with default group (None)."""

        class Head(VersionedClass):
            VERSION_TYPE = TriNumberVersion

        class V1(Head):
            VERSION = TriNumberVersion(1)

        registry = self.TestClass(head_class=Head)
        registry.register_class(V1, group=None)
        assert registry.get_class(TriNumberVersion(1)) is V1

    def test_registry_load_module_success(self) -> None:
        """Tests successful module loading during class retrieval.

        Verifies that the registry attempts to import the specified module if the class is not found initially, and
        returns the expected result after the module side-effect.
        """
        registry = self.TestClass()
        with patch("classversioning.versionregistry.import_module") as mock_import:

            def side_effect(name: str) -> None:
                registry.data["loaded"] = ["something"]

            mock_import.side_effect = side_effect
            res = registry.get_class("key", group="loaded", module="mod", default="found")
            assert res == "found"
            mock_import.assert_called()

    def test_registry_load_module_and_errors(self) -> None:
        """Tests module loading failures and other registry errors.

        Verifies behavior when module loading fails (ImportError), and checks logic for ValueError when exact version is
        not found or no version greater than requested is found.
        """
        registry = self.TestClass()

        with patch("classversioning.versionregistry.import_module") as mock_import:
            mock_import.return_value = None
            registry.data["g"] = []

            with pytest.raises(ValueError, match=r"Exact version .* not found"):
                registry.get_class("key", exact=True, group="g", module="mod")

            class Head(VersionedClass):
                VERSION_TYPE = TriNumberVersion

            class V2(Head):
                VERSION = TriNumberVersion(2)

            registry.data["g"] = [V2]

            with pytest.raises(ValueError, match="Version needs to be greater than"):
                registry.get_class(TriNumberVersion(1), exact=False, group="g", module="mod")

        with patch("classversioning.versionregistry.import_module", side_effect=ImportError("fail")):
            with pytest.warns(UserWarning, match="Failed to import module"):
                registry.get_class("key", group="missing", module="bad.module", default="default")
