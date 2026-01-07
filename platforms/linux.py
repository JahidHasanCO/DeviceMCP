"""Linux platform implementation."""
import platform
import psutil
from typing import List
from core.base import DeviceInfoProvider
from core.models import DeviceInfo, BatteryInfo, StorageInfo, MemoryInfo
import distro

class LinuxDeviceProvider(DeviceInfoProvider):
    """Device information provider for Linux."""

    def get_device_info(self) -> DeviceInfo:
        """Get Linux device information."""
        # Try to get more specific Linux distribution info
        try:

            os_name = f"{distro.name()} Linux"
            os_version = distro.version()
        except ImportError:
            os_name = "Linux"
            os_version = platform.release()

        return DeviceInfo(
            os_name=os_name,
            os_version=os_version,
            hostname=platform.node(),
            architecture=platform.machine(),
            processor=platform.processor() or "Unknown",
            platform="linux"
        )

    def get_battery_level(self) -> BatteryInfo:
        """Get Linux battery information."""
        battery = psutil.sensors_battery()

        if battery is None:
            return BatteryInfo(
                percentage=None,
                is_charging=None,
                is_plugged=None,
                time_remaining=None,
                has_battery=False
            )

        return BatteryInfo(
            percentage=battery.percent,
            is_charging=battery.power_plugged,
            is_plugged=battery.power_plugged,
            time_remaining=battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
            has_battery=True
        )

    def get_storage_info(self, path: str = None) -> List[StorageInfo]:
        """Get Linux storage information."""
        storage_list = []

        # Get all disk partitions
        partitions = psutil.disk_partitions(all=False)

        for partition in partitions:
            # Skip virtual/temporary filesystems
            if partition.fstype in ['tmpfs', 'devtmpfs', 'squashfs', 'overlay']:
                continue

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                storage_list.append(StorageInfo(
                    total_bytes=usage.total,
                    used_bytes=usage.used,
                    free_bytes=usage.free,
                    usage_percent=usage.percent,
                    mount_point=partition.mountpoint
                ))
            except PermissionError:
                continue

        return storage_list

    def get_memory_info(self) -> MemoryInfo:
        """Get Linux memory information."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return MemoryInfo(
            total_bytes=mem.total,
            available_bytes=mem.available,
            used_bytes=mem.used,
            usage_percent=mem.percent,
            swap_total_bytes=swap.total,
            swap_used_bytes=swap.used
        )