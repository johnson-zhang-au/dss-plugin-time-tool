# DSS Plugin Time Tool

A Dataiku plugin that provides time-related functionality through an agent tool. This plugin allows you to get current time in specific timezones and convert times between different timezones.

## Features

- Get current time in any IANA timezone
- Convert time between different timezones
- Support for daylight saving time (DST)
- Detailed time difference calculations
- Comprehensive logging

## Installation

1. Download the plugin from the Dataiku plugin store or build it from source
2. Install it in your Dataiku instance
3. Configure the plugin in your Dataiku project

## Usage

The Time Tool provides two main actions:

### 1. Get Current Time

Get the current time in a specific timezone.

```json
{
    "action": "get_current_time",
    "timezone": "America/New_York"  // Optional, defaults to UTC
}
```

Response:
```json
{
    "output": {
        "timezone": "America/New_York",
        "datetime": "2024-03-21T10:30:00-04:00",
        "is_dst": true
    }
}
```

### 2. Convert Time

Convert a time from one timezone to another.

```json
{
    "action": "convert_time",
    "time": "14:30",  // Required, in 24-hour format (HH:MM)
    "source_timezone": "Europe/London",  // Optional, defaults to UTC
    "target_timezone": "Asia/Tokyo"  // Optional, defaults to UTC
}
```

Response:
```json
{
    "output": {
        "source": {
            "timezone": "Europe/London",
            "datetime": "2024-03-21T14:30:00+00:00",
            "is_dst": false
        },
        "target": {
            "timezone": "Asia/Tokyo",
            "datetime": "2024-03-21T23:30:00+09:00",
            "is_dst": false
        },
        "time_difference": "+9.0h"
    }
}
```

## Configuration

The plugin can be configured with the following settings:

- `logging_level`: Set the logging level (default: "INFO")
  - Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Requirements

- Python 3.7+
- Dataiku DSS 11.0+
- `zoneinfo` module (included in Python 3.9+, available as `backports.zoneinfo` for earlier versions)

## Error Handling

The tool provides detailed error messages for common issues:
- Invalid timezone names
- Invalid time formats
- Missing required fields
- Invalid actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This plugin is licensed under the Apache License 2.0. 