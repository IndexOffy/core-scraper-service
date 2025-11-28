"""Scraper endpoint for web scraping operations"""

import logging

from fastapi import APIRouter, HTTPException, status
from selenium.common.exceptions import TimeoutException, WebDriverException

from app.core.errors import ScrapingError
from app.serializers.scraper import ScrapeRequest, ScrapeResponse
from app.services.scraper_service import ScraperService

logger = logging.getLogger(__name__)
router_scraper = APIRouter()


@router_scraper.post(
    "/scrape",
    response_model=ScrapeResponse,
    status_code=status.HTTP_200_OK,
)
def scrape_page(request: ScrapeRequest):
    """
    """
    try:
        service = ScraperService()
        result = service.scrape(request)
        return result
    except ValueError as error:
        logger.error("Configuration error: %s", error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuration error: {str(error)}",
        ) from error
    except TimeoutException as error:
        logger.error("Page load timeout: %s", error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Page load timeout: {str(error)}",
        ) from error
    except WebDriverException as error:
        logger.error("Browser error: %s", error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Browser error: {str(error)}",
        ) from error
    except ScrapingError as error:
        logger.error("Scraping failed: %s", error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scraping failed: {str(error)}",
        ) from error
    except Exception as error:
        logger.error("Unexpected error: %s", error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(error)}",
        ) from error
