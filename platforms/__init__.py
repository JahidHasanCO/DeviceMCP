"""Platform-specific implementations for DeviceMCP."""
from .windows import WindowsDeviceProvider
from .macos import MacOSDeviceProvider
from .linux import LinuxDeviceProvider
from .android import AndroidDeviceProvider

__all__ = [
    "WindowsDeviceProvider",
    "MacOSDeviceProvider",
    "LinuxDeviceProvider",
    "AndroidDeviceProvider"
]