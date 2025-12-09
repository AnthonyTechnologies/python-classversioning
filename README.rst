classversioning
===============================

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit|

.. |PyPI| image:: https://img.shields.io/pypi/v/classversioning.svg
   :target: https://pypi.org/project/classversioning/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/classversioning.svg
   :target: https://pypi.org/project/classversioning/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/classversioning
   :target: https://pypi.org/project/classversioning
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/classversioning
   :target: https://github.com/AnthonyTechnologies/python-classversioning/blob/main/LICENSE
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/python-classversioning/latest.svg?label=Read%20the%20Docs
   :target: https://python-classversioning.readthedocs.io/
   :alt: Read the documentation at https://python-classversioning.readthedocs.io/
.. |Tests| image:: https://github.com/AnthonyTechnologies/python-classversioning/workflows/Tests/badge.svg
   :target: https://github.com/AnthonyTechnologies/python-classversioning/actions?query=workflow%3ATests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/AnthonyTechnologies/python-classversioning/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/AnthonyTechnologies/python-classversioning
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit


Features
--------

Tools for creating versioned class hierarchies.

A VersionedClass is structured so that subclasses can optionally define a version which can be used to compare with
other subclasses and for dispatch. The framework can also be used by instances of these classes, but it is primarily
focused on versioning classes. Versioning is useful for creating classes that interface with data structures that change
frequently while maintaining support for previous versions. For example, a file format may change how data is stored,
but you might have both new and previous versions. In this case, an appropriate class addressing each version can be
chosen based on the class' version.

Example
-------

This example demonstrates how to use the head class dispatch to automatically handle different file versions.

.. code-block:: python

    import json
    from pathlib import Path
    from classversioning import TriNumberVersion, VersionedClass, VersionRegistry

    class FileManager(VersionedClass):
        """Head class that dispatches to subclasses based on file version."""
        class_registration = True
        class_registry_type = VersionRegistry
        VERSION_TYPE = TriNumberVersion

        @classmethod
        def get_version_from_object(cls, obj):
            # Extract version from file content
            with Path(obj).open("r") as f:
                ver = json.load(f).get("version", "0.0.0")
                return TriNumberVersion(*map(int, ver.split(".")))

        def __init__(self, file_path):
            self.file_path = Path(file_path)

        def process(self):
             print(f"Processing V? file: {self.file_path}")

    class FileManagerV1(FileManager):
        VERSION = TriNumberVersion(1, 0, 0)

        def process(self):
            print(f"Processing V1 file: {self.file_path}")

    class FileManagerV2(FileManager):
        VERSION = TriNumberVersion(2, 0, 0)

        def process(self):
            print(f"Processing V2 file: {self.file_path}")

    # Usage:
    # If 'data.json' contains {"version": "2.0.0"}
    manager = FileManager("data.json")

    # manager is automatically an instance of FileManagerV2
    print(type(manager))  # <class 'FileManagerV2'>
    manager.process()     # Output: Processing V2 file: data.json


Requirements
------------

* Python 3.11 or later

Installation
------------

You can install *classversioning* via pip_ from PyPI_:

.. code:: console

   $ pip install classversioning


Documentation
-------------

For comprehensive guides, see the full documentation on Read the Docs:
https://python-classversioning.readthedocs.io/

The documentation includes a user guide, API reference, tutorials, and examples to help you get productive quickly.

For project-wide conventions and contribution standards, refer to `Anthony's Python Style Guide`_.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT License, *classversioning* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

Project Organization: `Anthony's Python Style Guide`_ based on `The Google Style Guide`_ and `Hypermodern Python`_ by `Claudio Jolowicz`_.

.. _pip: https://pip.pypa.io/
.. _PyPI: https://pypi.org/
.. _file an issue: https://github.com/AnthonyTechnologies/python-classversioning/issues
.. _Anthony's Python Style Guide: https://github.com/AnthonyTechnologies/python-styleguide
.. _The Google Style Guide: https://google.github.io/styleguide/pyguide.html
.. _Hypermodern Python: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
.. _Claudio Jolowicz: https://github.com/cjolowicz
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
