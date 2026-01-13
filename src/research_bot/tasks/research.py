"""Research task factory."""

from research_bot.tasks.base import TaskFactory


class ResearchTaskFactory(TaskFactory):
    """Factory for creating deep research tasks."""

    @property
    def description_template(self) -> str:
        return (
            "Conduct deep research on: {topic}\n\n"
            "Focus on:\n"
            "- Authoritative and primary sources\n"
            "- Technical details and specifications\n"
            "- Historical context and background\n"
            "- Expert opinions and analysis\n\n"
            "Use the research plan as your guide. Search thoroughly and extract detailed information."
        )

    @property
    def expected_output(self) -> str:
        return (
            "Comprehensive research findings with:\n"
            "- Detailed facts and data\n"
            "- Source URLs for all claims\n"
            "- Key quotes from authoritative sources\n"
            "- Any conflicting information found"
        )
