"""Research Planner agent factory."""

from crewai import LLM

from research_bot.agents.base import AgentFactory


class PlannerAgentFactory(AgentFactory):
    """Factory for creating Research Planner agents."""

    def __init__(self, llm: LLM) -> None:
        super().__init__(llm)

    @property
    def role(self) -> str:
        return "Research Planner"

    @property
    def goal(self) -> str:
        return "Create structured research plans that ensure comprehensive coverage"

    @property
    def backstory(self) -> str:
        return (
            "You are a senior research strategist with expertise in breaking down "
            "complex topics into manageable research questions. You ensure no important "
            "angle is missed and prioritize the most critical areas of investigation."
        )
