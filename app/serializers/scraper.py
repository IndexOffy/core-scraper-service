"""
Serializers for Scraper operations.
"""

from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class ScrapeRequest(BaseModel):
    """Request schema for scraping operation."""

    url: HttpUrl = Field(..., description="URL to scrape")
    wait_time: int = Field(
        default=5,
        ge=0,
        le=60,
        description="Wait time in seconds for page to load",
    )
    headless: bool = Field(
        default=True, description="Run browser in headless mode"
    )
    extract_text: bool = Field(
        default=True, description="Extract text content from page"
    )
    extract_html: bool = Field(
        default=False, description="Extract full HTML content"
    )
    extract_links: bool = Field(
        default=False, description="Extract all links from page"
    )
    extract_images: bool = Field(
        default=False, description="Extract all image URLs from page"
    )


class ScrapeResponse(BaseModel):
    """Response schema for scraping operation."""

    url: str = Field(..., description="Scraped URL")
    title: str | None = Field(None, description="Page title")
    text: str | None = Field(None, description="Extracted text content")
    html: str | None = Field(None, description="Extracted HTML content")
    links: list[str] = Field(
        default_factory=list, description="Extracted links"
    )
    images: list[str] = Field(
        default_factory=list, description="Extracted image URLs"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
