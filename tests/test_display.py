"""Tests for display functions."""

from unittest.mock import patch

from py_netatmo_truetemp_cli.display import (
    display_error_panel,
    display_rooms_table,
    display_temperature_result,
)


class TestDisplayRoomsTable:
    """Tests for display_rooms_table function."""

    @patch("py_netatmo_truetemp_cli.display.console")
    def test_display_empty_rooms(self, mock_console):
        """Test display with empty rooms list."""
        display_rooms_table([])

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "No rooms with thermostats found" in call_args

    @patch("py_netatmo_truetemp_cli.display.console")
    def test_display_multiple_rooms(self, mock_console):
        """Test display with multiple rooms."""
        rooms = [
            {"id": "room1", "name": "Living Room"},
            {"id": "room2", "name": "Bedroom"},
            {"id": "room3", "name": "Kitchen"},
        ]

        display_rooms_table(rooms)

        mock_console.print.assert_called_once()
        # Verify table was printed (exact format depends on Rich library)
        assert mock_console.print.called


class TestDisplayTemperatureResult:
    """Tests for display_temperature_result function."""

    @patch("py_netatmo_truetemp_cli.display.console")
    def test_display_success_message(self, mock_console):
        """Test success message display."""
        display_temperature_result("Living Room", 20.5)

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Living Room" in call_args
        assert "20.5" in call_args


class TestDisplayErrorPanel:
    """Tests for display_error_panel function."""

    @patch("py_netatmo_truetemp_cli.display.error_console")
    def test_display_error(self, mock_error_console):
        """Test error panel display."""
        display_error_panel("Test Error", "This is a test error message")

        mock_error_console.print.assert_called_once()
        # Verify Panel was created and printed (exact format depends on Rich library)
        assert mock_error_console.print.called
