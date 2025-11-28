"""
This module contains the main application.
"""

import os

import uvicorn

from app import create_app
from app.core.settings import settings

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        reload=settings.is_development,
    )
