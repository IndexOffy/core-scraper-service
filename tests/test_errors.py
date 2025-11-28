"""Tests for custom errors."""

import unittest

from app.core.errors import ScrapingError


class TestScrapingError(unittest.TestCase):
    """Test ScrapingError exception."""

    def test_scraping_error_creation(self):
        """Test ScrapingError can be created."""
        error = ScrapingError("Test error message")
        self.assertEqual(str(error), "Test error message")
        self.assertIsInstance(error, Exception)

    def test_scraping_error_raises(self):
        """Test ScrapingError can be raised."""
        with self.assertRaises(ScrapingError) as context:
            raise ScrapingError("Test error")
        self.assertEqual(str(context.exception), "Test error")

    def test_scraping_error_inheritance(self):
        """Test ScrapingError inherits from Exception."""
        error = ScrapingError("Test")
        self.assertIsInstance(error, Exception)
