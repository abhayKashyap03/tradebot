import unittest
import pytest
from unittest.mock import patch
from tradebot.clients.robinhood_client import RobinhoodClient
from tradebot.configs.config import ROBINHOOD_EMAIL, ROBINHOOD_PWD


class TestRobinhoodClient(unittest.TestCase):
    @patch("robin_stocks.robinhood.login")
    def test_login_success(self, mock_login):
        client = RobinhoodClient("test@example.com", "password")
        client.login()
        self.assertTrue(client.authenticated)
        mock_login.assert_called_once_with(
            username="test@example.com", password="password"
        )

    @patch("robin_stocks.robinhood.login", side_effect=Exception("Login failed"))
    def test_login_failure(self, mock_login):
        client = RobinhoodClient("test@example.com", "password")
        with self.assertRaises(Exception):
            client.login()
        self.assertFalse(client.authenticated)

    @patch("robin_stocks.robinhood.logout")
    def test_logout_success(self, mock_logout):
        client = RobinhoodClient("test@example.com", "password")
        client.authenticated = True
        client.logout()
        self.assertFalse(client.authenticated)
        mock_logout.assert_called_once()

    @patch("robin_stocks.robinhood.logout")
    def test_logout_not_logged_in(self, mock_logout):
        client = RobinhoodClient("test@example.com", "password")
        with self.assertRaises(Exception):
            client.logout()

    @patch("robin_stocks.robinhood.build_holdings")
    @patch("robin_stocks.robinhood.build_user_profile")
    def test_get_portfolio_state_not_logged_in(
        self, mock_build_user_profile, mock_build_holdings
    ):
        client = RobinhoodClient("test@example.com", "password")
        with self.assertRaises(Exception):
            client.get_portfolio_state()


@pytest.mark.integration
def test_robinhood_full_flow_integration():
    """
    This is an integration test that attempts a real login to Robinhood
    using the credentials from your .env file.

    It will likely require you to manually approve the login on your
    Robinhood app.
    """
    client = RobinhoodClient(
        email=ROBINHOOD_EMAIL,
        password=ROBINHOOD_PWD,
    )

    try:
        client.login()
        assert client.authenticated is True

        portfolio = client.get_portfolio_state()
        assert isinstance(portfolio, dict)

    finally:
        if client.authenticated:
            client.logout()
            assert client.authenticated is False
