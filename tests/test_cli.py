"""Tests for CLI commands."""

from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from py_netatmo_truetemp_cli.cli import app

runner = CliRunner()


@pytest.fixture
def mock_api_fixture():
    """Create mock API for CLI tests."""
    api = Mock()
    api.list_thermostat_rooms.return_value = [
        {"id": "room1", "name": "Living Room"},
        {"id": "room2", "name": "Bedroom"},
    ]
    return api


class TestListRooms:
    """Tests for list-rooms command."""

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_list_rooms_success(self, mock_api_class, mock_env_vars, mock_api_fixture):
        """Test successful room listing."""
        mock_api_class.return_value = mock_api_fixture

        result = runner.invoke(app, ["list-rooms"])

        assert result.exit_code == 0
        assert "Living Room" in result.stdout
        assert "Bedroom" in result.stdout

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_list_rooms_with_home_id(self, mock_api_class, mock_env_vars, mock_api_fixture):
        """Test room listing with home ID."""
        mock_api_class.return_value = mock_api_fixture

        result = runner.invoke(app, ["list-rooms", "--home-id", "test-home"])

        assert result.exit_code == 0
        mock_api_fixture.list_thermostat_rooms.assert_called_once_with(home_id="test-home")

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_list_rooms_empty(self, mock_api_class, mock_env_vars):
        """Test room listing with no rooms."""
        api = Mock()
        api.list_thermostat_rooms.return_value = []
        mock_api_class.return_value = api

        result = runner.invoke(app, ["list-rooms"])

        assert result.exit_code == 0
        assert "No rooms with thermostats found" in result.stdout


class TestSetTruetemperature:
    """Tests for set-truetemperature command."""

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_set_temperature_by_name(self, mock_api_class, mock_env_vars, mock_api_fixture):
        """Test setting temperature by room name."""
        mock_api_class.return_value = mock_api_fixture

        result = runner.invoke(
            app, ["set-truetemperature", "--room-name", "Living Room", "--temperature", "20.5"]
        )

        assert result.exit_code == 0
        mock_api_fixture.set_truetemperature.assert_called_once_with(
            room_id="room1", corrected_temperature=20.5, home_id=None
        )
        assert "Living Room" in result.stdout
        assert "20.5" in result.stdout

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_set_temperature_by_id(self, mock_api_class, mock_env_vars, mock_api_fixture):
        """Test setting temperature by room ID."""
        mock_api_class.return_value = mock_api_fixture

        result = runner.invoke(
            app, ["set-truetemperature", "--room-id", "room2", "--temperature", "19.0"]
        )

        assert result.exit_code == 0
        mock_api_fixture.set_truetemperature.assert_called_once_with(
            room_id="room2", corrected_temperature=19.0, home_id=None
        )

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_set_temperature_missing_room(self, mock_api_class, mock_env_vars):
        """Test error when neither room ID nor name provided."""
        result = runner.invoke(app, ["set-truetemperature", "--temperature", "20.5"])

        assert result.exit_code == 1
        # Error messages are written to stderr
        output = result.stdout + result.stderr
        assert "Either --room-id or --room-name must be provided" in output

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_set_temperature_both_room_params(self, mock_api_class, mock_env_vars):
        """Test error when both room ID and name provided."""
        result = runner.invoke(
            app,
            [
                "set-truetemperature",
                "--room-id",
                "room1",
                "--room-name",
                "Living Room",
                "--temperature",
                "20.5",
            ],
        )

        assert result.exit_code == 1
        # Error messages are written to stderr
        output = result.stdout + result.stderr
        assert "Cannot use both --room-id and --room-name" in output
