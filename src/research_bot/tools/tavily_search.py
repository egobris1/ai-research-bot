"""Tavily web search tool for research."""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

from research_bot.config.settings import Settings


class TavilySearchInput(BaseModel):
    """Input schema for Tavily search."""

    query: str = Field(..., description="The search query to execute")
    max_results: int = Field(5, ge=1, le=20, description="Maximum number of results")


class TavilySearchTool(BaseTool):
    """Tool for searching the web using Tavily API."""

    name: str = "tavily_web_search"
    description: str = (
        "Search the web for information on a topic. Returns relevant web pages "
        "with titles, URLs, and content summaries. Use this for broad research."
    )
    args_schema: Type[BaseModel] = TavilySearchInput

    _client: TavilyClient
    _settings: Settings

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._client = TavilyClient(api_key=settings.tavily_api_key)
        self._settings = settings

    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute Tavily search and return formatted results."""
        try:
            response = self._client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
            )

            results = []
            if response.get("answer"):
                results.append(f"Summary: {response['answer']}\n")

            for idx, result in enumerate(response.get("results", []), 1):
                results.append(
                    f"[{idx}] {result['title']}\n"
                    f"    URL: {result['url']}\n"
                    f"    {result.get('content', 'No content available')[:500]}\n"
                )

            return "\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Search error: {e}"
