"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_api():
    """Mock NetatmoAPI instance."""
    api = Mock()
    api.list_thermostat_rooms.return_value = [
        {"id": "room1", "name": "Living Room"},
        {"id": "room2", "name": "Bedroom"},
    ]
    return api


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
    monkeypatch.setenv("NETATMO_PASSWORD", "test-password")
    monkeypatch.setenv("NETATMO_HOME_ID", "test-home-id")
