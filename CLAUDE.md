# CLAUDE.md - py-netatmo-truetemp-cli

This file provides comprehensive guidance for developing and maintaining the py-netatmo-truetemp-cli package.

## Overview

**py-netatmo-truetemp-cli** is a standalone CLI tool for controlling Netatmo thermostats. It wraps the [py-netatmo-truetemp](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp) library with a user-friendly command-line interface built using Typer and Rich.

### Key Features

- List all rooms with thermostats in your home
- Set calibrated temperatures by room name or ID
- Beautiful terminal output with Rich formatting
- Robust error handling with user-friendly messages
- Environment variable configuration for security

## Project Structure

```
py-netatmo-truetemp-cli/
├── src/
│   └── py_netatmo_truetemp_cli/
│       ├── __init__.py          # Package initialization, version export
│       ├── cli.py               # Typer app, command definitions
│       ├── display.py           # Rich formatting (tables, panels)
│       └── helpers.py           # API initialization, error handling
├── tests/
│   ├── __init__.py
│   ├── test_cli.py             # CLI command tests
│   ├── test_display.py         # Display function tests
│   └── test_helpers.py         # Helper function tests
├── scripts/
│   └── validate_version.py     # Release automation validation
├── docs/
│   ├── architecture.md         # Architecture documentation
│   └── development.md          # Development guide
├── .github/
│   ├── workflows/
│   │   ├── ci.yml             # CI pipeline (test, lint, type-check)
│   │   └── release.yml        # Release automation (PyPI publish)
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
├── pyproject.toml             # Project metadata, dependencies, build config
├── uv.lock                    # Dependency lock file
├── README.md                  # User-facing documentation
├── CLAUDE.md                  # This file (developer documentation)
├── CHANGELOG.md               # Release history
├── CONTRIBUTING.md            # Contribution guidelines
├── CODE_OF_CONDUCT.md         # Community guidelines
├── SECURITY.md                # Security policy
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore patterns
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── mise.toml                  # Mise version manager config (Python 3.13+)
└── .python-version            # Python version for mise
```

## Architecture

### Module Responsibilities

#### `src/py_netatmo_truetemp_cli/cli.py`

**Purpose**: Command-line interface entry point and command definitions.

**Responsibilities**:
- Define Typer app and commands (`list-rooms`, `set-truetemperature`)
- Parse and validate command-line arguments
- Route commands to appropriate helper functions
- Handle command-level error responses

**Key Functions**:
- `list_rooms()` - Command to list all rooms with thermostats
- `set_truetemperature()` - Command to set calibrated temperature for a room

**Design Pattern**: Command pattern with dependency injection via helpers module.

#### `src/py_netatmo_truetemp_cli/helpers.py`

**Purpose**: Business logic, API initialization, and error handling.

**Responsibilities**:
- Load configuration from environment variables
- Initialize Netatmo API with authentication
- Resolve room names to room IDs (case-insensitive)
- Validate command inputs
- Provide consistent error handling via decorator

**Key Functions**:
- `NetatmoConfig.from_environment()` - Loads credentials from environment
- `create_netatmo_api_with_spinner()` - Initializes API with loading indicator
- `handle_api_errors()` - Decorator for consistent error handling
- `resolve_room_id()` - Resolves room name to ID with case-insensitive lookup
- `validate_room_input()` - Validates mutual exclusivity of room-id/room-name

**Design Pattern**: Factory pattern for API initialization, decorator pattern for error handling.

#### `src/py_netatmo_truetemp_cli/display.py`

**Purpose**: Terminal UI presentation layer using Rich library.

**Responsibilities**:
- Format and display data in tables
- Display success messages with styled panels
- Display error messages with styled panels
- Provide consistent visual styling across commands

**Key Functions**:
- `display_rooms_table()` - Formats room list as Rich table
- `display_temperature_result()` - Displays success message for temperature changes
- `display_error_panel()` - Displays error messages in styled panel

**Design Pattern**: Facade pattern over Rich library for consistent styling.

### Data Flow

1. **User Input** → CLI command with arguments
2. **CLI Layer** (`cli.py`) → Parses arguments, validates input
3. **Helper Layer** (`helpers.py`) → Initializes API, resolves identifiers
4. **API Layer** (py-netatmo-truetemp) → Communicates with Netatmo API
5. **Display Layer** (`display.py`) → Formats and displays results
6. **User Output** → Styled terminal output

### Error Handling Strategy

**Error Propagation**:
1. Library exceptions (py-netatmo-truetemp) bubble up
2. `@handle_api_errors` decorator catches all exceptions
3. Error panel displayed via `display_error_panel()`
4. Exit with appropriate status code via `click.Abort()`

**Exception Handling Hierarchy**:
- `AuthenticationError` → "Authentication failed" message
- `ValidationError` → "Invalid input" message
- `APIError` → "API communication error" message
- `NetatmoError` → Generic Netatmo error message
- `Exception` → Unexpected error with traceback

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli.git
cd py-netatmo-truetemp-cli

# Install mise (if not already installed)
curl https://mise.run | sh

