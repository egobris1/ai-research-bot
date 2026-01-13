"""Lead Researcher agent factory."""

from typing import List, Optional

from crewai import LLM
from crewai.tools import BaseTool

from research_bot.agents.base import AgentFactory


class ResearcherAgentFactory(AgentFactory):
    """Factory for creating Lead Researcher agents with research tools."""

    def __init__(
        self,
        llm: LLM,
        research_tools: List[BaseTool],
        max_iterations: Optional[int] = None,
    ) -> None:
        super().__init__(llm)
        self._research_tools = research_tools
        self._max_iterations = max_iterations

    @property
    def role(self) -> str:
        return "Lead Researcher"

    @property
    def goal(self) -> str:
        return "Conduct thorough research and gather authoritative information"

    @property
    def backstory(self) -> str:
        return (
            "You are a senior researcher with a PhD-level attention to detail. "
            "You excel at finding authoritative sources, extracting key information, "
            "and identifying the most important facts. You always cite your sources."
        )

    @property
    def tools(self) -> List[BaseTool]:
        return self._research_tools

    @property
    def max_iter(self) -> Optional[int]:
        return self._max_iterations
