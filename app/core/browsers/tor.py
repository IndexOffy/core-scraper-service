"""Tor Browser Module"""

import os

from selenium import webdriver
from tbselenium.common import USE_RUNNING_TOR
from tbselenium.tbdriver import TorBrowserDriver

from app.core.browsers.abc import Browser


class TorBrowser(Browser):
    """Tor Browser implementation using tbselenium."""

    def __init__(
        self,
        headless: bool = True,
        multi_instances: bool = False,
        tor_browser_path: str | None = None,
        tor_data_dir: str | None = None,
        use_running_tor: bool = False,
    ) -> None:
        """
        Initialize Tor Browser.
        """
        self.tor_browser_path = (
            tor_browser_path
            or os.environ.get("TOR_BROWSER_PATH")
            or "/var/task/opt/tor-browser"
        )
        self.tor_data_dir = tor_data_dir or os.environ.get(
            "TOR_DATA_DIR", "/tmp/tor-data"
        )
        self.use_running_tor = use_running_tor
        super().__init__(headless=headless, multi_instances=multi_instances)

    def _set_executable(self) -> None:
        """Set Tor Browser executable path."""
        self.executable = self.tor_browser_path

    def _set_options(self) -> None:
        """Set Tor Browser options."""
        self.options = None

    def _create_driver(self) -> webdriver.Firefox:
        """
        Create a new TorBrowserDriver instance.

        Returns:
            TorBrowserDriver instance

        Raises:
            ValueError: If tor_browser_path is not set or invalid
        """
        if not self.tor_browser_path:
            raise ValueError(
                "Tor Browser path is required. "
                "Set TOR_BROWSER_PATH environment variable or "
                "pass tor_browser_path parameter."
            )

        tor_browser_path = os.path.abspath(
            os.path.expanduser(self.tor_browser_path)
        )

        if not os.path.exists(tor_browser_path):
            raise ValueError(
                f"Tor Browser path does not exist: {tor_browser_path}. "
                "Please verify TOR_BROWSER_PATH points to a valid "
                "Tor Browser installation."
            )

        driver_kwargs = {}
        if self.tor_data_dir:
            tor_data_dir = os.path.abspath(
                os.path.expanduser(self.tor_data_dir)
            )
            os.makedirs(tor_data_dir, exist_ok=True)
            driver_kwargs["tor_data_dir"] = tor_data_dir
        if self.use_running_tor:
            driver_kwargs["use_running_tor"] = USE_RUNNING_TOR

        driver = TorBrowserDriver(tor_browser_path, **driver_kwargs)
        driver.implicitly_wait(5)
        return driver

    def get_instance(self) -> webdriver.Firefox:
        """
        Get Tor Browser driver instance.

        Returns:
            TorBrowserDriver instance
        """
        if self.multi_instances:
            return self._create_driver()

        if not self.instance:
            self.instance = self._create_driver()

        return self.instance
