"""Market Analyst agent factory."""

from typing import List, Optional

from crewai import LLM
from crewai.tools import BaseTool

from research_bot.agents.base import AgentFactory


class AnalystAgentFactory(AgentFactory):
    """Factory for creating Market Analyst agents with research tools."""

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
        return "Market Analyst"

    @property
    def goal(self) -> str:
        return "Analyze industry trends, market impact, and real-world applications"

    @property
    def backstory(self) -> str:
        return (
            "You are a senior industry analyst who understands market dynamics, "
            "business implications, and real-world applications. You find case studies, "
            "track trends, and provide practical business perspectives."
        )

    @property
    def tools(self) -> List[BaseTool]:
        return self._research_tools

    @property
    def max_iter(self) -> Optional[int]:
        return self._max_iterations
