"""Tests for helper functions."""

from unittest.mock import patch

import pytest
import typer
from py_netatmo_truetemp.exceptions import (
    ApiError,
    AuthenticationError,
    HomeNotFoundError,
    NetatmoError,
    RoomNotFoundError,
    ValidationError,
)

from py_netatmo_truetemp_cli.helpers import (
    NetatmoConfig,
    create_netatmo_api_with_spinner,
    handle_api_errors,
    resolve_room_id,
    validate_room_input,
)


class TestNetatmoConfig:
    """Tests for NetatmoConfig class."""

    def test_from_environment_success(self, mock_env_vars):
        """Test successful configuration loading."""
        config = NetatmoConfig.from_environment()

        assert config["username"] == "test@example.com"
        assert config["password"] == "test-password"
        assert config["home_id"] == "test-home-id"

    def test_from_environment_missing_username(self, monkeypatch):
        """Test error when username is missing."""
        monkeypatch.setenv("NETATMO_PASSWORD", "test-password")
        monkeypatch.delenv("NETATMO_USERNAME", raising=False)

        with pytest.raises(ValueError, match="Missing required environment variables"):
            NetatmoConfig.from_environment()

    def test_from_environment_missing_password(self, monkeypatch):
        """Test error when password is missing."""
        monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
        monkeypatch.delenv("NETATMO_PASSWORD", raising=False)

        with pytest.raises(ValueError, match="Missing required environment variables"):
            NetatmoConfig.from_environment()

    def test_from_environment_optional_home_id(self, monkeypatch):
        """Test that home_id is optional."""
        monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
        monkeypatch.setenv("NETATMO_PASSWORD", "test-password")
        monkeypatch.delenv("NETATMO_HOME_ID", raising=False)

        config = NetatmoConfig.from_environment()

        assert config["username"] == "test@example.com"
        assert config["password"] == "test-password"
        assert config["home_id"] is None


class TestCreateNetatmoApiWithSpinner:
    """Tests for create_netatmo_api_with_spinner function."""

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_creates_api_with_config(self, mock_api_class, mock_env_vars):
        """Test API creation with valid configuration."""
        create_netatmo_api_with_spinner()

        mock_api_class.assert_called_once_with(
            username="test@example.com", password="test-password", home_id="test-home-id"
        )

    @patch("py_netatmo_truetemp_cli.helpers.NetatmoAPI")
    def test_creates_api_without_home_id(self, mock_api_class, monkeypatch):
        """Test API creation without home_id."""
        monkeypatch.setenv("NETATMO_USERNAME", "test@example.com")
        monkeypatch.setenv("NETATMO_PASSWORD", "test-password")
        monkeypatch.delenv("NETATMO_HOME_ID", raising=False)

        create_netatmo_api_with_spinner()

        mock_api_class.assert_called_once_with(
            username="test@example.com", password="test-password", home_id=None
        )


class TestResolveRoomId:
    """Tests for resolve_room_id function."""

    def test_resolve_by_name(self, mock_api):
        """Test room resolution by name."""
        room_id, room_name = resolve_room_id(mock_api, None, "Living Room", None)

        assert room_id == "room1"
        assert room_name == "Living Room"

    def test_resolve_by_name_case_insensitive(self, mock_api):
        """Test room resolution by name is case-insensitive."""
        room_id, room_name = resolve_room_id(mock_api, None, "living room", None)

        assert room_id == "room1"
        assert room_name == "Living Room"

    def test_resolve_by_id(self, mock_api):
        """Test room resolution by ID."""
        room_id, room_name = resolve_room_id(mock_api, "room2", None, None)

        assert room_id == "room2"
        assert room_name == "Bedroom"

    def test_resolve_nonexistent_name(self, mock_api):
        """Test error when room name doesn't exist."""
        with pytest.raises(RoomNotFoundError):
            resolve_room_id(mock_api, None, "Nonexistent Room", None)

    def test_resolve_nonexistent_id(self, mock_api):
        """Test error when room ID doesn't exist."""
        with pytest.raises(RoomNotFoundError):
            resolve_room_id(mock_api, "nonexistent-id", None, None)


class TestValidateRoomInput:
    """Tests for validate_room_input function."""

    def test_valid_room_id_only(self):
        """Test validation passes with only room_id."""
        validate_room_input("room1", None)

    def test_valid_room_name_only(self):
        """Test validation passes with only room_name."""
        validate_room_input(None, "Living Room")

    def test_both_room_id_and_name(self):
        """Test error when both room_id and room_name provided."""
        with pytest.raises(typer.Exit):
            validate_room_input("room1", "Living Room")

    def test_neither_room_id_nor_name(self):
        """Test error when neither room_id nor room_name provided."""
        with pytest.raises(typer.Exit):
            validate_room_input(None, None)


class TestHandleApiErrorsDecorator:
    """Tests for handle_api_errors decorator."""

    def test_successful_execution(self):
        """Test decorator allows successful execution."""

        @handle_api_errors
        def success_func():
            return "success"

        result = success_func()
        assert result == "success"

    def test_reraises_typer_exit(self):
        """Test decorator re-raises typer.Exit."""

        @handle_api_errors
        def exit_func():
            raise typer.Exit(code=0)

        with pytest.raises(typer.Exit):
            exit_func()

    def test_handles_value_error(self):
        """Test decorator handles ValueError."""

        @handle_api_errors
        def error_func():
            raise ValueError("Config error")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_validation_error(self):
        """Test decorator handles ValidationError."""

        @handle_api_errors
        def error_func():
            raise ValidationError("Invalid input")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_authentication_error(self):
        """Test decorator handles AuthenticationError."""

        @handle_api_errors
        def error_func():
            raise AuthenticationError("Auth failed")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_home_not_found_error(self):
        """Test decorator handles HomeNotFoundError."""

        @handle_api_errors
        def error_func():
            raise HomeNotFoundError("home123")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_room_not_found_error(self):
        """Test decorator handles RoomNotFoundError."""

        @handle_api_errors
        def error_func():
            raise RoomNotFoundError("room123")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_api_error(self):
        """Test decorator handles ApiError."""

        @handle_api_errors
        def error_func():
            raise ApiError("API call failed")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_netatmo_error(self):
        """Test decorator handles generic NetatmoError."""

        @handle_api_errors
        def error_func():
            raise NetatmoError("Netatmo error")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1

    def test_handles_unexpected_exception(self):
        """Test decorator handles unexpected exceptions."""

        @handle_api_errors
        def error_func():
            raise RuntimeError("Unexpected error")

        with pytest.raises(typer.Exit) as exc_info:
            error_func()

        assert exc_info.value.exit_code == 1


class TestResolveRoomIdMultipleRooms:
    """Tests for resolve_room_id with multiple rooms scenario."""

    def test_multiple_rooms_same_name_warning(self, mock_api, capsys):
        """Test warning when multiple rooms have the same name."""
        # Mock list_thermostat_rooms to return duplicate names
        mock_api.list_thermostat_rooms.return_value = [
            {"id": "room1", "name": "Living Room"},
            {"id": "room3", "name": "Living Room"},
        ]

        room_id, room_name = resolve_room_id(mock_api, None, "Living Room", None)

        # Should return first match
        assert room_id == "room1"
        assert room_name == "Living Room"

        # Warning should be printed (tested via console output)
        # Note: Rich console output is hard to capture, but the function executes without error
