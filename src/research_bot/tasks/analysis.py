"""Market analysis task factory."""

from research_bot.tasks.base import TaskFactory


class AnalysisTaskFactory(TaskFactory):
    """Factory for creating market/industry analysis tasks."""

    @property
    def description_template(self) -> str:
        return (
            "Analyze industry and market aspects of: {topic}\n\n"
            "Focus on:\n"
            "- Current trends and developments\n"
            "- Real-world applications and case studies\n"
            "- Market impact and business implications\n"
            "- Future outlook and predictions\n\n"
            "Complement the lead researcher's findings with practical perspectives."
        )

    @property
    def expected_output(self) -> str:
        return (
            "Industry analysis with:\n"
            "- Current market trends\n"
            "- Notable implementations/case studies\n"
            "- Business implications\n"
            "- Source URLs"
        )
