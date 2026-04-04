from datetime import datetime

from pydantic import BaseModel, Field


class AdminRecentAssessment(BaseModel):
    assessment_id: int
    created_at: datetime
    interest_area: str
    top_career: str | None = None
    fit_score: float | None = None


class AdminAnalyticsResponse(BaseModel):
    total_users: int
    total_assessments: int
    total_careers: int
    total_skills: int
    total_resources: int
    recent_assessments: list[AdminRecentAssessment]


class AdminPasswordResetRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    new_password: str = Field(min_length=8, max_length=128)
