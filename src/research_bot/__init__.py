"""
Research Bot - Multi-Agent AI Research System.

A CrewAI-based research system following SOLID principles:
- S: Single Responsibility - Each module has one purpose
- O: Open/Closed - Extensible via factories and protocols
- L: Liskov Substitution - All factories are interchangeable
- I: Interface Segregation - Minimal, focused interfaces
- D: Dependency Inversion - Depends on abstractions

Architecture:
- agents/     - Agent factory implementations (Factory Pattern)
- tasks/      - Task factory implementations (Factory Pattern)
- crews/      - Crew builder (Builder Pattern)
- models/     - Pydantic data models
- tools/      - Research tool implementations
- services/   - Orchestration layer (Strategy Pattern)
- config/     - Settings management
"""

__version__ = "0.1.0"
__author__ = "Research Bot Team"

from research_bot.config import Settings
from research_bot.services import ResearchService

__all__ = [
    "Settings",
    "ResearchService",
    "__version__",
]
