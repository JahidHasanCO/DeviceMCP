"""Abstract base classes for platform implementations."""
from abc import ABC, abstractmethod
from typing import List
from .models import DeviceInfo, BatteryInfo, StorageInfo, MemoryInfo


class DeviceInfoProvider(ABC):
    """Abstract base class for device information providers."""

    @abstractmethod
    def get_device_info(self) -> DeviceInfo:
        """
        Get comprehensive device information.

        Returns:
            DeviceInfo: Device information object
        """
        pass

    @abstractmethod
    def get_battery_level(self) -> BatteryInfo:
        """
        Get battery information.

        Returns:
            BatteryInfo: Battery information object
        """
        pass

    @abstractmethod
    def get_storage_info(self, path: str = None) -> List[StorageInfo]:
        """
        Get storage information for all drives/partitions.

        Args:
            path: Optional specific path to check (uses primary drive if None)

        Returns:
            List[StorageInfo]: List of storage information objects
        """
        pass

    @abstractmethod
    def get_memory_info(self) -> MemoryInfo:
        """
        Get memory (RAM) information.

        Returns:
            MemoryInfo: Memory information object
        """
        pass