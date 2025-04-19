"""Browser Module"""

import os

from selenium import webdriver
from get_gecko_driver import GetGeckoDriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.abc.browser import Browser


class Chrome(Browser):

    def _set_executable(self) -> None:
        get_driver = GetGeckoDriver()
        get_driver.install()
        base_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES.chromedriver" in base_path:
            return os.path.join(os.path.dirname(base_path), "chromedriver")
        return base_path

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
