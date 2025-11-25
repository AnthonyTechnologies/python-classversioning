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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
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
        self.a = 1

class Example_1_1_0(Example_1_0_0):
    """This class inherits from 1.0.0"""
    VERSION = "1.1.0"

class Example_2_0_0(ExampleVersioning):
    """Reimplements the whole class."""
    VERSION = (2, 0, 0)


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
    @pytest.mark.parametrize("key,expected,exact,group,sort,module", GET_CASES)
    def test_get_version_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: Any,
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

    @pytest.mark.parametrize("key,expected,exact,group,sort,module", GET_CASES)
    def test_get_registered_class(
        self,
        key: Any,
        expected: type[VersionedClass] | None,
        exact: bool,
        group: str | None,
        sort: bool,
        module: Any,
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
