"""Utility functions for formatting device information."""


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable format.

    Args:
        bytes_value: Size in bytes

    Returns:
        str: Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_time(seconds: int) -> str:
    """
    Format seconds to human-readable time.

    Args:
        seconds: Time in seconds

    Returns:
        str: Formatted string (e.g., "2h 30m")
    """
    if seconds < 0:
        return "Unknown"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return f"{seconds}s"


def format_percentage(value: float) -> str:
    """
    Format percentage value.

    Args:
        value: Percentage value

    Returns:
        str: Formatted string (e.g., "45.67%")
    """
    return f"{value:.2f}%"