# Install Python 3.13+ via mise
mise install

# Create virtual environment and install dependencies
uv venv
uv sync

# Install pre-commit hooks
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

### Running the CLI Locally

```bash
# Set environment variables
export NETATMO_USERNAME="your.email@example.com"
export NETATMO_PASSWORD="your-password"

# Run CLI commands
uv run netatmo-truetemp list-rooms
uv run netatmo-truetemp set-truetemperature --room-name "Living Room" --temperature 20.5
```

### Testing Strategy

#### Unit Tests

**Location**: `tests/`

**Coverage Requirements**:
- Minimum 80% code coverage
- 100% coverage for critical paths (authentication, API calls)

**Test Structure**:
```python
# tests/test_helpers.py
def test_resolve_room_id_case_insensitive(mock_api):
    """Test room name resolution with case-insensitive matching."""
    room_id, room_name = resolve_room_id(mock_api, None, "living room", None)
    assert room_id == "expected_id"
    assert room_name == "Living Room"
```

**Running Tests**:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=py_netatmo_truetemp_cli --cov-report=html

# Run specific test file
uv run pytest tests/test_helpers.py

# Run specific test
uv run pytest tests/test_helpers.py::test_resolve_room_id
```

#### Integration Tests

**Purpose**: Test end-to-end CLI functionality with mocked API responses.

**Location**: `tests/test_cli.py`

**Strategy**:
- Mock `py_netatmo_truetemp.NetatmoAPI` responses
- Test CLI commands via Typer's `CliRunner`
- Verify output formatting and error handling

#### Manual Testing

**Test Cases**:
1. List rooms with default home
2. List rooms with explicit home ID
3. Set temperature by room name
4. Set temperature by room ID
5. Handle authentication errors
6. Handle API errors
7. Handle invalid room names/IDs

### Code Quality Tools

#### Ruff (Linting and Formatting)

**Configuration**: `pyproject.toml`

```bash
# Check for lint issues
uv run ruff check src/ tests/

# Auto-fix lint issues
uv run ruff check src/ tests/ --fix

# Format code
uv run ruff format src/ tests/
```

#### Mypy (Type Checking)

**Configuration**: `pyproject.toml`

```bash
# Type check source code
uv run mypy src/

# Type check with strict mode
uv run mypy src/ --strict
```

#### Pre-commit Hooks

**Configuration**: `.pre-commit-config.yaml`

**Hooks**:
- `ruff` - Auto-fix lint issues
- `ruff-format` - Format code
- `trailing-whitespace` - Remove trailing whitespace
- `end-of-file-fixer` - Ensure files end with newline
- `check-yaml` - Validate YAML syntax
- `check-toml` - Validate TOML syntax
- `check-added-large-files` - Prevent large file commits
- `conventional-pre-commit` - Validate commit messages

**Running Manually**:
```bash
# Run all hooks on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run ruff --all-files
```

## Release Automation

### Versioning Strategy

**Scheme**: Semantic Versioning (SemVer) - `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (e.g., CLI argument changes, removed commands)
- **MINOR**: New features (e.g., new commands, new options)
- **PATCH**: Bug fixes, documentation updates

**Version Locations**:
- `src/py_netatmo_truetemp_cli/__init__.py` - `__version__` variable
- `pyproject.toml` - `project.version` field

### Release Process

**Automated via GitHub Actions** (`.github/workflows/release.yml`):

1. **Trigger**: Push tag matching `v*.*.*` pattern
2. **Validation**: Verify version consistency across files
3. **Build**: Build source distribution and wheel
4. **Publish**: Upload to PyPI via Trusted Publisher
5. **GitHub Release**: Create release with CHANGELOG excerpt

**Manual Release Steps**:

```bash
# 1. Update version in both locations
# Edit src/py_netatmo_truetemp_cli/__init__.py
__version__ = "1.2.3"

# Edit pyproject.toml
version = "1.2.3"

# 2. Update CHANGELOG.md
# Add new section under "## [Unreleased]"

# 3. Commit changes
git add src/py_netatmo_truetemp_cli/__init__.py pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 1.2.3"

# 4. Create and push tag
git tag v1.2.3
git push origin main
git push origin v1.2.3

# 5. GitHub Actions automatically publishes to PyPI
```

### Version Validation

**Script**: `scripts/validate_version.py`

**Purpose**: Ensure version consistency before release.

**Usage**:
```bash
# Validate version consistency
uv run python scripts/validate_version.py

# Expected output (success):
# Version validation successful: 1.2.3

# Expected output (failure):
# Version mismatch:
#   pyproject.toml: 1.2.3
#   __init__.py: 1.2.2
```

## CI/CD Pipelines

### CI Pipeline (`.github/workflows/ci.yml`)

**Triggers**: Push to main, pull requests

**Jobs**:
1. **Test** - Run pytest with coverage reporting
2. **Lint** - Run ruff linting
3. **Format** - Verify ruff formatting
4. **Type Check** - Run mypy type checking

**Matrix Strategy**: Test on Python 3.13+ on Linux, macOS, Windows

### Release Pipeline (`.github/workflows/release.yml`)

