# py-netatmo-truetemp-cli

**Netatmo's missing true temperature CLI** - set real room temps from your terminal with a simple, intuitive command-line interface.

[![PyPI version](https://badge.fury.io/py/py-netatmo-truetemp-cli.svg)](https://pypi.org/project/py-netatmo-truetemp-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-netatmo-truetemp-cli)](https://pypi.org/project/py-netatmo-truetemp-cli/)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## ⚠️ Disclaimer

This is an **unofficial** CLI tool for Netatmo thermostats. It is:
- **Not affiliated with or endorsed by Netatmo**
- **Not officially supported** - use at your own risk
- **For personal/educational use** - production use not recommended
- **Subject to archival** - may become unmaintained if I lose access to Netatmo hardware

**Use responsibly**: This tool controls heating equipment. Test thoroughly before relying on it.

## Features

- **Accurate Temperature Control**: Uses TrueTemperature calibration system for precise setpoints
- **Room-by-Room Management**: Control individual rooms by name or ID
- **Beautiful Terminal Output**: Rich formatting with tables and styled panels
- **Secure Configuration**: Environment variable-based credential management
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Robust Error Handling**: User-friendly error messages with actionable guidance

## Installation

```bash
pip install py-netatmo-truetemp-cli
```

## Quick Start

### 1. Set Environment Variables

```bash
export NETATMO_USERNAME="your.email@example.com"
export NETATMO_PASSWORD="your-password"
export NETATMO_HOME_ID="your-home-id"  # Optional, auto-detected if omitted
```

### 2. List Rooms

```bash
netatmo-truetemp list-rooms
```

### 3. Set Temperature

```bash
# By room name (case-insensitive)
netatmo-truetemp set-truetemperature --room-name "Living Room" --temperature 20.5

# By room ID
netatmo-truetemp set-truetemperature --room-id 1234567890 --temperature 20.5
```

## Commands

### `list-rooms`

Lists all rooms with thermostats in your home.

**Options:**
- `--home-id TEXT`: Home ID (optional, uses default if not provided)

**Example:**
```bash
netatmo-truetemp list-rooms
netatmo-truetemp list-rooms --home-id <home_id>
```

### `set-truetemperature`

Sets the calibrated temperature for a Netatmo room.

**Options:**
- `--temperature FLOAT`: Temperature value (required)
- `--room-id TEXT`: Room ID to set temperature for
- `--room-name TEXT`: Room name to set temperature for (alternative to --room-id)
- `--home-id TEXT`: Home ID (optional, uses default if not provided)

**Examples:**
```bash
netatmo-truetemp set-truetemperature --room-name "Living Room" --temperature 20.5
netatmo-truetemp set-truetemperature --room-id 1234567890 --temperature 19.0
```

## Common Use Cases

### List Available Rooms
```bash
netatmo-truetemp list-rooms
```

### Set Room Temperature
```bash
# By room name (case-insensitive)
netatmo-truetemp set-truetemperature --room-name "Living Room" --temperature 21.0

# By room ID (for automation scripts)
netatmo-truetemp set-truetemperature --room-id "1234567890abcdef" --temperature 21.0
```

### Automation Example
```bash
#!/bin/bash
# Adjust bedroom temperature based on time of day
HOUR=$(date +%H)

if [ $HOUR -ge 22 ]; then
    netatmo-truetemp set-truetemperature --room-name "Bedroom" --temperature 18.0
fi
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NETATMO_USERNAME` | Yes | Your Netatmo account email |
| `NETATMO_PASSWORD` | Yes | Your Netatmo account password |
| `NETATMO_HOME_ID` | No | Home ID (auto-detected if omitted) |

## Security

**Credential Management**:
- Store credentials in environment variables (never commit to version control)
- For CI/CD or automation, use your platform's secret management system

**Authentication Cache**:
The underlying library caches authentication tokens at:
- Linux: `~/.local/share/netatmo-truetemp/`
- macOS: `~/Library/Application Support/netatmo-truetemp/`
- Windows: `%LOCALAPPDATA%\netatmo-truetemp\`

To report security vulnerabilities, see [SECURITY.md](SECURITY.md).

## Development

### Setup

```bash
git clone https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli.git
cd py-netatmo-truetemp-cli
uv venv
uv sync
uv run pre-commit install
```

### Run Tests

```bash
uv run pytest
```

### Run Linting

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

### Run Type Checking

```bash
uv run mypy src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

Having issues or want to contribute?

- **Bug Reports**: [Create an issue](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/issues/new?template=bug_report.md)
- **Feature Requests**: [Request a feature](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/issues/new?template=feature_request.md)
- **Discussions**: [Join the conversation](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Issues**: See [SECURITY.md](SECURITY.md)

**Related Projects**:
- [py-netatmo-truetemp](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp) - The underlying Python library
- [PyPI Package](https://pypi.org/project/py-netatmo-truetemp-cli/)

## Acknowledgments

Built with [py-netatmo-truetemp](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp), [Typer](https://typer.tiangolo.com/), and [Rich](https://rich.readthedocs.io/).
