"""versionregistry_test.py
Tests for VersionRegistry using the standard test suite.
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
import pytest

# Local Packages #
from classversioning import TriNumberVersion, VersionedClass, VersionRegistry
from classversioning.testsuite import VersionRegistryTestSuite


# Definitions #
# Classes #
class Head(VersionedClass):
    """Head class for testing."""
    VERSION_TYPE = TriNumberVersion
    class_registration = False  # We will manually register

class V1(Head):
    """Version 1."""
    VERSION = TriNumberVersion(1, 0, 0)

class V2(Head):
    """Version 2."""
    VERSION = TriNumberVersion(2, 0, 0)

class V3(Head):
    """Version 3."""
    VERSION = TriNumberVersion(3, 0, 0)


class TestVersionRegistry(VersionRegistryTestSuite):
    """Concrete test suite for VersionRegistry."""

    TestClass = VersionRegistry

    # Define example classes expected by the suite
    ExampleClass1 = V1
    ExampleClass2 = V2

    # Cases
    register_cases = [("default",), ("custom_group",)]

    get_cases = [
        # key, expected, exact, group, default
        (TriNumberVersion(1, 0, 0), V1, True, "default", None),
        (TriNumberVersion(2, 0, 0), V2, True, "default", None),
        (TriNumberVersion(1, 0, 0), V1, False, "default", None),
        (TriNumberVersion(2, 0, 0), V2, False, "default", None),
        (TriNumberVersion(3, 0, 0), None, True, "default", None), # Should fail
        (TriNumberVersion(3, 0, 0), V2, False, "default", None), # Should return V2 (latest <= 3)
        (TriNumberVersion(0, 1, 0), None, False, "default", None), # Should fail (no version <= 0.1.0)
    ]

    latest_cases = [
        ("default", V2),
    ]

    def create_test_registry(self, *args: Any, **kwargs: Any) -> VersionRegistry:
        """Creates a registry instance for testing."""
        # Ensure we pass the head class so validation passes
        kwargs.setdefault("head_class", Head)
        return self.TestClass(*args, **kwargs)

    @pytest.mark.parametrize("group", register_cases)
    def test_register_class(self, group: str | None, *args: Any, **kwargs: Any) -> None:
        """Tests register_class method.

        Args:
            group: The group to register the class in.
            *args: Arguments to pass to register_class.
            **kwargs: Keyword arguments to pass to register_class.
        """
        super().test_register_class(group, *args, **kwargs)

    @pytest.mark.parametrize("key,expected,exact,group,default", get_cases)
    def test_get_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        default: Any,
    ) -> None:
        """Tests get_class method.

        Args:
            key: The key to search for.
            expected: The expected class to be returned.
            exact: Whether to search for an exact match.
            group: The group to search in.
            default: The default value to return if not found.
        """
        super().test_get_class(key, expected, exact, group, default)

    @pytest.mark.parametrize("group,expected", latest_cases)
    def test_get_latest_version(self, group: str | None, expected: type[VersionedClass] | None) -> None:
        """Tests get_latest_version method.

        Args:
            group: The group to search in.
            expected: The expected class to be returned.
        """
        super().test_get_latest_version(group, expected)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
