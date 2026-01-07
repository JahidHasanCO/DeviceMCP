"""Data models for device information."""
from typing import Optional, List
from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """Device information model."""

    os_name: str = Field(..., description="Operating system name")
    os_version: str = Field(..., description="Operating system version")
    hostname: str = Field(..., description="Device hostname")
    architecture: str = Field(..., description="System architecture (x86_64, ARM64, etc.)")
    processor: str = Field(..., description="Processor/CPU name")
    platform: str = Field(..., description="Platform identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "os_name": "Windows",
                "os_version": "11",
                "hostname": "MY-LAPTOP",
                "architecture": "x86_64",
                "processor": "Intel Core i7-9750H",
                "platform": "windows"
            }
        }


class BatteryInfo(BaseModel):
    """Battery information model."""

    percentage: Optional[float] = Field(None, description="Battery percentage (0-100)")
    is_charging: Optional[bool] = Field(None, description="Whether battery is charging")
    is_plugged: Optional[bool] = Field(None, description="Whether device is plugged in")
    time_remaining: Optional[int] = Field(None, description="Time remaining in seconds")
    has_battery: bool = Field(True, description="Whether device has a battery")

    class Config:
        json_schema_extra = {
            "example": {
                "percentage": 85.5,
                "is_charging": True,
                "is_plugged": True,
                "time_remaining": 3600,
                "has_battery": True
            }
        }


class StorageInfo(BaseModel):
    """Storage information model."""

    total_bytes: int = Field(..., description="Total storage in bytes")
    used_bytes: int = Field(..., description="Used storage in bytes")
    free_bytes: int = Field(..., description="Free storage in bytes")
    usage_percent: float = Field(..., description="Storage usage percentage")
    mount_point: str = Field(..., description="Mount point or drive letter")

    class Config:
        json_schema_extra = {
            "example": {
                "total_bytes": 512000000000,
                "used_bytes": 256000000000,
                "free_bytes": 256000000000,
                "usage_percent": 50.0,
                "mount_point": "C:\\"
            }
        }


class MemoryInfo(BaseModel):
    """Memory (RAM) information model."""

    total_bytes: int = Field(..., description="Total RAM in bytes")
    available_bytes: int = Field(..., description="Available RAM in bytes")
    used_bytes: int = Field(..., description="Used RAM in bytes")
    usage_percent: float = Field(..., description="RAM usage percentage")
    swap_total_bytes: Optional[int] = Field(None, description="Total swap memory in bytes")
    swap_used_bytes: Optional[int] = Field(None, description="Used swap memory in bytes")

    class Config:
        json_schema_extra = {
            "example": {
                "total_bytes": 16000000000,
                "available_bytes": 8000000000,
                "used_bytes": 8000000000,
                "usage_percent": 50.0,
                "swap_total_bytes": 4000000000,
                "swap_used_bytes": 1000000000
            }
        }