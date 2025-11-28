"""Browsers module"""

from app.core.browsers.abc import Browser
from app.core.browsers.chrome import Chrome
from app.core.browsers.tor import TorBrowser

__all__ = [
    "Browser",
    "Chrome",
    "TorBrowser",
]
