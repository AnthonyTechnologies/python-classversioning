#!/usr/bin/env python
"""conftest.py
Pytest configuration hooks and helpers for the test suite.

This module defines incremental-failure behavior via custom hooks and ensures
the tests package is discoverable by pytest.
"""

# Imports #
# Third-Party Packages #
import pytest

# Definitions #
_test_failed_incremental: dict[str, dict[tuple[int, ...], str]] = {}


# Functions #
def pytest_runtest_makereport(item, call) -> None:
    """Handles reports on incremental test calls which are dependent on the success of previous test calls."""
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = tuple(item.callspec.indices.values()) if hasattr(item, "callspec") else ()
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(parametrize_index, test_name)


def pytest_runtest_setup(item) -> None:
    """Implements incremental to make test calls in classes dependent on the success of previous test calls."""
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = tuple(item.callspec.indices.values()) if hasattr(item, "callspec") else ()
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail(f"previous test failed ({test_name})")
