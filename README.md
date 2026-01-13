# Research Bot 🔬

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-orange.svg)](https://www.crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready multi-agent AI research system built with [CrewAI](https://www.crewai.com/). Five specialized agents collaborate through a sequential pipeline to produce comprehensive, citation-backed research reports.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Agents](#agents)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Design Patterns](#design-patterns)
- [Extending the System](#extending-the-system)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

Research Bot automates the research process by orchestrating multiple AI agents, each with specialized roles:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RESEARCH PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   📋 Topic Input                                                        │
│        │                                                                │
│        ▼                                                                │
│   ┌─────────────┐    ┌──────────────┐    ┌────────────────┐            │
│   │  Research   │───▶│    Lead      │───▶│    Market      │            │
│   │  Planner    │    │  Researcher  │    │    Analyst     │            │
│   └─────────────┘    └──────────────┘    └────────────────┘            │
│                             │                    │                      │
│                             ▼                    ▼                      │
│                      ┌─────────────────────────────┐                   │
│                      │    Research Director        │                   │
│                      │    (Quality Review)         │                   │
│                      └─────────────────────────────┘                   │
│                                    │                                    │
│                                    ▼                                    │
│                      ┌─────────────────────────────┐                   │
│                      │      Report Writer          │                   │
│                      └─────────────────────────────┘                   │
│                                    │                                    │
│                                    ▼                                    │
│                           📄 Markdown Report                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Features

- **Multi-Agent Collaboration**: Five specialized agents work in sequence, each building on previous outputs
- **Web Research**: Real-time web search via Tavily API with intelligent result ranking
- **Content Extraction**: JavaScript-rendered page scraping via scrape.do
- **Quality Assurance**: Dedicated review phase ensures completeness and accuracy
- **Professional Output**: Structured markdown reports with proper citations
- **Clean Architecture**: SOLID principles, design patterns, full type hints

---

## Architecture

The system follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Presentation Layer                         │
│                         (main.py CLI)                           │
├─────────────────────────────────────────────────────────────────┤
│                      Service Layer                              │
│                    (ResearchService)                            │
│              Orchestrates the research pipeline                 │
├─────────────────────────────────────────────────────────────────┤
│                      Builder Layer                              │
│                  (ResearchCrewBuilder)                          │
│            Assembles agents, tasks, and crew                    │
├─────────────────────────────────────────────────────────────────┤
│                      Factory Layer                              │
│              (AgentFactory / TaskFactory)                       │
│         Creates configured agents and tasks                     │
├─────────────────────────────────────────────────────────────────┤
│                      Domain Layer                               │
│                  (Pydantic Models)                              │
│      ResearchSource, ResearchFinding, ResearchReport            │
├─────────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                          │
│              (Tools: Tavily, scrape.do)                         │
│            External API integrations                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agents

| Agent | Role | Tools | Purpose |
|-------|------|-------|---------|
| **Research Planner** | Strategist | None | Analyzes topic, creates structured research plan with key questions |
| **Lead Researcher** | Investigator | Tavily, Scrape | Deep research on authoritative sources, technical details |
| **Market Analyst** | Analyst | Tavily, Scrape | Industry trends, case studies, business implications |
| **Research Director** | Reviewer | None | Quality assurance, completeness check, synthesis |
| **Report Writer** | Author | None | Professional markdown report with citations |

### Pipeline Phases

1. **Planning** - Break down topic into research questions and subtopics
2. **Deep Research** - Gather authoritative sources and technical information
3. **Industry Analysis** - Market trends, real-world applications, case studies
4. **Quality Review** - Verify completeness, accuracy, identify gaps
5. **Report Generation** - Synthesize findings into professional document

---

## Installation

### Prerequisites

- Python 3.10 - 3.13
- API Keys:
  - [Tavily](https://tavily.com/) - Web search API
  - [scrape.do](https://scrape.do/) - Web scraping API
  - [Google AI](https://makersuite.google.com/app/apikey) - Gemini LLM

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/research-bot.git
cd research-bot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

---

## Configuration

Create a `.env` file in the project root:

```env
# API Keys (required)
TAVILY_API_KEY=tvly-xxxxx
SCRAPE_DO_API_KEY=xxxxx
GOOGLE_API_KEY=xxxxx

# LLM Configuration
LLM_MODEL=gemini/gemini-2.0-flash
LLM_TEMPERATURE=0.3

# Agent-specific temperatures (creativity: 0.0-1.0)
DIRECTOR_TEMPERATURE=0.3
RESEARCHER_TEMPERATURE=0.5
WRITER_TEMPERATURE=0.7

# Research Configuration
MAX_ITERATIONS=5
MAX_RESEARCH_ROUNDS=3
MAX_SOURCES_PER_ROUND=10

# Logging
LOG_LEVEL=INFO
CREW_VERBOSE=true
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | `gemini/gemini-2.0-flash` | LLM model identifier |
| `LLM_TEMPERATURE` | `0.3` | Default creativity level |
| `MAX_ITERATIONS` | `5` | Max tool calls per agent |
| `CREW_VERBOSE` | `true` | Show agent reasoning |

---

## Usage

### Command Line

```bash
# Basic research
research-bot "Impact of artificial intelligence on healthcare"

# Custom output file
research-bot "Quantum computing market analysis" -o quantum_report.md

# Verbose mode (debug logging)
research-bot "Electric vehicle trends" --verbose

# Quiet mode (no banner)
research-bot "Renewable energy" --quiet
```

### Programmatic Usage

```python
from research_bot import Settings, ResearchService

# Initialize
settings = Settings()
service = ResearchService(settings)

# Execute research
report = service.execute_research(
    topic="The future of remote work",
    output_file="remote_work_report.md"
)

print(report)
```

### Custom Tool Provider

```python
from research_bot.services import ResearchService, ToolProvider
from research_bot.config import Settings

class CustomToolProvider:
    """Custom tool provider with additional tools."""

    def get_tools(self):
        return [
            MyCustomSearchTool(),
            MyCustomScrapeTool(),
        ]

settings = Settings()
service = ResearchService(
    settings,
    tool_provider=CustomToolProvider()
)
```

---

## Project Structure

```
research-bot/
├── src/research_bot/
│   ├── __init__.py           # Package exports
│   ├── __main__.py           # Module entry point
│   ├── main.py               # CLI implementation
│   │
│   ├── config/
│   │   └── settings.py       # Pydantic Settings configuration
│   │
│   ├── agents/               # Agent Factory Pattern
│   │   ├── base.py           # AgentFactory ABC
│   │   ├── planner.py        # PlannerAgentFactory
│   │   ├── researcher.py     # ResearcherAgentFactory
│   │   ├── analyst.py        # AnalystAgentFactory
│   │   ├── director.py       # DirectorAgentFactory
│   │   └── writer.py         # WriterAgentFactory
│   │
│   ├── tasks/                # Task Factory Pattern
│   │   ├── base.py           # TaskFactory ABC
│   │   ├── planning.py       # PlanningTaskFactory
│   │   ├── research.py       # ResearchTaskFactory
│   │   ├── analysis.py       # AnalysisTaskFactory
│   │   ├── review.py         # ReviewTaskFactory
│   │   └── report.py         # ReportTaskFactory
│   │
│   ├── crews/                # Builder Pattern
│   │   └── research_crew.py  # ResearchCrewBuilder
│   │
│   ├── models/               # Domain Models
│   │   ├── research.py       # ResearchSource, Finding, Result
│   │   └── report.py         # ReportSection, Metadata, Report
│   │
│   ├── tools/                # External Integrations
│   │   ├── tavily_search.py  # Tavily web search
│   │   └── scrape_tool.py    # scrape.do extraction
│   │
│   └── services/             # Orchestration
│       └── research_service.py
│
├── pyproject.toml            # Project metadata & dependencies
├── .env.example              # Environment template
└── README.md
```

---

## Design Patterns

### Factory Pattern (Agents & Tasks)

Abstract factories enable creation of agents and tasks without specifying concrete classes:

```python
class AgentFactory(ABC):
    """Abstract factory for creating CrewAI agents."""

    @property
    @abstractmethod
    def role(self) -> str: ...

    @property
    @abstractmethod
    def goal(self) -> str: ...

    def create(self) -> Agent:
        return Agent(role=self.role, goal=self.goal, ...)
```

**Benefits**: New agent types can be added without modifying existing code (Open/Closed Principle).

### Builder Pattern (Crew Assembly)

Fluent builder interface for constructing complex crew configurations:

```python
crew = (
    ResearchCrewBuilder(llm)
    .with_tools([search_tool, scrape_tool])
    .with_max_iterations(5)
    .with_verbose(True)
    .for_topic("AI in Healthcare")
    .build()
)
```

**Benefits**: Separates construction from representation, enables step-by-step configuration.

### Strategy Pattern (Tool Provision)

Protocol-based tool provider allows swapping tool implementations:

```python
class ToolProvider(Protocol):
    def get_tools(self) -> List[BaseTool]: ...

class DefaultToolProvider:
    def get_tools(self) -> List[BaseTool]:
        return [TavilySearchTool(), ScrapeTool()]
```

**Benefits**: Tools can be swapped without changing service code (Dependency Inversion).

### SOLID Principles

| Principle | Implementation |
|-----------|----------------|
| **S**ingle Responsibility | Each factory has one job |
| **O**pen/Closed | Extend via new factories, not modification |
| **L**iskov Substitution | All factories interchangeable via ABC |
| **I**nterface Segregation | Minimal `ToolProvider` protocol |
| **D**ependency Inversion | Settings/LLM injected, not created |

---

## Extending the System

### Adding a New Agent

1. Create factory in `agents/`:

```python
# agents/fact_checker.py
from research_bot.agents.base import AgentFactory

class FactCheckerAgentFactory(AgentFactory):
    @property
    def role(self) -> str:
        return "Fact Checker"

    @property
    def goal(self) -> str:
        return "Verify claims against authoritative sources"

    @property
    def backstory(self) -> str:
        return "You are a meticulous fact-checker..."
```

2. Create corresponding task in `tasks/`
3. Register in `ResearchCrewBuilder._build_agents()`

### Adding a New Tool

1. Implement `BaseTool`:

```python
from crewai.tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "my_tool"
    description: str = "Does something useful"

    def _run(self, query: str) -> str:
        # Implementation
        return result
```

2. Add to `DefaultToolProvider.get_tools()`

---

## Troubleshooting

### Common Issues

**API Key Errors**
```
ValueError: GOOGLE_API_KEY must be set
```
→ Ensure `.env` file exists and contains valid API keys

**Module Not Found**
```
ModuleNotFoundError: No module named 'research_bot'
```
→ Run `pip install -e .` from project root

**Rate Limiting**
```
429 Too Many Requests
```
→ Reduce `MAX_ITERATIONS` or add delays between requests

### Debug Mode

```bash
research-bot "topic" --verbose
```

This enables DEBUG logging and shows full agent reasoning.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [CrewAI](https://www.crewai.com/) - Multi-agent orchestration framework
- [Tavily](https://tavily.com/) - AI-optimized search API
- [scrape.do](https://scrape.do/) - Web scraping service
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Large language model

---

<p align="center">
  Built with ❤️ using CrewAI
</p>
