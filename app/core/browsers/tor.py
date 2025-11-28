"""Tor Browser Module"""

import logging
import os
import platform
import tarfile
import urllib.request
from pathlib import Path
from typing import Any

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
            or self._detect_tor_browser_path()
        )
        self.tor_data_dir = tor_data_dir or os.environ.get(
            "TOR_DATA_DIR", "/tmp/tor-data"
        )
        self.use_running_tor = use_running_tor
        super().__init__(headless=headless, multi_instances=multi_instances)

    @staticmethod
    def _detect_tor_browser_path() -> str:
        """
        Detect Tor Browser path in common locations.

        Returns:
            Default path for Lambda or common local paths
        """
        common_paths = [
            "/var/task/opt/tor-browser",
            os.path.expanduser("~/tor-browser"),
            os.path.expanduser("~/Tor Browser"),
            "/opt/tor-browser",
            "/usr/local/tor-browser",
        ]
        if os.name == "posix" and os.path.exists("/Applications"):
            macos_paths = [
                "/Applications/Tor Browser.app/Contents/MacOS",
                os.path.expanduser(
                    "~/Applications/Tor Browser.app/Contents/MacOS"
                ),
            ]
            common_paths.extend(macos_paths)
        for path in common_paths:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                browser_dir = os.path.join(expanded, "Browser")
                if os.path.exists(browser_dir):
                    return expanded
        return os.path.expanduser("~/tor-browser")

    @staticmethod
    def _install_tor_browser(install_dir: str) -> str:
        """
        Automatically download and install Tor Browser.

        Args:
            install_dir: Directory to install Tor Browser

        Returns:
            Path to installed Tor Browser
        """
        if platform.system() == "Darwin":
            raise ValueError(
                "macOS requires manual Tor Browser installation. "
                "Download from: https://www.torproject.org/download/"
            )

        version = "13.0.12"
        lang = "en-US"
        url = (
            f"https://www.torproject.org/dist/torbrowser/{version}/"
            f"tor-browser-linux64-{version}_{lang}.tar.xz"
        )

        install_path = Path(install_dir).expanduser()
        install_path.mkdir(parents=True, exist_ok=True)

        tmp_file = install_path / f"tor-browser-{version}.tar.xz"

        logger = logging.getLogger(__name__)
        logger.info("Downloading Tor Browser automatically...")

        try:
            urllib.request.urlretrieve(url, tmp_file)
            logger.info("Extracting Tor Browser...")
            with tarfile.open(tmp_file, "r:xz") as tar:
                tar.extractall(install_path)
                members = tar.getmembers()
                if members:
                    first_member = members[0].name.split("/")[0]
                    extracted_dir = install_path / first_member
                    if extracted_dir.exists():
                        for item in extracted_dir.iterdir():
                            dest = install_path / item.name
                            if not dest.exists():
                                item.rename(dest)
                        extracted_dir.rmdir()

            browser_exe = install_path / "Browser" / "firefox"
            if browser_exe.exists():
                browser_exe.chmod(0o755)
            else:
                raise ValueError("Tor Browser installation incomplete")

            tmp_file.unlink()
            logger.info("Tor Browser installed to %s", install_path)
            return str(install_path)

        except Exception as e:
            if tmp_file.exists():
                tmp_file.unlink()
            raise ValueError(
                f"Failed to install Tor Browser automatically: {e}. "
                "Please install manually or set TOR_BROWSER_PATH."
            ) from e

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
            logger = logging.getLogger(__name__)
            logger.info(
                "Tor Browser not found at %s. Installing automatically...",
                tor_browser_path,
            )
            try:
                tor_browser_path = self._install_tor_browser(
                    self.tor_browser_path
                )
                self.tor_browser_path = tor_browser_path
            except ValueError as e:
                if "macOS" in str(e):
                    raise
                logger.error("Automatic installation failed: %s", e)
                raise ValueError(
                    f"Tor Browser not found and automatic installation "
                    f"failed: {e}. Please install manually or set "
                    "TOR_BROWSER_PATH environment variable."
                ) from e

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
        return driver  # type: ignore[no-any-return]

    def get_instance(self) -> Any:
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
