"""Tests for browser modules."""

import unittest
from unittest.mock import MagicMock, patch

from app.core.browsers.abc import Browser


class MockBrowser(Browser):
    """Mock browser for testing."""

    def _set_executable(self) -> None:
        """Set mock executable."""
        self.executable = "/mock/browser"

    def _set_options(self) -> None:
        """Set mock options."""
        self.options = MagicMock()

    def get_instance(self):
        """Get mock instance."""
        return MagicMock()


class TestBrowserABC(unittest.TestCase):
    """Test Browser abstract base class."""

    def test_browser_initialization(self):
        """Test browser initialization."""
        browser = MockBrowser(headless=True, multi_instances=False)
        self.assertTrue(browser.headless)
        self.assertFalse(browser.multi_instances)
        self.assertIsNotNone(browser.executable)
        self.assertIsNotNone(browser.options)

    def test_browser_headless_mode(self):
        """Test browser headless mode."""
        browser = MockBrowser(headless=True)
        self.assertTrue(browser.headless)

        browser = MockBrowser(headless=False)
        self.assertFalse(browser.headless)

    def test_browser_multi_instances(self):
        """Test browser multi_instances mode."""
        browser = MockBrowser(multi_instances=True)
        self.assertTrue(browser.multi_instances)

        browser = MockBrowser(multi_instances=False)
        self.assertFalse(browser.multi_instances)

    def test_browser_get_instance(self):
        """Test browser get_instance method."""
        browser = MockBrowser()
        instance = browser.get_instance()
        self.assertIsNotNone(instance)


class TestTorBrowser(unittest.TestCase):
    """Test TorBrowser class."""

    @patch("app.core.browsers.tor.os.path.exists")
    @patch("app.core.browsers.tor.os.path.expanduser")
    def test_tor_browser_path_detection(self, mock_expanduser, mock_exists):
        """Test Tor Browser path detection."""
        from app.core.browsers.tor import TorBrowser

        mock_exists.return_value = False
        mock_expanduser.return_value = "~/tor-browser"

        path = TorBrowser._detect_tor_browser_path()
        self.assertIsNotNone(path)

    def test_tor_browser_initialization(self):
        """Test TorBrowser initialization without actual browser."""
        from app.core.browsers.tor import TorBrowser

        with patch("app.core.browsers.tor.TorBrowser._install_tor_browser"):
            try:
                browser = TorBrowser(headless=True, multi_instances=True)
                self.assertTrue(browser.headless)
                self.assertTrue(browser.multi_instances)
            except (ValueError, FileNotFoundError):
                pass


class TestChromeBrowser(unittest.TestCase):
    """Test Chrome browser class."""

    @patch("app.core.browsers.chrome.ChromeDriverManager")
    @patch("app.core.browsers.chrome.GetGeckoDriver")
    def test_chrome_initialization(self, mock_gecko, mock_chrome_manager):
        """Test Chrome browser initialization."""
        from app.core.browsers.chrome import Chrome

        mock_chrome_manager.return_value.install.return_value = (
            "/mock/chromedriver"
        )
        mock_gecko.return_value.install.return_value = None

        browser = Chrome(headless=True, multi_instances=True)
        self.assertTrue(browser.headless)
        self.assertTrue(browser.multi_instances)
