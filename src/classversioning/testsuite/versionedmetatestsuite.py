"""versionedmetatestsuite.py
Reusable pytest test suite for VersionedMeta.
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
import operator
from typing import Any, ClassVar
from collections.abc import Callable
from unittest.mock import MagicMock, patch

# Third-Party Packages #
import pytest
from baseobjects.testsuite import BaseTestSuite
from baseobjects.versioning import TriNumberVersion, Version  # type: ignore

# Local Packages #
from ..meta import VersionedMeta


# Definitions #
# Classes #
class VersionedMetaTestSuite(BaseTestSuite):  # type: ignore[misc]
    """Reusable test suite for VersionedMeta."""

    TestMeta: ClassVar[type[VersionedMeta]]
    version_type: ClassVar[type[Version]] = TriNumberVersion
    first_version: Version = TriNumberVersion(1, 0, 0)
    second_version: Version = TriNumberVersion(2, 0, 0)

    # Fixtures #
    @pytest.fixture
    def versioned_classes(self) -> tuple[type, dict[Version | None, type]]:
        """Creates a set of versioned classes for testing.

        Returns:
            A tuple containing the head class and a dictionary mapping versions to their corresponding classes.
        """
        v_1 = self.first_version
        v_2 = self.second_version

        class Head(metaclass=self.TestMeta):
            VERSION_TYPE = self.version_type
            VERSION: Version | None = None

        class V1(Head):
            VERSION = v_1

        class V2(Head):
            VERSION = v_2

        class NoVerA(Head):
            VERSION = None

        class NoVerB(Head):
            VERSION = None

        return Head, {v_1: V1, v_2: V2, "NoVerA": NoVerA, "NoVerB": NoVerB}

    # Helper Methods #
    def _test_operator(
        self,
        operator_func: Callable[..., Any],
        versioned_classes: tuple[type, dict[Any, Any]],
        cls_key: Any,
        other: Any,
        expected: Any,
    ) -> None:
        """Helper method to test comparison operators.

        Args:
            operator_func: The operator function to test.
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        # Get Objects to Compare
        _, versions = versioned_classes
        cls = versions[cls_key]
        other_obj = versions[other[1]] if isinstance(other, tuple) and len(other) > 0 and other[0] == "cls" else other

        # Execute Operation
        if expected is TypeError:
            with pytest.raises(TypeError):
                operator_func(cls, other_obj)
        else:
            assert operator_func(cls, other_obj) is expected

    # Tests #
    def test_hash(self, versioned_classes: tuple[type, dict[Any, Any]]) -> None:
        """Tests that versioned classes are hashable.

        Verifies that a versioned class can be hashed, using its registry key.
        """
        _, versions = versioned_classes
        v1 = versions[self.first_version]
        assert hash(v1) == id(v1)

    def test_object_id(self, versioned_classes: tuple[type, dict[Any, Any]]) -> None:
        """Tests fallback to object identity when version comparison fails.

        Verifies that if version casting raises a TypeError, the comparison falls back to checking object identity.
        """
        head, _ = versioned_classes

        with patch("builtins.id") as mock_id:
            def side_effect(obj: Any) -> Any:
                if obj is head:
                    return 123
                if obj is object:
                    return 123
                return 456 + (hash(obj) % 1000)
            mock_id.side_effect = side_effect

            # Trigger __eq__
            # Head == Head
            # Should return True via id check
            assert (head == head) is True

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (first_version, ("cls", first_version), True),
        (first_version, ("cls", second_version), False),
        (first_version, first_version, True),
        (first_version, second_version, False),
        (first_version, "1.0.0", True),
        (first_version, "2.0.0", False),
        (first_version, object(), False),
        (first_version, ("cls", "NoVerA"), False),
        ("NoVerA", ("cls", "NoVerA"), True),
        ("NoVerA", ("cls", "NoVerB"), False),
        ("NoVerA", ("cls", first_version), False),
        ("NoVerA", first_version, False),
        ("NoVerA", "1.0.0", False),
        ("NoVerA", object(), False),
    ])
    def test_eq(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the equality operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.eq, versioned_classes, cls_key, other, expected)

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (first_version, ("cls", second_version), True),
        (first_version, ("cls", first_version), False),
        (first_version, second_version, True),
        (first_version, first_version, False),
        (first_version, "2.0.0", True),
        (first_version, "1.0.0", False),
        (first_version, object(), True),
        (first_version, ("cls", "NoVerA"), True),
        ("NoVerA", ("cls", "NoVerA"), False),
        ("NoVerA", ("cls", "NoVerB"), True),
        ("NoVerA", ("cls", first_version), True),
        ("NoVerA", first_version, True),
        ("NoVerA", "1.0.0", True),
        ("NoVerA", object(), True),
    ])
    def test_ne(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the inequality operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.ne, versioned_classes, cls_key, other, expected)

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (first_version, ("cls", second_version), True),
        (first_version, ("cls", first_version), False),
        (second_version, ("cls", first_version), False),
        (first_version, second_version, True),
        (first_version, "2.0.0", True),
        (second_version, "1.0.0", False),
        (first_version, object(), TypeError),
        (first_version, ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerB"), TypeError),
        ("NoVerA", ("cls", first_version), TypeError),
        ("NoVerA", first_version, TypeError),
        ("NoVerA", "1.0.0", TypeError),
        ("NoVerA", object(), TypeError),
    ])
    def test_lt(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the less than operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.lt, versioned_classes, cls_key, other, expected)

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (second_version, ("cls", first_version), True),
        (first_version, ("cls", second_version), False),
        (first_version, ("cls", first_version), False),
        (second_version, first_version, True),
        (second_version, "1.0.0", True),
        (first_version, "2.0.0", False),
        (first_version, object(), TypeError),
        (first_version, ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerB"), TypeError),
        ("NoVerA", ("cls", first_version), TypeError),
        ("NoVerA", first_version, TypeError),
        ("NoVerA", "1.0.0", TypeError),
        ("NoVerA", object(), TypeError),
    ])
    def test_gt(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the greater than operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.gt, versioned_classes, cls_key, other, expected)

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (first_version, ("cls", second_version), True),
        (first_version, ("cls", first_version), True),
        (second_version, ("cls", first_version), False),
        (first_version, second_version, True),
        (first_version, "2.0.0", True),
        (second_version, "1.0.0", False),
        (first_version, object(), TypeError),
        (first_version, ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerB"), TypeError),
        ("NoVerA", ("cls", first_version), TypeError),
        ("NoVerA", first_version, TypeError),
        ("NoVerA", "1.0.0", TypeError),
        ("NoVerA", object(), TypeError),
    ])
    def test_le(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the less than or equal operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.le, versioned_classes, cls_key, other, expected)

    @pytest.mark.parametrize(("cls_key", "other", "expected"), [
        (second_version, ("cls", first_version), True),
        (first_version, ("cls", first_version), True),
        (first_version, ("cls", second_version), False),
        (second_version, first_version, True),
        (second_version, "1.0.0", True),
        (first_version, "2.0.0", False),
        (first_version, object(), TypeError),
        (first_version, ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerA"), TypeError),
        ("NoVerA", ("cls", "NoVerB"), TypeError),
        ("NoVerA", ("cls", first_version), TypeError),
        ("NoVerA", first_version, TypeError),
        ("NoVerA", "1.0.0", TypeError),
        ("NoVerA", object(), TypeError),
    ])
    def test_ge(self, versioned_classes: tuple[type, dict[Any, Any]], cls_key: Any, other: Any, expected: Any) -> None:
        """Tests the greater than or equal operator.

        Verifies that the class compares correctly with other classes, versions, and values.

        Args:
            versioned_classes: The versioned classes fixture.
            cls_key: The key of the class to test.
            other: The other object to compare against.
            expected: The expected result or exception.
        """
        self._test_operator(operator.ge, versioned_classes, cls_key, other, expected)
