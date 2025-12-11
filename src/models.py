"""Data models for the Student Ambassador API.

These Pydantic models mirror the JSON schema definitions used in the specification.
They provide type checking and validation for request and response bodies.
"""

from datetime import date as date_type, datetime
from typing import List, Optional, Dict, Any, Annotated

from pydantic import BaseModel, Field, StringConstraints


class Document(BaseModel):
    """A file uploaded by the student, stored encrypted on device."""

    type: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)] = Field(
        ..., description="Type of document (e.g., transcript, award_letter)."
    )
    content_hash: str = Field(..., description="Hash of the file content for deduplication.")
    encrypted_content: str = Field(..., description="Encrypted content (base64 encoded).")


class TestScore(BaseModel):
    """Standardised test score record."""

    type: str = Field(..., description="Type of test (e.g., SAT, ACT, AP).")
    score: float = Field(..., ge=0, description="Numeric score obtained.")
    test_date: date_type = Field(..., description="Date of the test.")


class Activity(BaseModel):
    """Extracurricular activity or job."""

    name: str = Field(..., description="Name of the activity.")
    role: str = Field(..., description="Role held in the activity.")
    hours: int = Field(..., ge=0, description="Number of hours spent.")
    years: List[int] = Field(..., description="Years of participation (e.g. [2023, 2024]).")


class Essay(BaseModel):
    """Essay draft or final submission."""

    school_id: str
    prompt: str
    version: int = Field(..., ge=1)
    content_hash: str


class Recommendation(BaseModel):
    """Recommendation request and status."""

    recommender: str
    status: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, pattern="^(requested|received|submitted)$")] = Field(...)
    requested_date: date_type


class Student(BaseModel):
    """A single student with personal data stored on device."""

    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    documents: List[Document] = Field(default_factory=list)
    test_scores: List[TestScore] = Field(default_factory=list)
    activities: List[Activity] = Field(default_factory=list)
    essays: List[Essay] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    financials: Dict[str, Any] = Field(default_factory=dict, description="Detailed financial information.")


class Application(BaseModel):
    """An application record linking a student to a school and tracking status."""

    id: str
    student_id: str
    school_id: str
    status: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, pattern="^(draft|submitted|accepted|rejected)$")] = Field(...)
    timeline: Dict[str, Any] = Field(default_factory=dict)


class Negotiation(BaseModel):
    """Aid negotiation or appeal event."""

    id: str
    student_id: str
    negotiation_type: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, pattern="^(scholarship|grant|appeal|other)$")] = Field(...)
    ask: Dict[str, Any]
    result: Optional[str] = None
    strategy_used: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ScholarshipSource(BaseModel):
    """Provider of scholarships or grants."""

    id: str
    name: str
    amount_range: List[float] = Field(..., min_length=2, max_length=2)
    criteria: str
    deadline: date_type


class ScholarshipMatch(BaseModel):
    """Return structure for scholarship matches."""

    source: ScholarshipSource
    match_score: float = Field(..., ge=0, le=1)
    reasons: List[str]