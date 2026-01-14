# py-netatmo-truetemp-cli

Official CLI tool for [py-netatmo-truetemp](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp) - control your Netatmo thermostats from the command line.

[![PyPI version](https://badge.fury.io/py/py-netatmo-truetemp-cli.svg)](https://pypi.org/project/py-netatmo-truetemp-cli/)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🏠 List all rooms with thermostats
- 🌡️ Set calibrated temperatures for rooms
- 🎨 Beautiful CLI with Rich formatting
- ⚡ Fast and reliable with py-netatmo-truetemp library
- 🔒 Secure environment variable configuration

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

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NETATMO_USERNAME` | Yes | Your Netatmo account email |
| `NETATMO_PASSWORD` | Yes | Your Netatmo account password |
| `NETATMO_HOME_ID` | No | Home ID (auto-detected if omitted) |

**Security Note:** Never commit credentials to version control. Use environment variables or a secure credential manager.

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

## Links

- [GitHub Repository](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli)
- [PyPI Package](https://pypi.org/project/py-netatmo-truetemp-cli/)
- [Issue Tracker](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/issues)
- [py-netatmo-truetemp Library](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp)

## Acknowledgments

Built with [py-netatmo-truetemp](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp), [Typer](https://typer.tiangolo.com/), and [Rich](https://rich.readthedocs.io/).
