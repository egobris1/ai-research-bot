"""Web page extraction tool using scrape.do API."""

import urllib.parse
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from research_bot.config.settings import Settings


class ScrapeInput(BaseModel):
    """Input schema for scrape.do tool."""

    url: str = Field(..., description="The URL to scrape and extract content from")
    render: bool = Field(True, description="Whether to render JavaScript (default: True)")


class ScrapeTool(BaseTool):
    """Tool for extracting content from web pages using scrape.do."""

    name: str = "web_page_extractor"
    description: str = (
        "Extract the full content from a specific web page URL. "
        "Use this when you have a specific URL and need its full content."
    )
    args_schema: Type[BaseModel] = ScrapeInput

    _api_key: str
    _base_url: str = "https://api.scrape.do/"

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._api_key = settings.scrape_do_api_key

    def _run(self, url: str, render: bool = True) -> str:
        """Extract content from URL using scrape.do API."""
        try:
            encoded_url = urllib.parse.quote_plus(url)
            api_url = (
                f"{self._base_url}?token={self._api_key}"
                f"&url={encoded_url}&render={str(render).lower()}"
            )

            response = requests.get(api_url, timeout=30)
            response.raise_for_status()

            content = response.text[:10000]
            return f"Content from {url}:\n\n{content}"
        except requests.RequestException as e:
            return f"Extraction error: {e}"
