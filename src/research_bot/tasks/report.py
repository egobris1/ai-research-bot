"""Report writing task factory."""

from typing import Optional

from research_bot.tasks.base import TaskFactory


class ReportTaskFactory(TaskFactory):
    """Factory for creating report writing tasks."""

    def __init__(self, topic: str, output_file: str = "research_report.md") -> None:
        super().__init__(topic)
        self._output_file = output_file

    @property
    def description_template(self) -> str:
        return (
            "Write a professional research report on: {topic}\n\n"
            "IMPORTANT: Today's date is {date}. Use this date in the report.\n\n"
            "Use all the research findings and quality review to create a comprehensive report.\n\n"
            "Report Structure:\n"
            "1. Title and Date (use {date} as the report date)\n"
            "2. Executive Summary (key findings in 2-3 paragraphs)\n"
            "3. Introduction (context and scope)\n"
            "4. Methodology (how research was conducted)\n"
            "5. Key Findings (organized by theme)\n"
            "6. Industry Analysis (market perspective)\n"
            "7. Conclusions and Implications\n"
            "8. References (all sources with URLs)\n\n"
            "Make it professional, well-organized, and cite all sources."
        )

    @property
    def expected_output(self) -> str:
        return (
            "A professional markdown report with all sections, "
            "proper formatting, citations, and a polished presentation."
        )

    @property
    def output_file(self) -> Optional[str]:
        return self._output_file
