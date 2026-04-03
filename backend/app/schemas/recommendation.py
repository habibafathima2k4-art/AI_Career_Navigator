from pydantic import BaseModel, Field

from app.schemas.career import CareerResponse
from app.schemas.common import ORMModel, TimestampedSchema


class RecommendationSkillGapResponse(ORMModel):
    skill_id: int
    gap_type: str
    note: str | None = None


class RecommendationResponse(TimestampedSchema):
    id: int
    assessment_id: int
    career_id: int
    fit_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    rank: int
    reason_summary: str | None = None
    career: CareerResponse
    skill_gaps: list[RecommendationSkillGapResponse] = []


class AssessmentRecommendationBundle(BaseModel):
    assessment_id: int
    recommendations: list[RecommendationResponse]
