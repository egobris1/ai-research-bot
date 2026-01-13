"""Research Director agent factory."""

from crewai import LLM

from research_bot.agents.base import AgentFactory


class DirectorAgentFactory(AgentFactory):
    """Factory for creating Research Director agents."""

    def __init__(self, llm: LLM) -> None:
        super().__init__(llm)

    @property
    def role(self) -> str:
        return "Research Director"

    @property
    def goal(self) -> str:
        return "Ensure research quality, completeness, and accuracy"

    @property
    def backstory(self) -> str:
        return (
            "You are a research director who ensures all research meets high standards. "
            "You evaluate completeness, verify accuracy, identify gaps, and synthesize "
            "findings into clear conclusions. You are critical but constructive."
        )
