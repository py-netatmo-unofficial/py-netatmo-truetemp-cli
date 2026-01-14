"""Tests for package initialization."""


def test_version_import_success():
    """Test successful version import."""
    from py_netatmo_truetemp_cli import __version__

    assert isinstance(__version__, str)
    # Version should be set (either real version or fallback)
    assert len(__version__) > 0


def test_all_exports():
    """Test __all__ exports."""
    from py_netatmo_truetemp_cli import __all__

    assert "__version__" in __all__


def test_package_imports():
    """Test that package imports work correctly."""
    # This ensures the package is importable and __init__.py works
    import py_netatmo_truetemp_cli

    assert hasattr(py_netatmo_truetemp_cli, "__version__")
    assert isinstance(py_netatmo_truetemp_cli.__version__, str)
