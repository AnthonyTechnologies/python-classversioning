#!/usr/bin/env python
"""versionedclass_example.py
Example of how to create and use VersionedClass hierarchies.

This example demonstrates:
1. Creating a base "head" class for versioning
2. Implementing version extraction logic
3. Defining concrete versioned subclasses
4. Dispatching to the correct class based on data
5. Registry querying
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

# Source Packages #
from classversioning import TriNumberVersion, VersionedClass, VersionRegistry


# Definitions #
class DataProcessor(VersionedClass):
    """Head class for data processors.

    This class defines the version type and how to extract versions from data.
    """
    class_registration = True
    class_registry_type = VersionRegistry
    VERSION_TYPE = TriNumberVersion

    @classmethod
    def get_version_from_object(cls, obj: dict[str, Any]) -> str:
        """Extracts version from the input dictionary.

        Args:
            obj: The data object containing a 'version' key.

        Returns:
            The version string found in the object.
        """
        return str(obj.get("version", "0.0.0"))

    def process(self, data: dict[str, Any]) -> None:
        """Abstract process method to be implemented by subclasses."""
        raise NotImplementedError


class DataProcessorV1(DataProcessor):
    """Processor for version 1.0.0 data."""
    VERSION = TriNumberVersion(1, 0, 0)

    def process(self, data: dict[str, Any]) -> None:
        """Processes the data.

        Args:
            data: The data to process.
        """
        print(f"Processing V1 data: {data['payload']}")


class DataProcessorV2(DataProcessor):
    """Processor for version 2.0.0 data."""
    VERSION = TriNumberVersion(2, 0, 0)

    def process(self, data: dict[str, Any]) -> None:
        """Processes the data.

        Args:
            data: The data to process.
        """
        # V2 processes data differently (e.g., uppercase payload)
        print(f"Processing V2 data (enhanced): {data['payload'].upper()}")


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrates basic class definition and dispatch."""
    print(f"\nBasic Usage: Dispatching\n{'-' * 72}")

    # Data with different versions
    data_v1 = {"version": "1.0.0", "payload": "hello"}
    data_v2 = {"version": "2.0.0", "payload": "world"}

    # Dispatching
    # When instantiating the head class (DataProcessor), the framework uses
    # get_version_from_object to find the matching subclass.

    # Note: We pass 'obj' as a keyword argument because _dispatch_kwarg defaults to "obj".
    processor1 = DataProcessor(obj=data_v1)
    print(f"Processor for data_v1 is instance of: {processor1.__class__.__name__}")
    processor1.process(data_v1)

    processor2 = DataProcessor(obj=data_v2)
    print(f"Processor for data_v2 is instance of: {processor2.__class__.__name__}")
    processor2.process(data_v2)


def registry_usage_example() -> None:
    """Demonstrates querying the class registry."""
    print(f"\nRegistry Usage\n{'-' * 72}")

    # Get specific version class directly
    cls_v1 = DataProcessor.get_registered_class("1.0.0")
    print(f"Class for 1.0.0: {cls_v1.__name__}")

    # Get latest version class
    cls_latest = DataProcessor.get_latest_version_class()
    print(f"Latest class: {cls_latest.__name__}")

    # Inspect registry content
    if DataProcessor.class_registry:
        # The registry groups classes. By default, they are in the "default" group.
        # We can inspect the classes registered in this group.
        # Accessing the internal data storage for demonstration:
        registry_data = DataProcessor.class_registry.data

        if "default" in registry_data:
            classes = registry_data["default"]
            # Classes are sorted by version in the registry list
            # Note: DataProcessor itself is registered (as 0.0.0) because it enabled registration
            # and didn't specify a version (TriNumberVersion defaults to 0.0.0).
            versions = [str(cls.VERSION) for cls in classes]
            print(f"Registered versions in 'default' group: {versions}")


def edge_cases_example() -> None:
    """Demonstrates handling of unknown versions."""
    print(f"\nEdge Cases\n{'-' * 72}")

    data_unknown = {"version": "9.9.9", "payload": "future"}

    try:
        # This should fail if version is not registered and no default is set/found
        # Or it might return None/raise error depending on implementation of get_registered_class
        # By default get_registered_class might raise error if exact=True or fallback fails.
        # But let's see what happens.
        print("Attempting to create processor for version 9.9.9...")
        _ = DataProcessor(obj=data_unknown)
    except Exception as e:
        print(f"Caught expected error: {e}")


# Main #
if __name__ == "__main__":
    basic_usage_example()
    registry_usage_example()
    edge_cases_example()
