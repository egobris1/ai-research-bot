"""Planning task factory."""

from research_bot.tasks.base import TaskFactory


class PlanningTaskFactory(TaskFactory):
    """Factory for creating research planning tasks."""

    @property
    def description_template(self) -> str:
        return (
            "Analyze this research topic and create a research plan:\n\n"
            "TOPIC: {topic}\n"
            "TODAY'S DATE: {date}\n\n"
            "Create a structured research plan with:\n"
            "1. Key questions that need to be answered\n"
            "2. Important subtopics to investigate\n"
            "3. Types of sources to consult (academic, industry, news)\n"
            "4. Potential challenges or areas needing clarification\n\n"
            "Note: Focus on the most current and recent information available as of {date}."
        )

    @property
    def expected_output(self) -> str:
        return (
            "A research plan with:\n"
            "- 3-5 key research questions\n"
            "- Priority subtopics\n"
            "- Recommended source types"
        )
