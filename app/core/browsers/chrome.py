"""Chrome Browser Module."""

import os
import shutil
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from app.core.browsers.abc import Browser


class Chrome(Browser):
    """Chrome browser implementation."""

    def _set_executable(self) -> None:
        lambda_path = "/var/task/chromedriver"

        if os.path.exists(lambda_path):
            self.executable = lambda_path
            return

        chromedriver_path = shutil.which("chromedriver")
        if chromedriver_path:
            self.executable = chromedriver_path
            return

        self.executable = None

    def _set_options(self) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if self.headless:
            options.add_argument("--headless")

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"],
        )
        options.add_experimental_option(
            "useAutomationExtension",
            False,
        )

        self.options = options

    def get_instance(self) -> Any:
        """Get browser driver instance."""

        def new_driver() -> Any:
            if self.executable:
                driver = webdriver.Chrome(
                    service=Service(self.executable),
                    options=self.options,
                )
            else:
                driver = webdriver.Chrome(options=self.options)
            driver.implicitly_wait(5)
            return driver

        if self.multi_instances:
            return new_driver()

        if not self.instance:
            self.instance = new_driver()

        return self.instance
