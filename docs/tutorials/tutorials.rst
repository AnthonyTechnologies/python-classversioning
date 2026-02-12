Tutorials and Examples
======================

.. contents:: Contents
   :local:
   :backlinks: none

This project includes additional tutorials and examples in the repository to help you learn by doing.

Jupyter Tutorials
-----------------

The following Jupyter notebooks are available in the ``tutorials/`` directory of the repository:

* **Versioned Class Tutorial**: ``tutorials/versionedclass_tutorial.ipynb`` - A guide on creating and using versioned classes.
* **Versioned File Management Tutorial**: ``tutorials/versioned_file_management_tutorial.ipynb`` - Applying versioning to file management systems.

To run the notebooks locally, install the optional dependencies and launch Jupyter:

.. code-block:: bash

   pip install -e .[jupyter]
   jupyter notebook tutorials/

Code Examples
-------------

The ``examples/`` directory contains Python scripts demonstrating key features:

* ``versionedclass_example.py``: Basic usage of ``VersionedClass``.
* ``versionregistry_example.py``: How to use the ``VersionRegistry``.
* ``file_manager_example.py``: An example of building a file manager with versioned classes.
