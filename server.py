"""DeviceMCP - Cross-platform device information MCP server."""
from typing import List, Dict, Any

from fastmcp import FastMCP

from utils.formatters import format_bytes, format_time
from utils.platform_detector import get_device_provider, detect_platform

# Initialize FastMCP server
mcp = FastMCP("DeviceMCP")

# Get the appropriate device provider for the current platform
device_provider = get_device_provider()


@mcp.tool()
def get_device_info() -> Dict[str, Any]:
    """
    Get comprehensive device information including OS, hostname, architecture, and processor.

    Returns a dictionary containing:
    - os_name: Operating system name
    - os_version: Operating system version
    - hostname: Device hostname
    - architecture: System architecture (x86_64, ARM64, etc.)
    - processor: Processor/CPU name
    - platform: Platform identifier (windows, macOS, linux, android)
    """
    info = device_provider.get_device_info()
    return info.model_dump()


@mcp.tool()
def get_battery_level() -> Dict[str, Any]:
    """
    Get battery information including charge percentage and power status.

    Returns a dictionary containing:
    - percentage: Battery percentage (0-100) or None if no battery
    - is_charging: Whether battery is currently charging
    - is_plugged: Whether device is plugged into power
    - time_remaining: Estimated time remaining in seconds (None if unknown)
    - time_remaining_formatted: Human-readable time remaining
    - has_battery: Whether device has a battery
    """
    battery = device_provider.get_battery_level()
    result = battery.model_dump()

    # Add formatted time remaining
    if battery.time_remaining is not None:
        result['time_remaining_formatted'] = format_time(battery.time_remaining)
    else:
        result['time_remaining_formatted'] = "Unknown"

    return result


@mcp.tool()
def get_storage_info() -> List[Dict[str, Any]]:
    """
    Get storage information for all drives/partitions.

    Returns a list of dictionaries, each containing:
    - total_bytes: Total storage capacity in bytes
    - used_bytes: Used storage in bytes
    - free_bytes: Free storage in bytes
    - usage_percent: Storage usage percentage
    - mount_point: Mount point or drive letter
    - total_formatted: Human-readable total size
    - used_formatted: Human-readable used size
    - free_formatted: Human-readable free size
    """
    storage_list = device_provider.get_storage_info()

    result = []
    for storage in storage_list:
        storage_dict = storage.model_dump()
        storage_dict['total_formatted'] = format_bytes(storage.total_bytes)
        storage_dict['used_formatted'] = format_bytes(storage.used_bytes)
        storage_dict['free_formatted'] = format_bytes(storage.free_bytes)
        result.append(storage_dict)

    return result


@mcp.tool()
def get_memory_info() -> Dict[str, Any]:
    """
    Get memory (RAM) information including usage and swap details.

    Returns a dictionary containing:
    - total_bytes: Total RAM in bytes
    - available_bytes: Available RAM in bytes
    - used_bytes: Used RAM in bytes
    - usage_percent: RAM usage percentage
    - swap_total_bytes: Total swap memory in bytes (if available)
    - swap_used_bytes: Used swap memory in bytes (if available)
    - total_formatted: Human-readable total RAM
    - available_formatted: Human-readable available RAM
    - used_formatted: Human-readable used RAM
    """
    memory = device_provider.get_memory_info()
    result = memory.model_dump()

    # Add formatted values
    result['total_formatted'] = format_bytes(memory.total_bytes)
    result['available_formatted'] = format_bytes(memory.available_bytes)
    result['used_formatted'] = format_bytes(memory.used_bytes)

    if memory.swap_total_bytes is not None:
        result['swap_total_formatted'] = format_bytes(memory.swap_total_bytes)
        result['swap_used_formatted'] = format_bytes(memory.swap_used_bytes)

    return result


@mcp.tool()
def get_system_summary() -> Dict[str, Any]:
    """
    Get a comprehensive summary of all device information in one call.

    Returns a dictionary containing:
    - device: Device information
    - battery: Battery information
    - storage: Storage information for all drives
    - memory: Memory information
    - platform: Detected platform
    """
    return {
        "platform": detect_platform(),
        "device": get_device_info(),
        "battery": get_battery_level(),
        "storage": get_storage_info(),
        "memory": get_memory_info()
    }


if __name__ == "__main__":
    # Run the server with stdio transport by default
    mcp.run()