"""Ping"""

from fastapi import APIRouter

ping_router = APIRouter(tags=["Ping"])


@ping_router.get("", include_in_schema=False)
def get_status():
    """Get status of messaging server."""
    return {"status": "it's alive"}
