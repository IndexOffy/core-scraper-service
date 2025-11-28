"""
Settings configuration for the FastAPI application.
"""

import json
import os
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    scope: Literal["development", "production", "test"] = Field(
        default="development",
        description="Application environment scope",
    )

    database_url: str = Field(
        default="sqlite:///./sql_app.db",
        description="Database connection URL",
    )

    api_version: str = Field(default="0.1.0", description="API version")

    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")

    cors_origins: list[str] = Field(
        default=["*"], description="Allowed CORS origins"
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, cors_origins_value):
        """
        Parse CORS origins from JSON string or comma-separated string.
        """
        if isinstance(cors_origins_value, str):
            try:
                return json.loads(cors_origins_value)
            except json.JSONDecodeError:
                return [
                    origin.strip()
                    for origin in cors_origins_value.split(",")
                    if origin.strip()
                ]
        return cors_origins_value

    cors_allow_methods: list[str] = Field(
        default=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
        ],
        description="Allowed HTTP methods for CORS",
    )

    cors_allow_headers: list[str] = Field(
        default=["Content-Type"],
        description="Allowed headers for CORS",
    )

    @model_validator(mode="before")
    @classmethod
    def remove_empty_strings(
        cls, data: dict | list | None
    ) -> dict | list | None:
        """Remove empty string values to allow defaults to be used."""
        if isinstance(data, dict):
            return {
                k: v for k, v in data.items() if v != "" and v is not None
            }
        return data

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.scope == "development"

    @property
    def is_lambda(self) -> bool:
        """Check if running on AWS Lambda."""
        return (
            os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
        )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This function uses lru_cache to ensure only one instance is created.
    """
    return Settings()


settings = get_settings()
