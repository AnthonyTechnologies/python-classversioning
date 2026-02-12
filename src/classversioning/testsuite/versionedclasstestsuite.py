"""versionedclasstestsuite.py
A reusable test suite for VersionedClass hierarchies.

Subclasses must supply concrete class references and version-like values by setting the required class attributes
documented below.
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

# Third-Party Packages #
import pytest
from baseobjects.testsuite import BaseRegisteredClassTestSuite

# Local Packages #
from ..versionedclass import VersionedClass


# Definitions #
# Classes
class VersionedClassTestSuite(BaseRegisteredClassTestSuite):
    """Reusable base tests for a VersionedClass hierarchy.

    Subclass this in your test modules and set the class attributes to supply concrete classes and parameters for the
    tests. Only the datasets relevant to your hierarchy need to be provided; individual tests will be skipped if their
    required dataset is missing.

    Required attributes for specific tests:
        UnitTestClass: The version head class (a subclass of VersionedClass). Required by all tests.
        get_cases: Iterable of tuples (key, expected_cls, exact, group, sort, module)
            Used by test_get_version_class. "group" may be None to use the default.
        registered_cases: Iterable of tuples (key, expected_cls, exact, group, sort, module)
            Used by test_get_registered_class. If omitted, test mirrors get_cases with the same parameters.
        auto_version_cases: Iterable of tuples (dispatch_obj, expected_cls)
            Used by test_auto_version to validate construction-time dispatch.
        latest_cases: Iterable of tuples (group, expected_cls, sort)
            Used by test_get_latest_version_class.
    """

    # Attributes
    UnitTestClass: type[VersionedClass]

    # Optional datasets expected to be provided by subclasses
    get_cases: ClassVar[Iterable[tuple[Any, type[VersionedClass] | None, bool, str | None, bool, str | None]]] = ()
    registered_cases: ClassVar[
        Iterable[tuple[Any, type[VersionedClass] | None, bool, str | None, bool, str | None]]
    ] = ()
    auto_version_cases: ClassVar[Iterable[tuple[Any, type[VersionedClass]]]] = ()
    latest_cases: ClassVar[Iterable[tuple[str | None, type[VersionedClass], bool]]] = ()

    # Implement abstract base tests concretely by delegating to super

    def test_pickling(self, test_object: Any) -> None:
        """Tests the pickling method.

        Args:
            test_object: The object to test pickling.
        """
        super().test_pickling(test_object)

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Test the register_class method.

        Overrides BaseRegisteredClassTestSuite.test_register_class to support VersionRegistry.

        Args:
            *args: Positional arguments to pass to the register_class method.
            **kwargs: Keyword arguments to pass to the register_class method.
        """
        if self.UnitTestClass.VERSION_TYPE is None:
            pytest.skip("UnitTestClass.VERSION_TYPE is not set.")

        class NewTestSubclass(self.UnitTestClass):  # type: ignore
            class_registration = False
            VERSION = self.UnitTestClass.VERSION_TYPE((0, 0, 0))  # type: ignore

        # Register class
        NewTestSubclass.register_class(*args, **kwargs)

        # Verify class was registered
        group = kwargs.get("group", "default")
        if self.UnitTestClass.class_registry is None:
            pytest.fail("UnitTestClass.class_registry is not set.")
        assert NewTestSubclass in self.UnitTestClass.class_registry[group]

    # Tests
    @pytest.mark.parametrize(("key", "expected", "exact", "group", "sort", "module"), get_cases)
    def test_get_version_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: str | None,
    ) -> None:
        """Tests VersionedClass.get_version_class.

        Validates class resolution given a version-like key under exact/inexact modes, with optional grouping, sorting,
        and lazy module import.

        Args:
            key: The key to search for (e.g., a version or value castable to the version type).
            expected: The expected class to be returned.
            exact: If True, require an exact version match; otherwise return the closest version.
            group: The group of versioned classes to search.
            sort: If True, sort the registry before getting the class.
            module: Optional module to import if the class is not found.
        """
        cls = self.UnitTestClass.get_version_class(key, exact=exact, group=group, sort=sort, module=module)
        assert cls is expected

    @pytest.mark.parametrize(("key", "expected", "exact", "group", "sort", "module"), registered_cases)
    def test_get_registered_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: str | None,
    ) -> None:
        """Tests VersionedClass.get_registered_class wrapper.

        Mirrors get_version_class but calls the wrapper API to ensure the default group handling and delegation are
        correct.

        Args:
            key: The key to search for (e.g., a version or value castable to the version type).
            expected: The expected class to be returned.
            exact: If True, require an exact version match; otherwise return the closest version.
            group: The group of versioned classes to search.
            sort: If True, sort the registry before getting the class.
            module: Optional module to import if the class is not found.
        """
        cls = self.UnitTestClass.get_registered_class(key, exact=exact, group=group, sort=sort, module=module)
        assert cls is expected

    def test_version_dispatch(self) -> None:
        """Tests that the head class correctly dispatches to subclasses based on input.

        Validates that instantiating the head class with a dispatch object returns an instance of the correct versioned
        subclass.
        """
        for dispatch_obj, expected_cls in self.auto_version_cases:
            obj = self.UnitTestClass(dispatch_obj)
            assert type(obj) is expected_cls

    def test_get_latest_version_class(self) -> None:
        """Tests VersionedClass.get_latest_version_class.

        Validates retrieving the class with the latest version from a group.
        """
        for group, expected_cls, sort in self.latest_cases:
            cls = self.UnitTestClass.get_latest_version_class(group=group, sort=sort)
            assert cls is expected_cls
