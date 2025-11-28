"""
Scraper service for web scraping operations using Tor Browser.
"""

import logging
import time
from typing import Any

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from app.core.browsers.tor import TorBrowser
from app.core.errors import ScrapingError
from app.serializers.scraper import ScrapeRequest, ScrapeResponse

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for web scraping operations."""

    def _initialize_browser(self, headless: bool):
        """
        Initialize Tor Browser.

        Args:
            headless: Run browser in headless mode

        Returns:
            WebDriver instance

        Raises:
            ValueError: If Tor Browser is not configured
            WebDriverException: If Tor Browser fails to initialize
        """
        browser = TorBrowser(
            headless=headless,
            multi_instances=True,
        )
        driver = browser.get_instance()
        logger.info("Tor Browser initialized successfully")
        return driver

    def _wait_for_page_load(self, driver, wait_time: int):
        """
        Wait for page to load completely.

        Args:
            driver: WebDriver instance
            wait_time: Time to wait in seconds
        """
        if wait_time > 0:
            time.sleep(wait_time)
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

    def _extract_title(self, driver) -> str | None:
        """Extract page title."""
        try:
            return driver.title
        except Exception:
            return None

    def _extract_text(self, driver) -> str | None:
        """Extract text content from page."""
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            return body.text
        except Exception:
            return None

    def _extract_html(self, driver) -> str | None:
        """Extract HTML content from page."""
        try:
            return driver.page_source
        except Exception:
            return None

    def _extract_links(self, driver) -> list[str]:
        """Extract all links from page."""
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            return [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
            ]
        except Exception:
            return []

    def _extract_images(self, driver) -> list[str]:
        """Extract all image URLs from page."""
        try:
            images = driver.find_elements(By.TAG_NAME, "img")
            return [
                img.get_attribute("src")
                for img in images
                if img.get_attribute("src")
            ]
        except Exception:
            return []

    def _extract_data(self, driver, request: ScrapeRequest) -> dict[str, Any]:
        """
        Extract all requested data from the page.

        Args:
            driver: WebDriver instance
            request: ScrapeRequest with extraction options

        Returns:
            Dictionary with extracted data
        """
        response_data: dict[str, Any] = {
            "url": str(request.url),
            "title": None,
            "text": None,
            "html": None,
            "links": [],
            "images": [],
            "metadata": {},
        }

        response_data["title"] = self._extract_title(driver)

        if request.extract_text:
            response_data["text"] = self._extract_text(driver)

        if request.extract_html:
            response_data["html"] = self._extract_html(driver)

        if request.extract_links:
            response_data["links"] = self._extract_links(driver)

        if request.extract_images:
            response_data["images"] = self._extract_images(driver)

        response_data["metadata"] = {
            "current_url": driver.current_url,
            "wait_time": request.wait_time,
            "headless": request.headless,
        }

        return response_data

    def scrape(
        self, request: ScrapeRequest
    ) -> ScrapeResponse:
        """
        Scrape a webpage using Tor Browser.

        Args:
            request: ScrapeRequest with scraping parameters

        Returns:
            ScrapeResponse with scraped data

        Raises:
            ValueError: If browser configuration is invalid
            WebDriverException: If browser fails to initialize
            TimeoutException: If page load times out
            ScrapingError: For other scraping errors
        """
        driver = None
        try:
            logger.info("Initializing browser for URL: %s", request.url)
            driver = self._initialize_browser(request.headless)

            driver.get(str(request.url))
            self._wait_for_page_load(driver, request.wait_time)

            response_data = self._extract_data(driver, request)
            return ScrapeResponse(**response_data)

        except ValueError as e:
            logger.error("Configuration error: %s", e, exc_info=True)
            raise
        except TimeoutException as e:
            logger.error("Page load timeout: %s", e, exc_info=True)
            raise
        except WebDriverException as e:
            logger.error("Browser error: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Scraping error: %s", e, exc_info=True)
            raise ScrapingError(f"Scraping error: {str(e)}") from e
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
