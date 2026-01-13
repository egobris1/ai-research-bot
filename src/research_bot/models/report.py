"""Report data models."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SectionType(str, Enum):
    """Enum for report section types."""

    EXECUTIVE_SUMMARY = "executive_summary"
    INTRODUCTION = "introduction"
    METHODOLOGY = "methodology"
    KEY_FINDINGS = "key_findings"
    INDUSTRY_ANALYSIS = "industry_analysis"
    CONCLUSIONS = "conclusions"
    REFERENCES = "references"


class ReportSection(BaseModel):
    """Model for a report section."""

    section_type: SectionType = Field(..., description="Type of section")
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content in markdown")
    order: int = Field(..., ge=0, description="Section order in report")

    class Config:
        frozen = True


class ReportMetadata(BaseModel):
    """Model for report metadata."""

    title: str = Field(..., description="Report title")
    topic: str = Field(..., description="Research topic")
    generated_at: datetime = Field(default_factory=datetime.now)
    author: str = Field(default="Research Bot", description="Report author")
    version: str = Field(default="1.0", description="Report version")

    class Config:
        frozen = True


class ResearchReport(BaseModel):
    """Model for complete research report."""

    metadata: ReportMetadata = Field(..., description="Report metadata")
    sections: List[ReportSection] = Field(default_factory=list)
    raw_content: Optional[str] = Field(None, description="Raw markdown content")

    @property
    def sorted_sections(self) -> List[ReportSection]:
        """Return sections sorted by order."""
        return sorted(self.sections, key=lambda s: s.order)

    def to_markdown(self) -> str:
        """Convert report to markdown string."""
        if self.raw_content:
            return self.raw_content

        lines = [
            f"# {self.metadata.title}",
            f"",
            f"**Topic:** {self.metadata.topic}",
            f"**Generated:** {self.metadata.generated_at.strftime('%Y-%m-%d %H:%M')}",
            f"**Author:** {self.metadata.author}",
            f"",
            "---",
            "",
        ]

        for section in self.sorted_sections:
            lines.append(f"## {section.title}")
            lines.append("")
            lines.append(section.content)
            lines.append("")

        return "\n".join(lines)
