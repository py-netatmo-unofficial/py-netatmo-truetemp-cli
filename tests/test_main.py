"""Tests for __main__ module entry point."""


def test_main_module_structure():
    """Test that __main__ module has correct structure."""
    import py_netatmo_truetemp_cli.__main__ as main_module

    # Verify the module imports app
    assert hasattr(main_module, "app")

    # Verify app is callable (Typer app)
    assert callable(main_module.app)


def test_main_entry_point_with_help():
    """Test that __main__ can be invoked with --help."""
    import subprocess
    import sys

    # Run the module with --help (should not fail)
    result = subprocess.run(
        [sys.executable, "-m", "py_netatmo_truetemp_cli", "--help"],
        capture_output=True,
        text=True,
    )

    # Should exit successfully with help text
    assert result.returncode == 0
    assert "Usage:" in result.stdout
