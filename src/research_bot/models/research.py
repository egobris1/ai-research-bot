"""Research data models."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ResearchPhase(str, Enum):
    """Enum for research pipeline phases."""

    PLANNING = "planning"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    REVIEW = "review"
    REPORT = "report"


class ResearchSource(BaseModel):
    """Model for a research source/citation."""

    title: str = Field(..., description="Title of the source")
    url: HttpUrl = Field(..., description="URL of the source")
    snippet: Optional[str] = Field(None, description="Relevant excerpt from source")
    accessed_at: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True


class ResearchFinding(BaseModel):
    """Model for a single research finding."""

    content: str = Field(..., description="The finding content")
    sources: List[ResearchSource] = Field(default_factory=list)
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence score (0-1)",
    )
    phase: ResearchPhase = Field(..., description="Phase where finding was discovered")

    class Config:
        frozen = True


class ResearchResult(BaseModel):
    """Model for complete research results."""

    topic: str = Field(..., description="The research topic")
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    findings: List[ResearchFinding] = Field(default_factory=list)
    phases_completed: List[ResearchPhase] = Field(default_factory=list)

    def mark_complete(self) -> "ResearchResult":
        """Return a new instance marked as complete."""
        return self.model_copy(update={"completed_at": datetime.now()})

    @property
    def is_complete(self) -> bool:
        """Check if research is complete."""
        return self.completed_at is not None

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate research duration in seconds."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
