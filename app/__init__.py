"""
This module contains the FastAPI application.
"""

__version__ = "0.1.0"

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ping import ping_router
from app.api.v1 import api_router as v1_router
from app.core.settings import settings


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    docs_url = "/docs" if settings.is_development else None
    openapi_url = "/openapi.json" if settings.is_development else None

    new_app = FastAPI(
        title="dotflow",
        description="dotflow API",
        contact={
            "name": "Fernando Celmer",
            "email": "email@fernandocelmer.com",
        },
        version=settings.api_version,
        debug=settings.is_development,
        docs_url=docs_url,
        openapi_url=openapi_url,
    )

    if settings.is_development:
        cors_origins = ["*"]
    else:
        cors_origins = (
            settings.cors_origins
            if "*" not in settings.cors_origins
            else ["*"]
        )

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
        expose_headers=[],
        max_age=86400,
    )

    new_app.include_router(
        v1_router,
        prefix=settings.api_v1_prefix,
    )
    new_app.include_router(ping_router, prefix="/ping")

    return new_app


app = create_app()
