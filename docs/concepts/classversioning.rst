Class Versioning
================

The :class:`~classversioning.versionedclass.VersionedClass` framework provides a powerful mechanism for managing versioned class hierarchies. It relies on a combination of metaclass magic for comparisons and a registry pattern for dynamic dispatching.

This section details the internal mechanics of how these components interact.

Metaclass Comparisons
---------------------

The foundation of the versioning system is the :class:`~classversioning.meta.versionedmeta.VersionedMeta` metaclass. Its primary purpose is to make class objects themselves comparable based on their assigned version.

Comparison Logic
^^^^^^^^^^^^^^^^

Classes that use :class:`~classversioning.meta.versionedmeta.VersionedMeta` (or inherit from :class:`~classversioning.versionedclass.VersionedClass`) proxy standard comparison operators (``<``, ``<=``, ``==``, ``!=``, ``>=``, ``>``) to their ``VERSION`` attribute.

This allows for intuitive checks directly on the class types:

.. code-block:: python

    if MyClassV1 < MyClassV2:
        print("V1 is older than V2")

The comparison logic follows these rules:

1.  **Identity Check**: If the two operands are the exact same class object (same memory address), they are equal.
2.  **Class-to-Class**: If comparing against another class instance of ``VersionedMeta``, the comparison is delegated to their respective ``VERSION`` attributes.
    *   If either class has ``VERSION`` set to ``None``, comparisons requiring ordering (like ``<``) will raise a ``TypeError``, while equality checks handle it gracefully.
3.  **Class-to-Value**: If comparing against a non-class object (e.g., a ``str`` or ``Version`` object), the class's ``VERSION`` attribute is compared directly against that value.

Dispatching Mechanics
---------------------

:class:`~classversioning.versionedclass.VersionedClass` builds upon the metaclass capabilities to provide a full dispatching system. This allows the correct class subclass to be selected dynamically at runtime based on data or other inputs.

Registration Lifecycle
^^^^^^^^^^^^^^^^^^^^^^

The registration system uses the standard Python ``__init_subclass__`` hook.

1.  **Definition**: A user defines a subclass of ``VersionedClass`` (or a subclass of an existing versioned hierarchy).
2.  **Hook Execution**: ``VersionedClass.__init_subclass__`` is called automatically by Python.
3.  **Casting**: The subclass's ``VERSION`` attribute is cast to the hierarchy's ``VERSION_TYPE`` if necessary (and if ``VERSION_TYPE`` is defined).
4.  **Registration**: The subclass is added to the ``class_registry`` (an instance of :class:`~classversioning.versionregistry.VersionRegistry`) of the base class. It is registered under a specific "group" (defaulting to ``"default"``).

Dispatch Flow
^^^^^^^^^^^^^

The dispatching workflow typically follows this pattern:

1.  **Input Analysis**: The user calls :meth:`~classversioning.versionedclass.VersionedClass.get_class_information` (or a similar entry point) with an object (e.g., a data dictionary or file path).
2.  **Version Extraction**: The abstract method :meth:`~classversioning.versionedclass.VersionedClass.get_version_from_object` is invoked. This method must be implemented by the user's base class to inspect the object and return a version identifier.
3.  **Registry Lookup**: The extracted version is passed to :meth:`~classversioning.versionedclass.VersionedClass.get_version_class`.
4.  **Resolution**: The registry searches for a matching class.
    *   If ``exact=True``, it looks for a class with that exact version.
    *   If ``exact=False`` (default), it returns the latest version that is less than or equal to the requested version.

Head Class Dispatching
^^^^^^^^^^^^^^^^^^^^^^

The most powerful feature of ``VersionedClass`` is the ability to dispatch to the correct subclass directly from the head class constructor. This is achieved through the ``__new__`` method inherited from ``DispatchableClass``.

When you instantiate the head class (e.g., ``MyHeadClass(data)``), the following sequence occurs:

1.  **Interception**: The ``__new__`` method of the head class intercepts the creation request.
2.  **Information Gathering**: It calls :meth:`~classversioning.versionedclass.VersionedClass.get_class_information` with the arguments passed to the constructor.
    *   By default, ``VersionedClass`` expects the object containing version info to be the first positional argument.
    *   You can customize which argument is inspected by setting ``_dispatch_kwarg`` in your class definition.
3.  **Version Determination**: :meth:`~classversioning.versionedclass.VersionedClass.get_class_information` calls the user-implemented :meth:`~classversioning.versionedclass.VersionedClass.get_version_from_object` to extract the version.
4.  **Class Resolution**: The extracted version is returned as a tuple and passed to :meth:`~classversioning.versionedclass.VersionedClass.get_registered_class`.
5.  **Instantiation**: The specific subclass returned by the registry is instantiated with the original arguments and returned to the caller.

This pattern allows the head class to act as a factory, abstracting away the version resolution logic from the client code.

.. code-block:: python

    # Usage
    # Even though we call HeadClass, we get an instance of SubClassV1
    instance = HeadClass(data_payload)
    print(type(instance))  # <class 'SubClassV1'>

VersionedInitMeta
-----------------

For advanced use cases, :class:`~classversioning.meta.versionedinitmeta.VersionedInitMeta` combines the features of ``VersionedMeta`` with initialization hooks.

It mixes in :class:`baseobjects.metaclasses.InitMeta`, allowing classes to define `__init__` behavior at the metaclass level while maintaining the version comparison capabilities. This is useful when the class definitions themselves require dynamic initialization logic beyond standard inheritance.
