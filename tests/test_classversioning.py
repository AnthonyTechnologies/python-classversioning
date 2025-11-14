#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""test_xltekobjects.py
Description:
"""
# Package Header #
from src.classversioning.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import pathlib

# Third-Party Packages #
import pytest

# Local Packages #
from classversioning import *


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class TestVersionedClass:
    # Define Classes with Versions
    class ExampleVersioning(VersionedClass):
        """A Version Class that establishes the type of class versioning the child classes will use."""
        _VERSION_TYPE = VersionType(name="Example", class_=TriNumberVersion)

        @classmethod
        def get_version_from_object(cls, obj):
            if isinstance(obj, int):
                return "1.0.0"
            elif isinstance(obj, str):
                return "1.1.0"
            else:
                return "2.0.0"

    class Example_1_0_0(ExampleVersioning):
        """This class is the first of Examples version 1.0.0 which implements some adding"""
        VERSION = TriNumberVersion(1, 0, 0)  # Version can be defined through version object

        def __init__(self, *args, **kwargs):
            self.a = 1
            self.b = 2

        def add(self, x):
            self.a = self.a + x

    class Example_1_1_0(Example_1_0_0):
        """This class inherits from 1.0.0 but changes how the adding is done"""
        VERSION = "1.1.0"  # Version can be defined through str as long as there is a method to derive the Version

        def add(self, x):
            self.b = self.b + x

    class Example_2_0_0(ExampleVersioning):
        """Rather than inherit from previous version, this class reimplements the whole class."""
        VERSION = (2, 0, 0)

        def __init__(self,  *args, **kwargs):
            self.a = 1
            self.c = 3

        def multiply(self, x):
            self.a = self.a * x

    class Example_2_x_0(ExampleVersioning):
        """A Version that will not be added to the registry."""
        VERSION = (2, 7, 0)
        _registration = False

        def __init__(self,  *args, **kwargs):
            self.a = None
            self.c = None

        def not_multiply(self, x):
            self.a = self.a * x

    class BadExample(VersionedClass):
        """A Version Class that establishes the type of class versioning the child classes will use."""
        _VERSION_TYPE = VersionType(name="BadExample", class_=TriNumberVersion)

    # Define Versioned Datasets
    version_types = ["1.0.0", (1, 0, 0), TriNumberVersion(1, 0, 0, ver_name="Example")]

    version_selection = [
        (100, Example_1_0_0),
        ("Random", Example_1_1_0),
        (None, Example_2_0_0),
    ]

    @pytest.mark.parametrize("version_", version_types)
    @pytest.mark.parametrize("exact", [False, True])
    @pytest.mark.parametrize("sort", [False, True])
    def test_get_version_class(self, version_, exact, sort):
        assert self.ExampleVersioning.get_version_class(version_, exact=exact, sort=sort) is self.Example_1_0_0

    @pytest.mark.parametrize("arg,expected", version_selection)
    def test_auto_version(self, arg, expected):
        assert self.ExampleVersioning(arg).__class__ is expected

    def test_auto_version_error(self):
        try:
            self.BadExample("random")
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("type_", [None, "Example"])
    @pytest.mark.parametrize("sort", [False, True])
    def test_get_latest_version_class(self, type_, sort):
        assert self.ExampleVersioning.get_latest_version_class(type_=type_, sort=sort) is self.Example_2_0_0

    versions_e = ["1.0.0", (1, 0, 0), TriNumberVersion(1, 0, 0, ver_name="Example"), Example_1_0_0]
    versions_ne = ["1.2.0", (1, 0, 0), TriNumberVersion(1, 0, 0, ver_name="Example"), Example_2_0_0]
    versions_l = ["1.2.0", (4, 0, 0), TriNumberVersion(1, 9, 0, ver_name="Example"), Example_2_0_0]
    versions_g = ["1.2.0", (0, 1, 0), TriNumberVersion(1, 3, 0, ver_name="Example"), Example_1_0_0]
    versions_le = ["1.2.0", (4, 0, 0), TriNumberVersion(1, 9, 0, ver_name="Example"), Example_1_1_0]
    versions_ge = ["1.2.0", (0, 1, 0), TriNumberVersion(1, 3, 0, ver_name="Example"), Example_2_0_0]

    @pytest.mark.parametrize("version_", versions_e)
    def test_version_comparison_equals(self, version_):
        assert self.Example_1_0_0 == version_

    @pytest.mark.parametrize("version_", versions_ne)
    def test_version_comparison_not_equals(self, version_):
        assert self.Example_1_1_0 != version_

    @pytest.mark.parametrize("version_", versions_l)
    def test_version_comparison_less_than(self, version_):
        assert self.Example_1_1_0 < version_

    @pytest.mark.parametrize("version_", versions_g)
    def test_version_comparison_greater_than(self, version_):
        assert self.Example_2_0_0 > version_

    @pytest.mark.parametrize("version_", versions_le)
    def test_version_comparison_less_than_equal(self, version_):
        assert self.Example_1_1_0 <= version_

    @pytest.mark.parametrize("version_", versions_ge)
    def test_version_comparison_greater_than_equal(self, version_):
        assert self.Example_2_0_0 >= version_


# Main #
if __name__ == '__main__':
    pytest.main(["-v", "-s"])
