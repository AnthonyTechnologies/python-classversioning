#!/usr/bin/env python
"""file_manager_example.py
Example of how to use VersionedClass to manage versioned files.

This example demonstrates:
1. Creating a "head" class that represents a file manager.
2. Implementing logic to open a file and read its version.
3. Defining versioned subclasses that handle specific file versions.
4. Dispatching to the correct subclass based on file content.
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
import json
import tempfile
from pathlib import Path
from typing import Any

# Source Packages #
from classversioning import TriNumberVersion, VersionedClass, VersionRegistry


# Definitions #
class FileManager(VersionedClass):
    """Head class for file managers.

    This class defines how to extract the version from a file.
    """
    class_registration = True
    class_registry_type = VersionRegistry
    VERSION_TYPE = TriNumberVersion

    @classmethod
    def get_version_from_object(cls, obj: Path | str) -> TriNumberVersion | None:
        """Extracts version from the file.

        Args:
            obj: The file path.

        Returns:
            The version object found in the file, or None if not found.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path = Path(obj)
        if not path.exists():
            msg = f"File not found: {path}"
            raise FileNotFoundError(msg)

        try:
            with path.open("r") as f:
                data = json.load(f)
                version_str = str(data.get("version", "0.0.0"))
                parts = [int(p) for p in version_str.split(".")]
                return TriNumberVersion(parts[0], parts[1], parts[2])
        except Exception as e:
            print(f"Error reading version from file: {e}")
            return None

    def __init__(self, obj: Path | str, **kwargs: Any) -> None:
        """Initializes the file manager.

        Args:
            obj: The file path.
            **kwargs: Additional arguments.
        """
        self.file_path = Path(obj)

    def load_data(self) -> Any:
        """Abstract method to load data."""
        raise NotImplementedError


class FileManagerV1(FileManager):
    """File manager for version 1.0.0 files."""
    VERSION = TriNumberVersion(1, 0, 0)

    def load_data(self) -> dict[str, Any]:
        """Loads data from the file.

        Returns:
            The loaded data.
        """
        with self.file_path.open("r") as f:
            data: dict[str, Any] = json.load(f)
        print(f"V1 Manager loading data: {data}")
        return data


class FileManagerV2(FileManager):
    """File manager for version 2.0.0 files."""
    VERSION = TriNumberVersion(2, 0, 0)

    def load_data(self) -> dict[str, Any]:
        """Loads data from the file.

        Returns:
            The loaded data with V2 processing.
        """
        with self.file_path.open("r") as f:
            data: dict[str, Any] = json.load(f)
        # V2 might need some transformation
        data["processed"] = True
        print(f"V2 Manager loading data with processing: {data}")
        return data


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrates basic file version dispatching."""
    print(f"\nBasic Usage: File Version Dispatching\n{'-' * 72}")

    # Create temporary files with different versions
    with tempfile.TemporaryDirectory() as tmp_dir:
        path_v1 = Path(tmp_dir) / "data_v1.json"
        path_v2 = Path(tmp_dir) / "data_v2.json"

        with path_v1.open("w") as f:
            json.dump({"version": "1.0.0", "content": "old data"}, f)

        with path_v2.open("w") as f:
            json.dump({"version": "2.0.0", "content": "new data"}, f)

        # Dispatching
        # We pass the path to the constructor. The get_version_from_object method
        # will read the file at that path to determine the version.
        manager1 = FileManager(obj=path_v1)
        print(f"Manager for {path_v1.name} is instance of: {manager1.__class__.__name__}")
        manager1.load_data()

        manager2 = FileManager(obj=path_v2)
        print(f"Manager for {path_v2.name} is instance of: {manager2.__class__.__name__}")
        manager2.load_data()


def edge_cases_example() -> None:
    """Demonstrates handling of files with unknown versions."""
    print(f"\nEdge Cases\n{'-' * 72}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        path_future = Path(tmp_dir) / "data_future.json"
        with path_future.open("w") as f:
            json.dump({"version": "5.0.0", "content": "future data"}, f)

        print(f"Attempting to load {path_future.name} (Version 5.0.0)...")
        try:
            manager = FileManager(obj=path_future)
            print(f"-> Dispatched to: {manager.__class__.__name__} (Version {manager.VERSION})")
            print("   (Note: Default behavior is to find the latest version <= requested version)")
        except Exception as e:
            print(f"-> Caught error: {e}")

        path_old = Path(tmp_dir) / "data_old.json"
        with path_old.open("w") as f:
            json.dump({"version": "0.1.0", "content": "ancient data"}, f)

        print(f"\nAttempting to load {path_old.name} (Version 0.1.0)...")
        try:
            manager = FileManager(obj=path_old)
            print(f"-> Dispatched to: {manager.__class__.__name__} (Base Class)")
            # The base class does not implement load_data
            manager.load_data()
        except Exception as e:
            print(f"-> Caught expected error when calling load_data: {e}")


if __name__ == "__main__":
    basic_usage_example()
    edge_cases_example()
