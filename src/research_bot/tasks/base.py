"""Base task factory - Abstract Factory Pattern."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from crewai import Agent, Task


class TaskFactory(ABC):
    """
    Abstract factory for creating CrewAI tasks.

    Follows:
    - Single Responsibility: Only creates tasks
    - Open/Closed: Extend for new task types without modification
    - Liskov Substitution: All factories are interchangeable
    - Interface Segregation: Minimal required interface
    """

    def __init__(self, topic: str) -> None:
        """Initialize factory with research topic."""
        self._topic = topic

    @property
    def topic(self) -> str:
        """The research topic."""
        return self._topic

    @property
    def current_date(self) -> str:
        """Current date formatted for task context."""
        return datetime.now().strftime("%Y-%m-%d")

    @property
    @abstractmethod
    def description_template(self) -> str:
        """Task description template with {topic} and {date} placeholders."""
        ...

    @property
    @abstractmethod
    def expected_output(self) -> str:
        """Expected output description."""
        ...

    @property
    def output_file(self) -> Optional[str]:
        """Optional output file path. Override to specify."""
        return None

    def _format_description(self) -> str:
        """Format description with topic and date."""
        return self.description_template.format(
            topic=self._topic,
            date=self.current_date,
        )

    def create(
        self,
        agent: Agent,
        context: Optional[List[Task]] = None,
    ) -> Task:
        """
        Create and return a configured CrewAI Task.

        Args:
            agent: The agent assigned to this task.
            context: Optional list of tasks that provide context.

        Returns:
            Configured Task instance.
        """
        task_kwargs = {
            "description": self._format_description(),
            "expected_output": self.expected_output,
            "agent": agent,
        }

        if context:
            task_kwargs["context"] = context

        if self.output_file:
            task_kwargs["output_file"] = self.output_file

        return Task(**task_kwargs)
