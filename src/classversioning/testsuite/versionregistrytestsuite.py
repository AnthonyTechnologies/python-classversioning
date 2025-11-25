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
# Standard Library #
from typing import Any, ClassVar, Iterable, Type

# Third-Party #
import pytest
from baseobjects.testsuite.classregistration import BaseClassRegistryTestSuite
from baseobjects.versioning import Version, TriNumberVersion

# Local Imports #
from ..versionregistry import VersionRegistry
from ..versionedclass import VersionedClass


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
    register_cases: ClassVar[Iterable[tuple[str | None, ...]]] = (None, "other")
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

    get_cases: ClassVar[Iterable[tuple[Any, Type[VersionedClass], bool, str, Any]]] = ()
    @pytest.mark.parametrize("key,expected,exact,group,default", get_cases)  # type: ignore[misc]
    def test_get_class(
        self,
        key: Any,
        expected: Type[VersionedClass] | None,
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

    latest_cases: ClassVar[Iterable[tuple[str, Type[VersionedClass]]]] = ()
    @pytest.mark.parametrize("group,expected", latest_cases)  # type: ignore[misc]
    def test_get_latest_version(self, group: str, expected: Type[VersionedClass]) -> None:
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
