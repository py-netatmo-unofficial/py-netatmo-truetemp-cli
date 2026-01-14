"""CLI tool for Netatmo thermostat control using py-netatmo-truetemp."""

try:
    from py_netatmo_cli._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
