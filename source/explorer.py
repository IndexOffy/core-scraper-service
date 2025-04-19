"""Explorer Module"""

from typing import List

from source.abc.browser import Browser
from source.data import DataInput


class Explorer:

    def __init__(
            self,
            data: List[DataInput],
            browser: Browser) -> None:
        self.data = data
        self.browser = browser

    def get(self):
        for _, resource in enumerate(self.data, start=1):
            try:
                driver = self.browser.get_instance()
                driver.get(resource.url)

                resource.title = driver.title
                resource.page_source = driver.page_source
                resource.print_page = driver.print_page()
                resource.cookies = driver.get_cookies()

            except Exception as error:
                print(error)
