"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore unknown env vars
    )

    # API Keys (required)
    tavily_api_key: str
    scrape_do_api_key: str
    google_api_key: str

    # LLM Configuration
    llm_model: str = "gemini/gemini-2.0-flash"
    llm_temperature: float = 0.3

    # Agent-specific temperatures
    director_temperature: float = 0.3
    researcher_temperature: float = 0.5
    writer_temperature: float = 0.7

    # Research Configuration
    max_iterations: int = 5
    max_research_rounds: int = 3
    max_sources_per_round: int = 10
    topic_similarity_threshold: float = 0.7

    # Logging
    log_level: str = "INFO"
    crew_verbose: bool = True
