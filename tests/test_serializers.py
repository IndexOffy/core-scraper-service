"""Tests for serializers."""

import unittest

from pydantic import ValidationError

from app.serializers.scraper import ScrapeRequest, ScrapeResponse


class TestScrapeRequest(unittest.TestCase):
    """Test ScrapeRequest serializer."""

    def test_valid_request_defaults(self):
        """Test valid request with default values."""
        request = ScrapeRequest(url="https://example.com")
        self.assertEqual(str(request.url), "https://example.com/")
        self.assertEqual(request.browser_type, "tor")
        self.assertEqual(request.wait_time, 5)
        self.assertTrue(request.headless)
        self.assertTrue(request.extract_text)
        self.assertFalse(request.extract_html)

    def test_valid_request_custom_values(self):
        """Test valid request with custom values."""
        request = ScrapeRequest(
            url="https://example.com",
            browser_type="chrome",
            wait_time=10,
            headless=False,
            extract_html=True,
            extract_links=True,
        )
        self.assertEqual(request.browser_type, "chrome")
        self.assertEqual(request.wait_time, 10)
        self.assertFalse(request.headless)
        self.assertTrue(request.extract_html)
        self.assertTrue(request.extract_links)

    def test_invalid_browser_type(self):
        """Test invalid browser type raises ValidationError."""
        with self.assertRaises(ValidationError):
            ScrapeRequest(url="https://example.com", browser_type="firefox")

    def test_invalid_wait_time_too_low(self):
        """Test wait_time below minimum raises ValidationError."""
        with self.assertRaises(ValidationError):
            ScrapeRequest(url="https://example.com", wait_time=-1)

    def test_invalid_wait_time_too_high(self):
        """Test wait_time above maximum raises ValidationError."""
        with self.assertRaises(ValidationError):
            ScrapeRequest(url="https://example.com", wait_time=61)

    def test_invalid_url(self):
        """Test invalid URL raises ValidationError."""
        with self.assertRaises(ValidationError):
            ScrapeRequest(url="not-a-url")


class TestScrapeResponse(unittest.TestCase):
    """Test ScrapeResponse serializer."""

    def test_valid_response_minimal(self):
        """Test valid response with minimal data."""
        response = ScrapeResponse(
            url="https://example.com",
            title="Example",
        )
        self.assertEqual(response.url, "https://example.com")
        self.assertEqual(response.title, "Example")
        self.assertIsNone(response.text)
        self.assertIsNone(response.html)
        self.assertEqual(response.links, [])
        self.assertEqual(response.images, [])

    def test_valid_response_full(self):
        """Test valid response with all fields."""
        response = ScrapeResponse(
            url="https://example.com",
            title="Example",
            text="Some text",
            html="<html></html>",
            links=["https://example.com/link1"],
            images=["https://example.com/image1.jpg"],
            metadata={"key": "value"},
        )
        self.assertEqual(response.url, "https://example.com")
        self.assertEqual(response.title, "Example")
        self.assertEqual(response.text, "Some text")
        self.assertEqual(response.html, "<html></html>")
        self.assertEqual(len(response.links), 1)
        self.assertEqual(len(response.images), 1)
        self.assertEqual(response.metadata["key"], "value")

    def test_response_defaults(self):
        """Test response with default values."""
        response = ScrapeResponse(url="https://example.com")
        self.assertEqual(response.links, [])
        self.assertEqual(response.images, [])
        self.assertEqual(response.metadata, {})
