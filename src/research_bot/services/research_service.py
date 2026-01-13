"""Research service - Orchestration layer for multi-agent research system."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Protocol

from crewai import LLM
from crewai.tools import BaseTool

from research_bot.config.settings import Settings
from research_bot.crews import ResearchCrewBuilder
from research_bot.models import ReportMetadata, ResearchReport
from research_bot.tools import ScrapeTool, TavilySearchTool

logger = logging.getLogger(__name__)


class ToolProvider(Protocol):
    """Protocol for tool providers - Interface Segregation Principle."""

    def get_tools(self) -> List[BaseTool]:
        """Return list of tools."""
        ...


class DefaultToolProvider:
    """
    Default tool provider implementation.

    Follows:
    - Single Responsibility: Only provides tools
    - Dependency Inversion: Depends on Settings abstraction
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_tools(self) -> List[BaseTool]:
        """Create and return research tools."""
        return [
            TavilySearchTool(self._settings),
            ScrapeTool(self._settings),
        ]


class ResearchService:
    """
    Orchestration service for the research pipeline.

    Follows:
    - Single Responsibility: Orchestrates research execution
    - Open/Closed: Extensible via tool providers
    - Dependency Inversion: Depends on abstractions (Settings, ToolProvider)

    Uses:
    - Builder Pattern: For crew construction
    - Strategy Pattern: For tool provision
    """

    def __init__(
        self,
        settings: Settings,
        tool_provider: ToolProvider | None = None,
    ) -> None:
        """
        Initialize research service.

        Args:
            settings: Application settings (dependency injection).
            tool_provider: Optional custom tool provider (strategy pattern).
        """
        self._settings = settings
        self._tool_provider = tool_provider or DefaultToolProvider(settings)
        self._llm = self._create_llm()

    def _create_llm(self) -> LLM:
        """Create LLM instance from settings."""
        return LLM(
            model=self._settings.llm_model,
            temperature=self._settings.llm_temperature,
        )

    def _print_header(self, topic: str) -> None:
        """Print execution header."""
        print(f"\n{'='*60}")
        print("🔬 RESEARCH BOT - Multi-Agent Research System")
        print(f"{'='*60}")
        print(f"📋 Topic: {topic}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")

    def _print_phases(self) -> None:
        """Print phase information."""
        phases = [
            ("📝", "Phase 1", "Research Planning"),
            ("🔍", "Phase 2", "Deep Research (Lead Researcher)"),
            ("📊", "Phase 3", "Industry Analysis (Market Analyst)"),
            ("✅", "Phase 4", "Quality Review (Director)"),
            ("📄", "Phase 5", "Report Generation (Writer)"),
        ]
        for emoji, phase, description in phases:
            print(f"{emoji} {phase}: {description}...")

    def _print_footer(self, output_file: str) -> None:
        """Print execution footer."""
        print(f"\n{'='*60}")
        print("✅ Research Complete!")
        print(f"📄 Report saved to: {output_file}")
        print(f"{'='*60}\n")

    def execute_research(
        self,
        topic: str,
        output_file: str = "research_report.md",
    ) -> str:
        """
        Execute comprehensive research on a topic.

        Args:
            topic: The research topic/query.
            output_file: Path for the output report file.

        Returns:
            The final markdown report content.
        """
        self._print_header(topic)
        self._print_phases()

        # Build crew using Builder Pattern
        crew = (
            ResearchCrewBuilder(self._llm)
            .with_tools(self._tool_provider.get_tools())
            .with_max_iterations(self._settings.max_iterations)
            .with_verbose(self._settings.crew_verbose)
            .with_output_file(output_file)
            .for_topic(topic)
            .build()
        )

        print(f"\n{'='*60}")
        print("🚀 Executing Research Pipeline...")
        print(f"{'='*60}\n")

        # Execute crew
        result = crew.kickoff()
        result_str = str(result)

        # Ensure file is written
        output_path = Path(output_file)
        if not output_path.exists():
            output_path.write_text(result_str)

        # Create report model
        report = ResearchReport(
            metadata=ReportMetadata(
                title=f"Research Report: {topic}",
                topic=topic,
            ),
            raw_content=result_str,
        )

        logger.info(
            "Research completed",
            extra={
                "topic": topic,
                "output_file": output_file,
                "report_length": len(result_str),
            },
        )

        self._print_footer(output_file)

        return report.raw_content or result_str
