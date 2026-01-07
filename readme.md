# DeviceMCP

A cross-platform Model Context Protocol (MCP) server that provides device information including system specs, battery status, storage, and memory details for Windows, macOS, Linux, and Android.

## Features

- 🖥️ **Cross-Platform Support**: Works on Windows, macOS, Linux, and Android (via Termux)
- 🔋 **Battery Information**: Get real-time battery level, charging status, and time remaining
- 💾 **Storage Details**: Monitor disk usage across all drives and partitions
- 🧠 **Memory Stats**: Track RAM and swap memory usage
- 📊 **System Info**: Access OS version, hostname, architecture, and processor details
- 🏗️ **Modular Architecture**: Clean, maintainable code with platform-specific implementations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or uv package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv pip install -r requirements.txt
```

### For Android (Termux)

```bash
pkg install python
pip install fastmcp psutil pydantic
# Optional: Install termux-api for better battery info
pkg install termux-api
```

## Usage

### Run Locally (stdio transport)

```bash
python server.py
```

Or using FastMCP CLI:

```bash
fastmcp run server.py:mcp
```

### Run with HTTP Transport

```bash
python server.py --transport http --port 8000
```

Or using FastMCP CLI:

```bash
fastmcp run server.py:mcp --transport http --port 8000
```

### Install in Claude Desktop

Generate the configuration file:

```bash
fastmcp install server.py:mcp --name DeviceMCP
```

Then follow the prompts to install it in Claude Desktop.

## Available Tools

### 1. `get_device_info`

Get comprehensive device information.

**Returns:**
```json
{
  "os_name": "Windows",
  "os_version": "11",
  "hostname": "MY-LAPTOP",
  "architecture": "x86_64",
  "processor": "Intel Core i7-9750H",
  "platform": "windows"
}
```

### 2. `get_battery_level`

Get battery information and charging status.

**Returns:**
```json
{
  "percentage": 85.5,
  "is_charging": true,
  "is_plugged": true,
  "time_remaining": 3600,
  "time_remaining_formatted": "1h 0m",
  "has_battery": true
}
```

### 3. `get_storage_info`

Get storage information for all drives/partitions.

**Returns:**
```json
[
  {
    "total_bytes": 512000000000,
    "used_bytes": 256000000000,
    "free_bytes": 256000000000,
    "usage_percent": 50.0,
    "mount_point": "C:\\",
    "total_formatted": "476.84 GB",
    "used_formatted": "238.42 GB",
    "free_formatted": "238.42 GB"
  }
]
```

### 4. `get_memory_info`

Get RAM and swap memory information.

**Returns:**
```json
{
  "total_bytes": 16000000000,
  "available_bytes": 8000000000,
  "used_bytes": 8000000000,
  "usage_percent": 50.0,
  "swap_total_bytes": 4000000000,
  "swap_used_bytes": 1000000000,
  "total_formatted": "14.90 GB",
  "available_formatted": "7.45 GB",
  "used_formatted": "7.45 GB",
  "swap_total_formatted": "3.73 GB",
  "swap_used_formatted": "953.67 MB"
}
```

### 5. `get_system_summary`

Get all device information in one comprehensive call.

**Returns:** Combined output of all the above tools plus platform detection.

## Project Structure

```
devicemcp/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── fastmcp.json                 # FastMCP configuration
├── server.py                    # Main MCP server entry point
├── core/
│   ├── __init__.py
│   ├── base.py                  # Abstract base classes
│   └── models.py                # Pydantic data models
├── platforms/
│   ├── __init__.py
│   ├── windows.py               # Windows implementation
│   ├── macos.py                 # macOS implementation
│   ├── linux.py                 # Linux implementation
│   └── android.py               # Android implementation
└── utils/
    ├── __init__.py
    ├── platform_detector.py    # Platform auto-detection
    └── formatters.py            # Output formatting utilities
```

## Architecture

The project follows a modular architecture with clear separation of concerns:

- **Core Layer**: Abstract base classes and data models
- **Platform Layer**: Platform-specific implementations
- **Utils Layer**: Helper functions for detection and formatting
- **Server Layer**: FastMCP server with tool definitions

Each platform provider implements the `DeviceInfoProvider` interface, ensuring consistent behavior across all platforms.

## Extending the Server

### Adding a New Platform

1. Create a new file in `platforms/` (e.g., `bsd.py`)
2. Implement the `DeviceInfoProvider` interface
3. Add platform detection logic in `utils/platform_detector.py`
4. Import and register in the factory function

### Adding New Metrics

1. Add new models in `core/models.py`
2. Add abstract methods in `core/base.py`
3. Implement in each platform provider
4. Add tool function in `server.py`

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 style guidelines. Format code with:

```bash
black .
isort .
```

## Troubleshooting

### Battery Information Not Available

Some desktop systems don't have batteries. The server will return `has_battery: false` in such cases.

### Permission Errors on Storage Info

Some drives/partitions may require elevated permissions. The server silently skips inaccessible drives.

### Android Battery Info

For best results on Android, install `termux-api`:
```bash
pkg install termux-api
```

## License

MIT License - feel free to use this in your own projects!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.