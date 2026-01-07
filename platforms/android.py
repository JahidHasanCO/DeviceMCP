"""Android platform implementation (via Termux)."""
import platform
import psutil
import subprocess
from typing import List, Optional
from core.base import DeviceInfoProvider
from core.models import DeviceInfo, BatteryInfo, StorageInfo, MemoryInfo


class AndroidDeviceProvider(DeviceInfoProvider):
    """Device information provider for Android (via Termux)."""

    def _run_termux_command(self, command: str) -> Optional[str]:
        """Run a termux-api command and return output."""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def get_device_info(self) -> DeviceInfo:
        """Get Android device information."""
        # Try to get Android version via getprop
        android_version = "Unknown"
        try:
            result = subprocess.run(
                ["getprop", "ro.build.version.release"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                android_version = result.stdout.strip()
        except:
            pass

        return DeviceInfo(
            os_name="Android",
            os_version=android_version,
            hostname=platform.node(),
            architecture=platform.machine(),
            processor=platform.processor() or "ARM",
            platform="android"
        )

    def get_battery_level(self) -> BatteryInfo:
        """Get Android battery information using termux-battery-status."""
        # Try to use termux-battery-status if available
        battery_json = self._run_termux_command("termux-battery-status")

        if battery_json:
            try:
                import json
                battery_data = json.loads(battery_json)
                return BatteryInfo(
                    percentage=battery_data.get("percentage"),
                    is_charging=battery_data.get("status") == "CHARGING",
                    is_plugged=battery_data.get("plugged") != "UNPLUGGED",
                    time_remaining=None,
                    has_battery=True
                )
            except (json.JSONDecodeError, KeyError):
                pass

        # Fallback to psutil
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
        """Get Android storage information."""
        storage_list = []

        # Get all disk partitions
        partitions = psutil.disk_partitions(all=False)

        for partition in partitions:
            # Focus on main storage partitions
            if partition.fstype in ['tmpfs', 'devtmpfs', 'sysfs', 'proc']:
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
        """Get Android memory information."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return MemoryInfo(
            total_bytes=mem.total,
            available_bytes=mem.available,
            used_bytes=mem.used,
            usage_percent=mem.percent,
            swap_total_bytes=swap.total if swap.total > 0 else None,
            swap_used_bytes=swap.used if swap.total > 0 else None
        )