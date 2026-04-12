# tests/test_network.py
"""
Network connectivity tests for gFetch.
Uses unittest.mock to simulate connection states without real network calls.
"""

import pytest
from unittest.mock import patch, MagicMock
import requests
from main import NetworkTestGlobal, NetworkTestNCBI, CheckConnection


# ── NetworkTestGlobal ──────────────────────────────────────────────────────────

class TestNetworkTestGlobal:

    def test_returns_true_on_success(self):
        """Should return True when Google is reachable."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            assert NetworkTestGlobal() is True

    def test_returns_false_on_unexpected_status(self):
        """Should return False on non-200 status code."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        with patch("requests.get", return_value=mock_response):
            assert NetworkTestGlobal() is False

    def test_returns_false_on_connection_error(self):
        """Should return False when connection is refused."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            assert NetworkTestGlobal() is False

    def test_returns_false_on_timeout(self):
        """Should return False when connection times out."""
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            assert NetworkTestGlobal() is False

    def test_does_not_raise_on_connection_error(self):
        """Should never raise an exception on connection failure."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            try:
                NetworkTestGlobal()
            except Exception as e:
                pytest.fail(f"NetworkTestGlobal() raised an exception: {e}")


# ── NetworkTestNCBI ────────────────────────────────────────────────────────────

class TestNetworkTestNCBI:

    def test_returns_true_on_success(self):
        """Should return True when NCBI API is reachable."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            assert NetworkTestNCBI() is True

    def test_returns_false_on_unexpected_status(self):
        """Should return False on non-200 status code."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        with patch("requests.get", return_value=mock_response):
            assert NetworkTestNCBI() is False

    def test_returns_false_on_connection_error(self):
        """Should return False when NCBI API is unreachable."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            assert NetworkTestNCBI() is False

    def test_returns_false_on_timeout(self):
        """Should return False when NCBI API times out."""
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            assert NetworkTestNCBI() is False

    def test_does_not_raise_on_timeout(self):
        """Should never raise an exception on timeout."""
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            try:
                NetworkTestNCBI()
            except Exception as e:
                pytest.fail(f"NetworkTestNCBI() raised an exception: {e}")


# ── CheckConnection ────────────────────────────────────────────────────────────

class TestCheckConnection:

    def test_exits_when_global_fails(self):
        """Should call sys.exit(1) when internet is unavailable."""
        with patch("main.NetworkTestGlobal", return_value=False):
            with pytest.raises(SystemExit) as exc:
                CheckConnection()
            assert exc.value.code == 1

    def test_exits_when_ncbi_fails(self):
        """Should call sys.exit(1) when NCBI is unreachable."""
        with patch("main.NetworkTestGlobal", return_value=True):
            with patch("main.NetworkTestNCBI", return_value=False):
                with pytest.raises(SystemExit) as exc:
                    CheckConnection()
                assert exc.value.code == 1

    def test_passes_when_both_ok(self):
        """Should not raise or exit when both checks pass."""
        with patch("main.NetworkTestGlobal", return_value=True):
            with patch("main.NetworkTestNCBI", return_value=True):
                try:
                    CheckConnection()
                except SystemExit:
                    pytest.fail("CheckConnection() exited unexpectedly")