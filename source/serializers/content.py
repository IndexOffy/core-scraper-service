from typing import List

from pydantic import BaseModel, Field


class Content(BaseModel):

    url: str = Field(description="Main URL")
    title: str = Field(default=None, description="Page Title")
    author: str = Field(default=None, description="Author Name")
    source: str = Field(default=None, description="Page Source")
    hrefs: List[str] = Field(default=[], description="References")
    subpages: List[str] = Field(default=[], description="Subpages")
