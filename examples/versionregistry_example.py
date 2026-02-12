#!/usr/bin/env python
"""versionregistry_example.py
Example usage of the VersionRegistry class.

This example demonstrates how to use VersionRegistry to:
1. Manually register versioned classes.
2. Retrieve classes by exact and approximate versions.
3. Organize classes into groups.
4. Retrieve the latest version from a registry.
"""

# Header #
__package_name__ = "classversioning"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "0.8.0"


# Imports #
# Source Packages #
from classversioning import TriNumberVersion, VersionedClass, VersionRegistry


# Definitions #
class ConfigLoader(VersionedClass):
    """Head class for configuration loaders.

    We disable automatic registration to demonstrate manual registry usage.
    """
    VERSION_TYPE = TriNumberVersion
    class_registration = False


class ConfigLoaderV1(ConfigLoader):
    """Loader for version 1.0.0 configurations (JSON only)."""
    VERSION = TriNumberVersion(1, 0, 0)


class ConfigLoaderV2(ConfigLoader):
    """Loader for version 2.0.0 configurations (YAML support)."""
    VERSION = TriNumberVersion(2, 0, 0)


class ConfigLoaderV2_1(ConfigLoader):  # noqa: N801
    """Loader for version 2.1.0 configurations (TOML support)."""
    VERSION = TriNumberVersion(2, 1, 0)


# Example Sections #
def basic_registry_usage() -> None:
    """Demonstrates manual registration and exact retrieval."""
    print(f"\nBasic Registry Usage\n{'-' * 72}")

    # 1. Create a registry
    # We pass the head_class so the registry knows the version type and can enforce compatibility.
    registry = VersionRegistry(head_class=ConfigLoader)
    print(f"Created registry: {registry}")

    # 2. Register classes
    # Since auto-registration is disabled, we add them manually.
    registry.register_class(ConfigLoaderV1)
    registry.register_class(ConfigLoaderV2)
    print("Registered ConfigLoaderV1 (1.0.0) and ConfigLoaderV2 (2.0.0).")

    # 3. Retrieve exact version
    version_to_find = TriNumberVersion(1, 0, 0)
    cls = registry.get_class(version_to_find, exact=True)
    print(f"Retrieved class for {version_to_find}: {cls.__name__}")


def approximate_matching_usage() -> None:
    """Demonstrates retrieving classes when an exact match isn't required."""
    print(f"\nApproximate Version Matching\n{'-' * 72}")

    registry = VersionRegistry(head_class=ConfigLoader)
    registry.register_class(ConfigLoaderV1)     # 1.0.0
    registry.register_class(ConfigLoaderV2)     # 2.0.0
    registry.register_class(ConfigLoaderV2_1)   # 2.1.0

    # Scenario: We have data labeled as version 2.0.5.
    # We want the closest version that is less than or equal to 2.0.5 (which is 2.0.0).
    # Note: The registry finds the version <= requested version.

    request_ver = TriNumberVersion(2, 0, 5)
    cls = registry.get_class(request_ver, exact=False)
    print(f"Requested version {request_ver} -> Found class: {cls.__name__} (Version {cls.VERSION})")

    # Scenario: Data version 2.2.0. Should map to 2.1.0.
    request_ver_2 = TriNumberVersion(2, 2, 0)
    cls_2 = registry.get_class(request_ver_2, exact=False)
    print(f"Requested version {request_ver_2} -> Found class: {cls_2.__name__} (Version {cls_2.VERSION})")

    # Scenario: Data version 0.9.0. Should fail (no version <= 0.9.0).
    try:
        registry.get_class(TriNumberVersion(0, 9, 0), exact=False)
    except ValueError as e:
        print(f"Requested version 0.9.0 -> Correctly failed: {e}")


def grouping_usage() -> None:
    """Demonstrates organizing classes into groups within the same registry."""
    print(f"\nRegistry Groups\n{'-' * 72}")

    registry = VersionRegistry(head_class=ConfigLoader)

    # Register standard loaders to "default" group (default behavior)
    registry.register_class(ConfigLoaderV1)

    # Register experimental loaders to "experimental" group
    # We can re-use the same class for demonstration, or imagine these are different classes.
    registry.register_class(ConfigLoaderV2_1, group="experimental")

    print("Registered V1 to 'default' and V2.1 to 'experimental'.")

    # Retrieve from default
    default_latest = registry.get_latest_version(group="default")
    print(f"Latest in 'default': {default_latest.__name__} ({default_latest.VERSION})")

    # Retrieve from experimental
    exp_latest = registry.get_latest_version(group="experimental")
    print(f"Latest in 'experimental': {exp_latest.__name__} ({exp_latest.VERSION})")


def latest_version_usage() -> None:
    """Demonstrates retrieving the absolute latest version."""
    print(f"\nLatest Version Retrieval\n{'-' * 72}")

    registry = VersionRegistry(head_class=ConfigLoader)
    registry.register_class(ConfigLoaderV1)
    registry.register_class(ConfigLoaderV2)
    registry.register_class(ConfigLoaderV2_1)

    latest = registry.get_latest_version()
    print(f"Absolute latest version registered: {latest.__name__} ({latest.VERSION})")


# Main #
if __name__ == "__main__":
    basic_registry_usage()
    approximate_matching_usage()
    grouping_usage()
    latest_version_usage()
