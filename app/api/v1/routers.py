"""Routers"""

from fastapi import APIRouter

from app.api.v1.endpoints import router_scraper

v1 = APIRouter()

v1.include_router(router_scraper, tags=["Scraper"])
