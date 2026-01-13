"""Review task factory."""

from research_bot.tasks.base import TaskFactory


class ReviewTaskFactory(TaskFactory):
    """Factory for creating quality review tasks."""

    @property
    def description_template(self) -> str:
        return (
            "Review all research findings for: {topic}\n\n"
            "Evaluate:\n"
            "1. Completeness - Are all key questions answered?\n"
            "2. Accuracy - Are sources reliable?\n"
            "3. Relevance - Does everything relate to the topic?\n"
            "4. Gaps - What's missing?\n\n"
            "Provide a quality assessment and synthesize the key findings."
        )

    @property
    def expected_output(self) -> str:
        return (
            "Quality review with:\n"
            "- Assessment of research completeness (1-10)\n"
            "- Key verified findings\n"
            "- Any gaps or concerns\n"
            "- Synthesized main conclusions"
        )
