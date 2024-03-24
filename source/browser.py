"""
Browser Module
"""

from abc import ABC, abstractmethod

from domain import Domain

from selenium import webdriver
from get_gecko_driver import GetGeckoDriver
from selenium.webdriver.chrome.service import Service
from tbselenium.tbdriver import TorBrowserDriver
from webdriver_manager.chrome import ChromeDriverManager


class Browser(ABC):

    executable = None
    options = None
    instance = None

    def __init__(
            self,
            headless: bool = True,
            multi_instances: bool = False
        ) -> None:
        self.headless = headless
        self.multi_instances = multi_instances

        self._set_executable()
        self._set_options()

    @abstractmethod
    def _set_executable(self) -> None:
        pass

    @abstractmethod
    def _set_options(self) -> None:
        pass

    @abstractmethod
    def get_instance(self) -> None:
        pass


class BrowserChrome(Browser):

    def _set_executable(self) -> None:
        self.executable = ChromeDriverManager().install()
 
    def _set_options(self) -> None:
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless")

        self.options = options

    def get_instance(self) -> None:
        def new_driver():
            driver = webdriver.Chrome(
                service=Service(self.executable),
                options=self.options
            )
            driver.implicitly_wait(5)
            return driver

        if self.multi_instances:
            return new_driver()

        if not self.instance:
            self.instance = new_driver()

        return self.instance


# TODO: In Progress
class BrowserTor(Browser):

    def _set_executable(self) -> None:
        driver = GetGeckoDriver()
        self.executable = driver.install()
 
    def _set_options(self) -> None:
        options = webdriver.FirefoxOptions()
        options.headless = self.headless

        self.options = options

    def get_instance(self) -> None:
        def new_driver():
            driver = TorBrowserDriver(
                self.executable,
                options=self.options
            )
            return driver

        if self.multi_instances:
            return new_driver()

        if not self.instance:
            self.instance = new_driver()

        return self.instance
