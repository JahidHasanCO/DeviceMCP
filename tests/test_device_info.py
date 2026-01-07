"""Tests for device information functionality."""
import pytest
from utils.platform_detector import get_device_provider, detect_platform
from core.models import DeviceInfo, BatteryInfo, StorageInfo, MemoryInfo


def test_platform_detection():
    """Test that platform detection returns a valid platform."""
    platform = detect_platform()
    assert platform in ['windows', 'macos', 'linux', 'android']


def test_get_device_provider():
    """Test that device provider can be instantiated."""
    provider = get_device_provider()
    assert provider is not None


def test_device_info():
    """Test getting device information."""
    provider = get_device_provider()
    info = provider.get_device_info()

    assert isinstance(info, DeviceInfo)
    assert info.os_name
    assert info.hostname
    assert info.architecture
    assert info.platform in ['windows', 'macos', 'linux', 'android']


def test_battery_info():
    """Test getting battery information."""
    provider = get_device_provider()
    battery = provider.get_battery_level()

    assert isinstance(battery, BatteryInfo)
    assert isinstance(battery.has_battery, bool)

    if battery.has_battery:
        assert battery.percentage is not None
        assert 0 <= battery.percentage <= 100
        assert isinstance(battery.is_charging, bool)
        assert isinstance(battery.is_plugged, bool)


def test_storage_info():
    """Test getting storage information."""
    provider = get_device_provider()
    storage_list = provider.get_storage_info()

    assert isinstance(storage_list, list)
    assert len(storage_list) > 0

    for storage in storage_list:
        assert isinstance(storage, StorageInfo)
        assert storage.total_bytes > 0
        assert storage.free_bytes >= 0
        assert storage.used_bytes >= 0
        assert 0 <= storage.usage_percent <= 100
        assert storage.mount_point


def test_memory_info():
    """Test getting memory information."""
    provider = get_device_provider()
    memory = provider.get_memory_info()

    assert isinstance(memory, MemoryInfo)
    assert memory.total_bytes > 0
    assert memory.available_bytes >= 0
    assert memory.used_bytes >= 0
    assert 0 <= memory.usage_percent <= 100


def test_data_model_serialization():
    """Test that data models can be serialized to dict."""
    provider = get_device_provider()

    # Test DeviceInfo serialization
    device_info = provider.get_device_info()
    device_dict = device_info.model_dump()
    assert isinstance(device_dict, dict)
    assert 'os_name' in device_dict

    # Test BatteryInfo serialization
    battery_info = provider.get_battery_level()
    battery_dict = battery_info.model_dump()
    assert isinstance(battery_dict, dict)
    assert 'has_battery' in battery_dict

    # Test MemoryInfo serialization
    memory_info = provider.get_memory_info()
    memory_dict = memory_info.model_dump()
    assert isinstance(memory_dict, dict)
    assert 'total_bytes' in memory_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])