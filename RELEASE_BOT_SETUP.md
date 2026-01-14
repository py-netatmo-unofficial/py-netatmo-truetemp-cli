# Release Bot Setup Guide

This guide explains how to configure automated PyPI releases using GitHub's Trusted Publisher feature and GitHub Actions. Once configured, releases are triggered automatically when you push a version tag.

## Overview

The release automation uses:
- **GitHub Actions** - Runs the release workflow
- **PyPI Trusted Publisher** - Secure, token-free authentication
- **Hatchling** - Python build backend
- **Conventional Commits** - Standardized commit messages

## Prerequisites

- Repository admin access
- PyPI account
- Python 3.13+ installed locally

## Step 1: Configure PyPI Trusted Publisher

### 1.1 Create PyPI Account (if needed)

1. Go to https://pypi.org/account/register/
2. Create account and verify email
3. Enable two-factor authentication (recommended)

### 1.2 Add Trusted Publisher

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in the form:

   **PyPI Project Name**: `py-netatmo-truetemp-cli`

   **Owner**: `py-netatmo-unofficial` (or your GitHub username if forked)

   **Repository name**: `py-netatmo-truetemp-cli`

   **Workflow name**: `release.yml`

   **Environment name**: Leave blank (not using environments)

4. Click "Add"

### 1.3 Verify Configuration

You should see a pending publisher entry:
```
py-netatmo-truetemp-cli
  Owner: py-netatmo-unofficial
  Repository: py-netatmo-truetemp-cli
  Workflow: release.yml
  Status: Pending first use
```

**Note**: The status will change to "Active" after the first successful release.

## Step 2: Configure GitHub Repository

### 2.1 Verify Workflow File

