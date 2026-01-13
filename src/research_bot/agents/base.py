"""Base agent factory - Abstract Factory Pattern."""

from abc import ABC, abstractmethod
from typing import List, Optional

from crewai import Agent, LLM
from crewai.tools import BaseTool


class AgentFactory(ABC):
    """
    Abstract factory for creating CrewAI agents.

    Follows:
    - Single Responsibility: Only creates agents
    - Open/Closed: Extend for new agent types without modification
    - Liskov Substitution: All factories are interchangeable
    - Dependency Inversion: Depends on LLM abstraction
    """

    def __init__(self, llm: LLM) -> None:
        """Initialize factory with LLM dependency injection."""
        self._llm = llm

    @property
    @abstractmethod
    def role(self) -> str:
        """Agent's role name."""
        ...

    @property
    @abstractmethod
    def goal(self) -> str:
        """Agent's primary goal."""
        ...

    @property
    @abstractmethod
    def backstory(self) -> str:
        """Agent's backstory for context."""
        ...

    @property
    def tools(self) -> List[BaseTool]:
        """Tools available to the agent. Override to provide tools."""
        return []

    @property
    def allow_delegation(self) -> bool:
        """Whether agent can delegate tasks. Default: False."""
        return False

    @property
    def verbose(self) -> bool:
        """Whether to show verbose output. Default: True."""
        return True

    @property
    def max_iter(self) -> Optional[int]:
        """Maximum iterations for agent. Default: None (use CrewAI default)."""
        return None

    def create(self) -> Agent:
        """
        Create and return a configured CrewAI Agent.

        Template Method Pattern: Uses abstract properties to build agent.
        """
        agent_kwargs = {
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "llm": self._llm,
            "tools": self.tools,
            "verbose": self.verbose,
            "allow_delegation": self.allow_delegation,
        }

        if self.max_iter is not None:
            agent_kwargs["max_iter"] = self.max_iter

        return Agent(**agent_kwargs)
