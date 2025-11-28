"""Tests for settings configuration."""

import os
import unittest
from unittest.mock import patch

from app.core.settings import Settings, get_settings


class TestSettings(unittest.TestCase):
    """Test Settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        self.assertEqual(settings.scope, "development")
        self.assertEqual(settings.database_url, "sqlite:///./sql_app.db")
        self.assertEqual(settings.api_version, "0.1.0")
        self.assertEqual(settings.api_v1_prefix, "/api/v1")
        self.assertEqual(settings.cors_origins, ["*"])

    def test_is_development(self):
        """Test is_development property."""
        settings = Settings(scope="development")
        self.assertTrue(settings.is_development)

        settings = Settings(scope="production")
        self.assertFalse(settings.is_development)

    def test_is_lambda(self):
        """Test is_lambda property."""
        settings = Settings()
        self.assertFalse(settings.is_lambda)

        env_dict = {"AWS_LAMBDA_FUNCTION_NAME": "test-function"}
        with patch.dict(os.environ, env_dict):
            get_settings.cache_clear()
            settings = Settings()
            self.assertTrue(settings.is_lambda)
            get_settings.cache_clear()

    def test_cors_origins_json_string(self):
        """Test CORS origins parsing from JSON string."""
        cors_json = '["https://example.com", "https://test.com"]'
        settings = Settings(cors_origins=cors_json)
        self.assertEqual(len(settings.cors_origins), 2)
        self.assertIn("https://example.com", settings.cors_origins)
        self.assertIn("https://test.com", settings.cors_origins)

    def test_cors_origins_comma_separated(self):
        """Test CORS origins parsing from comma-separated string."""
        cors_str = "https://example.com,https://test.com"
        settings = Settings(cors_origins=cors_str)
        self.assertEqual(len(settings.cors_origins), 2)
        self.assertIn("https://example.com", settings.cors_origins)
        self.assertIn("https://test.com", settings.cors_origins)

    def test_cors_origins_list(self):
        """Test CORS origins as list."""
        cors_list = ["https://example.com"]
        settings = Settings(cors_origins=cors_list)
        self.assertEqual(settings.cors_origins, cors_list)

    def test_get_settings_cached(self):
        """Test get_settings returns cached instance."""
        get_settings.cache_clear()
        settings1 = get_settings()
        settings2 = get_settings()
        self.assertIs(settings1, settings2)
        get_settings.cache_clear()
