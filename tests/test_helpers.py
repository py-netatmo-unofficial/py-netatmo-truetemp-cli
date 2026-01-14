"""Tests for helper functions."""

from unittest.mock import patch

import pytest
import typer
from py_netatmo_truetemp.exceptions import RoomNotFoundError

from py_netatmo_truetemp_cli.helpers import (
    NetatmoConfig,
    create_netatmo_api_with_spinner,
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