Ensure `.github/workflows/release.yml` exists and contains:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Validate version consistency
        run: uv run python scripts/validate_version.py

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

      - name: Create GitHub Release
        uses: softprops/action-gh-releases@v1
        with:
          body: |
            See [CHANGELOG.md](https://github.com/py-netatmo-unofficial/py-netatmo-truetemp-cli/blob/main/CHANGELOG.md) for details.
          files: |
            dist/*
```

### 2.2 Verify Permissions

1. Go to repository Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Ensure "Read and write permissions" is selected
4. Click "Save"

## Step 3: Test Release Process

### 3.1 Local Validation

Before creating a release, test the build process locally:

```bash
# Validate version consistency
uv run python scripts/validate_version.py

# Build package
uv build

# Verify build artifacts
ls -lh dist/
# Should show:
#   py_netatmo_truetemp_cli-0.1.0-py3-none-any.whl
#   py_netatmo_truetemp_cli-0.1.0.tar.gz
```

### 3.2 Create Test Release

1. **Update version in two locations**:

   Edit `src/netatmo_truetemp_cli/__init__.py`:
   ```python
   __version__ = "0.1.0"
   ```

   Edit `pyproject.toml`:
   ```toml
   [project]
   version = "0.1.0"
   ```

2. **Update CHANGELOG.md**:

   Add entry under `## [Unreleased]`:
   ```markdown
   ## [0.1.0] - 2025-01-14

   ### Added
   - Initial release with list-rooms and set-truetemperature commands
   - Rich terminal formatting
   - Environment variable configuration
   ```

3. **Commit changes**:

   ```bash
   git add src/netatmo_truetemp_cli/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to 0.1.0"
   ```

4. **Create and push tag**:

   ```bash
   git tag v0.1.0
   git push origin main
   git push origin v0.1.0
   ```

5. **Monitor workflow**:

   - Go to repository → Actions tab
   - Watch "Release" workflow execute
   - Verify all steps complete successfully

6. **Verify PyPI publication**:

   - Go to https://pypi.org/project/py-netatmo-truetemp-cli/
   - Verify version 0.1.0 is published
   - Test installation: `pip install py-netatmo-truetemp-cli==0.1.0`

7. **Verify GitHub Release**:

   - Go to repository → Releases
   - Verify v0.1.0 release created
   - Verify release artifacts attached

## Step 4: Ongoing Release Process

### Normal Release Workflow

1. **Determine version bump**:
   - **MAJOR** (1.0.0 → 2.0.0): Breaking changes
   - **MINOR** (1.0.0 → 1.1.0): New features
   - **PATCH** (1.0.0 → 1.0.1): Bug fixes

2. **Update version in both files**:
   - `src/netatmo_truetemp_cli/__init__.py`
   - `pyproject.toml`

3. **Update CHANGELOG.md**:
   - Add new section with version and date
   - List changes under "Added", "Changed", "Fixed", "Removed"

4. **Commit and tag**:
   ```bash
   git add src/netatmo_truetemp_cli/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to X.Y.Z"
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z
   ```

5. **Wait for automation**:
   - GitHub Actions builds and publishes to PyPI
   - GitHub Release created automatically

## Troubleshooting

### Issue: "Version validation failed"

**Cause**: Version mismatch between `__init__.py` and `pyproject.toml`

**Solution**:
```bash
# Check current versions
grep __version__ src/netatmo_truetemp_cli/__init__.py
grep version pyproject.toml

# Update to match, then push new tag
git tag -d vX.Y.Z  # Delete local tag
git push origin :refs/tags/vX.Y.Z  # Delete remote tag
# Fix versions and re-tag
```

### Issue: "PyPI upload failed - project name already exists"

**Cause**: PyPI Trusted Publisher not configured correctly

**Solution**:
1. Go to https://pypi.org/manage/account/publishing/
2. Verify "py-netatmo-truetemp-cli" is listed
3. Check repository name, owner, and workflow name match exactly
4. Delete failed tag and re-push after fixing configuration

### Issue: "Permission denied" error in workflow

**Cause**: Insufficient workflow permissions

**Solution**:
1. Go to Settings → Actions → General
2. Enable "Read and write permissions"
3. Ensure `id-token: write` permission in workflow file
4. Re-run workflow

### Issue: "Tag already exists" error

**Cause**: Attempting to reuse version tag

**Solution**:
```bash
# Delete local tag
git tag -d vX.Y.Z

# Delete remote tag
git push origin :refs/tags/vX.Y.Z

# Increment version and create new tag
# Edit __init__.py and pyproject.toml
git commit -m "chore: bump version to X.Y.Z+1"
git tag vX.Y.Z+1
git push origin main
git push origin vX.Y.Z+1
```

### Issue: "Package build failed"

**Cause**: Invalid `pyproject.toml` or missing files

**Solution**:
```bash
# Validate pyproject.toml syntax
python3 -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

# Test build locally
uv build

# Check for missing files
git status
```

## Security Best Practices

1. **Never commit tokens** - Use Trusted Publisher instead of API tokens
2. **Enable 2FA on PyPI** - Protect your account
3. **Review workflow logs** - Check for unexpected behavior
4. **Use signed commits** - Verify release authenticity
5. **Pin action versions** - Use `@v4` instead of `@latest`

## Version Validation Script

The `scripts/validate_version.py` script ensures version consistency:

```python
#!/usr/bin/env python3
"""Validate version consistency across project files."""

import sys
import tomllib
from pathlib import Path

def validate_versions():
    # Read pyproject.toml version
    pyproject_path = Path("pyproject.toml")
    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)
    pyproject_version = pyproject["project"]["version"]

    # Read __init__.py version
    init_path = Path("src/netatmo_truetemp_cli/__init__.py")
    init_content = init_path.read_text()
    for line in init_content.splitlines():
        if line.startswith("__version__"):
            init_version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        print("Error: __version__ not found in __init__.py")
        sys.exit(1)

    # Compare versions
    if pyproject_version != init_version:
        print(f"Version mismatch:")
        print(f"  pyproject.toml: {pyproject_version}")
        print(f"  __init__.py: {init_version}")
        sys.exit(1)

    print(f"Version validation successful: {pyproject_version}")

if __name__ == "__main__":
    validate_versions()
```

## References

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions - PyPI Publish](https://github.com/marketplace/actions/pypi-publish)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
