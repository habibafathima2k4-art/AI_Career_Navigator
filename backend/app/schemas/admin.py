from datetime import datetime

from pydantic import BaseModel


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
