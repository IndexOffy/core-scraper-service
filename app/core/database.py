"""
This module contains the database configuration.
"""

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

from app.core.settings import settings

is_sqlite = settings.database_url.startswith("sqlite")

pool_config: dict[str, Any] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
}

if settings.is_lambda:
    pool_config.update(
        {
            "pool_size": 2,
            "max_overflow": 5,
            "pool_recycle": 3600,
        }
    )

if is_sqlite:
    pool_config = {
        "pool_pre_ping": True,
        "poolclass": None,
    }
else:
    pool_config.update(
        {
            "echo": False,
            "pool_reset_on_return": "commit",
        }
    )

connect_args = {}
if is_sqlite:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    url=settings.database_url,
    connect_args=connect_args,
    **pool_config,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Database:
    """Database connection and session management."""

    @classmethod
    def get_db(cls):
        """Independent database session/connection per request."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
