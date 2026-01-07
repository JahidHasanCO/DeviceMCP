"""Platform detection and provider factory."""
import platform
import sys
from typing import Optional
from core.base import DeviceInfoProvider


def detect_platform() -> str:
    """
    Detect the current platform.

    Returns:
        str: Platform identifier ('windows', 'macOS', 'linux', 'android')
    """
    system = platform.system().lower()

    # Check for Android (usually running in Termux)
    if system == 'linux':
        try:
            with open('/system/build.prop', 'r') as f:
                return 'android'
        except (FileNotFoundError, PermissionError):
            pass

        # Additional Android check
        if 'ANDROID_ROOT' in sys.prefix or 'com.termux' in sys.prefix:
            return 'android'

    # Map platform names
    if system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    else:
        # Default to linux for unknown Unix-like systems
        return 'linux'


def get_device_provider(platform_name: Optional[str] = None) -> DeviceInfoProvider:
    """
    Get the appropriate device provider for the platform.

    Args:
        platform_name: Optional platform name. Auto-detects if None.

    Returns:
        DeviceInfoProvider: Platform-specific device provider

    Raises:
        ValueError: If platform is not supported
    """
    if platform_name is None:
        platform_name = detect_platform()

    platform_name = platform_name.lower()

    if platform_name == 'windows':
        from platforms.windows import WindowsDeviceProvider
        return WindowsDeviceProvider()
    elif platform_name == 'macos':
        from platforms.macos import MacOSDeviceProvider
        return MacOSDeviceProvider()
    elif platform_name == 'linux':
        from platforms.linux import LinuxDeviceProvider
        return LinuxDeviceProvider()
    elif platform_name == 'android':
        from platforms.android import AndroidDeviceProvider
        return AndroidDeviceProvider()
    else:
        raise ValueError(f"Unsupported platform: {platform_name}")