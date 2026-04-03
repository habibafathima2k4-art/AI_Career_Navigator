from pydantic import BaseModel, Field

from app.models.enums import (
    EducationLevelEnum,
    ExperienceLevelEnum,
    InterestAreaEnum,
    ProficiencyLevelEnum,
    WorkStyleEnum,
)
from app.schemas.common import ORMModel, TimestampedSchema


class AssessmentSkillInput(BaseModel):
    skill_id: int = Field(gt=0)
    proficiency_level: ProficiencyLevelEnum
    years_of_experience: int | None = Field(default=None, ge=0, le=50)


class AssessmentCreate(BaseModel):
    interest_area: InterestAreaEnum
    education_level: EducationLevelEnum
    experience_level: ExperienceLevelEnum
    preferred_domain: str | None = Field(default=None, max_length=120)
    work_style: WorkStyleEnum | None = None
    goal_salary: float | None = Field(default=None, ge=0)
    skills: list[AssessmentSkillInput] = Field(default_factory=list)


class AssessmentSkillResponse(ORMModel):
    id: int
    skill_id: int
    proficiency_level: ProficiencyLevelEnum
    years_of_experience: int | None = None


class AssessmentResponse(TimestampedSchema):
    id: int
    user_id: int | None = None
    interest_area: InterestAreaEnum
    education_level: EducationLevelEnum
    experience_level: ExperienceLevelEnum
    preferred_domain: str | None = None
    work_style: WorkStyleEnum | None = None
    goal_salary: float | None = None
    selected_skills: list[AssessmentSkillResponse] = []


class AssessmentHistoryItem(ORMModel):
    assessment_id: int
    recommendation_id: int | None = None
    rank: int | None = None
    career_id: int | None = None
    career_title: str | None = None
    fit_score: float | None = None
    confidence_score: float | None = None
    reason_summary: str | None = None


class AssessmentListItem(TimestampedSchema):
    id: int
    user_id: int | None = None
    interest_area: InterestAreaEnum
    education_level: EducationLevelEnum
    experience_level: ExperienceLevelEnum
    preferred_domain: str | None = None
    work_style: WorkStyleEnum | None = None
    goal_salary: float | None = None
    selected_skills: list[AssessmentSkillResponse] = []
    top_recommendation: AssessmentHistoryItem | None = None
