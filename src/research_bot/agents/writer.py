"""Report Writer agent factory."""

from crewai import LLM

from research_bot.agents.base import AgentFactory


class WriterAgentFactory(AgentFactory):
    """Factory for creating Report Writer agents."""

    def __init__(self, llm: LLM) -> None:
        super().__init__(llm)

    @property
    def role(self) -> str:
        return "Report Writer"

    @property
    def goal(self) -> str:
        return "Create polished, professional research reports"

    @property
    def backstory(self) -> str:
        return (
            "You are a professional technical writer who creates executive-quality reports. "
            "Your reports are well-structured, clearly written, properly cited, and "
            "visually organized with appropriate headers and formatting."
        )
