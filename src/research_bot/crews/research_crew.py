"""Research crew builder - Builder Pattern implementation."""

from typing import List, Optional

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool

from research_bot.agents import (
    AnalystAgentFactory,
    DirectorAgentFactory,
    PlannerAgentFactory,
    ResearcherAgentFactory,
    WriterAgentFactory,
)
from research_bot.tasks import (
    AnalysisTaskFactory,
    PlanningTaskFactory,
    ReportTaskFactory,
    ResearchTaskFactory,
    ReviewTaskFactory,
)


class ResearchCrewBuilder:
    """
    Builder for constructing research crews.

    Implements Builder Pattern for flexible crew assembly.

    Follows:
    - Single Responsibility: Only builds crews
    - Open/Closed: New agent/task types via composition
    - Dependency Inversion: Depends on factory abstractions
    """

    def __init__(self, llm: LLM) -> None:
        """Initialize builder with LLM dependency."""
        self._llm = llm
        self._tools: List[BaseTool] = []
        self._max_iterations: Optional[int] = None
        self._verbose: bool = True
        self._output_file: str = "research_report.md"
        self._topic: Optional[str] = None

        # Built components
        self._agents: List[Agent] = []
        self._tasks: List[Task] = []

    def with_tools(self, tools: List[BaseTool]) -> "ResearchCrewBuilder":
        """Set research tools for agents."""
        self._tools = tools
        return self

    def with_max_iterations(self, max_iter: int) -> "ResearchCrewBuilder":
        """Set maximum iterations for research agents."""
        self._max_iterations = max_iter
        return self

    def with_verbose(self, verbose: bool) -> "ResearchCrewBuilder":
        """Set verbose output mode."""
        self._verbose = verbose
        return self

    def with_output_file(self, output_file: str) -> "ResearchCrewBuilder":
        """Set output file path for report."""
        self._output_file = output_file
        return self

    def for_topic(self, topic: str) -> "ResearchCrewBuilder":
        """Set the research topic."""
        self._topic = topic
        return self

    def _build_agents(self) -> None:
        """Build all agents using factories."""
        # Planner agent (no tools)
        planner_factory = PlannerAgentFactory(self._llm)
        planner = planner_factory.create()

        # Lead researcher (with tools)
        researcher_factory = ResearcherAgentFactory(
            self._llm,
            research_tools=self._tools,
            max_iterations=self._max_iterations,
        )
        researcher = researcher_factory.create()

        # Market analyst (with tools)
        analyst_factory = AnalystAgentFactory(
            self._llm,
            research_tools=self._tools,
            max_iterations=self._max_iterations,
        )
        analyst = analyst_factory.create()

        # Director (no tools)
        director_factory = DirectorAgentFactory(self._llm)
        director = director_factory.create()

        # Writer (no tools)
        writer_factory = WriterAgentFactory(self._llm)
        writer = writer_factory.create()

        self._agents = [planner, researcher, analyst, director, writer]

    def _build_tasks(self) -> None:
        """Build all tasks using factories with proper context chaining."""
        if not self._topic:
            raise ValueError("Topic must be set before building tasks")

        if len(self._agents) != 5:
            raise ValueError("Agents must be built before tasks")

        planner, researcher, analyst, director, writer = self._agents

        # Task 1: Planning
        planning_factory = PlanningTaskFactory(self._topic)
        planning_task = planning_factory.create(agent=planner)

        # Task 2: Research (depends on planning)
        research_factory = ResearchTaskFactory(self._topic)
        research_task = research_factory.create(
            agent=researcher,
            context=[planning_task],
        )

        # Task 3: Analysis (depends on planning + research)
        analysis_factory = AnalysisTaskFactory(self._topic)
        analysis_task = analysis_factory.create(
            agent=analyst,
            context=[planning_task, research_task],
        )

        # Task 4: Review (depends on all previous)
        review_factory = ReviewTaskFactory(self._topic)
        review_task = review_factory.create(
            agent=director,
            context=[planning_task, research_task, analysis_task],
        )

        # Task 5: Report (depends on all previous)
        report_factory = ReportTaskFactory(self._topic, self._output_file)
        report_task = report_factory.create(
            agent=writer,
            context=[planning_task, research_task, analysis_task, review_task],
        )

        self._tasks = [planning_task, research_task, analysis_task, review_task, report_task]

    def build(self) -> Crew:
        """
        Build and return the complete research crew.

        Returns:
            Configured Crew ready for execution.

        Raises:
            ValueError: If topic is not set.
        """
        if not self._topic:
            raise ValueError("Topic must be set using for_topic() before building")

        self._build_agents()
        self._build_tasks()

        return Crew(
            agents=self._agents,
            tasks=self._tasks,
            process=Process.sequential,
            verbose=self._verbose,
        )