**Trigger**: Push tag matching `v*.*.*`

**Jobs**:
1. **Validate** - Run `scripts/validate_version.py`
2. **Build** - Build source distribution and wheel
3. **Publish** - Upload to PyPI via Trusted Publisher
4. **Create Release** - Create GitHub release with CHANGELOG

## Configuration Files

### `pyproject.toml`

**Sections**:
- `[project]` - Package metadata, dependencies
- `[project.scripts]` - CLI entry point (`netatmo-truetemp`)
- `[build-system]` - Build backend (Hatchling)
- `[tool.ruff]` - Ruff linting configuration
- `[tool.mypy]` - Mypy type checking configuration
- `[tool.pytest]` - Pytest configuration
- `[tool.coverage]` - Coverage reporting configuration

### `mise.toml`

**Purpose**: Define Python version requirement (3.13+).

**Content**:
```toml
[tools]
python = "3.13"
```

### `.python-version`

**Purpose**: Specify Python version for mise and other tools.

**Content**:
```
3.13
```

## Security Considerations

### Credential Management

**Environment Variables** (recommended):
```bash
export NETATMO_USERNAME="your.email@example.com"
export NETATMO_PASSWORD="your-password"
export NETATMO_HOME_ID="your-home-id"  # Optional
```

**Security Best Practices**:
- Never commit credentials to version control
- Use environment variables or secure credential managers
- Credentials stored in persistent cookies by py-netatmo-truetemp library
- Cookie storage location: `~/.netatmo-cookie` (platform-specific via platformdirs)

### Dependency Security

**Automated Scanning**:
- Dependabot configured in `.github/dependabot.yml`
- Weekly security updates for GitHub Actions and Python dependencies

**Manual Audit**:
```bash
# Check for known vulnerabilities
uv run pip-audit
```

## Troubleshooting

### Common Issues

#### Authentication Failures

**Symptoms**: "Authentication failed" error

**Diagnosis**:
1. Verify environment variables are set: `env | grep NETATMO`
2. Check credentials are correct
3. Delete cached cookies: `rm ~/.netatmo-cookie`
4. Enable debug logging in py-netatmo-truetemp

#### Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'py_netatmo_truetemp_cli'`

**Diagnosis**:
1. Verify virtual environment is activated: `which python`
2. Reinstall package: `uv sync`
3. Check Python version: `python --version` (must be 3.13+)

#### CLI Command Not Found

**Symptoms**: `netatmo-truetemp: command not found`

**Diagnosis**:
1. Verify installation: `uv pip list | grep netatmo`
2. Check entry point in pyproject.toml: `[project.scripts]`
3. Reinstall package: `uv sync`
4. Use explicit invocation: `uv run netatmo-truetemp`

#### API Communication Errors

**Symptoms**: "API communication error" message

**Diagnosis**:
1. Check internet connectivity
2. Verify Netatmo API is accessible: `curl https://api.netatmo.com`
3. Check for rate limiting (wait and retry)
4. Enable debug logging for detailed error information

### Debug Logging

**Enable Debug Logging** (via py-netatmo-truetemp):
```bash
export NETATMO_DEBUG=1
uv run netatmo-truetemp list-rooms
```

**Disable Debug Logging**:
```bash
unset NETATMO_DEBUG
```

## Contributing

### Contribution Workflow

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/py-netatmo-truetemp-cli.git
   cd py-netatmo-truetemp-cli
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make Changes**
   - Follow code style (Ruff)
   - Add tests for new functionality
   - Update documentation

4. **Test Changes**
   ```bash
   uv run pytest
   uv run ruff check src/ tests/
   uv run mypy src/
   ```

5. **Commit with Conventional Commits**
   ```bash
   git commit -m "feat: add new command for listing homes"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/my-new-feature
   ```

### Conventional Commits

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting)
- `refactor` - Code refactoring
- `test` - Test changes
- `chore` - Build/tooling changes

**Examples**:
```bash
feat(cli): add new command for listing homes
fix(helpers): handle missing room name gracefully
docs(readme): update installation instructions
chore(deps): update py-netatmo-truetemp to 1.2.0
```

## Best Practices

1. **Keep CLI simple** - Focus on common use cases, avoid feature bloat
2. **Provide helpful error messages** - Guide users to resolution
3. **Use environment variables for credentials** - Never hardcode secrets
4. **Test with real devices** - Ensure compatibility with actual Netatmo hardware
5. **Document all commands** - Keep README and help text up-to-date
6. **Follow semantic versioning** - Communicate breaking changes clearly
7. **Maintain test coverage** - Aim for 80%+ coverage
8. **Use type hints** - Improve code clarity and catch errors early

## Links

- **GitHub Repository**: https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli
- **PyPI Package**: https://pypi.org/project/py-netatmo-truetemp-cli/
- **py-netatmo-truetemp Library**: https://github.com/py-netatmo-unofficial/py-netatmo-truetemp
- **Issue Tracker**: https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/issues
- **Typer Documentation**: https://typer.tiangolo.com/
- **Rich Documentation**: https://rich.readthedocs.io/
