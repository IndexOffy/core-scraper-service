"""
Dataclass Module
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from bs4 import BeautifulSoup


@dataclass
class DataInput:

    url: str
    title: Optional[str] = field(default=None)
    page_source: Optional[str] = field(default=None)
    print_page: Optional[str] = field(default=None)
    cookies: Optional[List[Dict]] = field(default=None)
