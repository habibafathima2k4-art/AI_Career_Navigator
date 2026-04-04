from pydantic import BaseModel, Field

from app.models.enums import ImportanceLevelEnum, SkillCategoryEnum
from app.schemas.learning_resource import LearningResourceResponse
from app.schemas.common import ORMModel, TimestampedSchema


class SkillBase(ORMModel):
    id: int
    name: str
    category: SkillCategoryEnum
    description: str | None = None


class CareerSkillResponse(ORMModel):
    skill_id: int
    importance_level: ImportanceLevelEnum
    is_required: bool
    weight: int = Field(ge=1)
    skill: SkillBase


class CareerResponse(TimestampedSchema):
    id: int
    title: str
    slug: str
    description: str
    industry: str | None = None
    growth_outlook: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    is_active: bool


class CareerDetailResponse(CareerResponse):
    required_skills: list[CareerSkillResponse] = []
    learning_resources: list[LearningResourceResponse] = []


class SkillCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: SkillCategoryEnum
    description: str | None = Field(default=None, max_length=500)


class CareerSkillInput(BaseModel):
    skill_id: int = Field(gt=0)
    importance_level: ImportanceLevelEnum
    is_required: bool = True
    weight: int = Field(default=1, ge=1, le=10)


class CareerCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    description: str = Field(min_length=10)
    industry: str | None = Field(default=None, max_length=120)
    growth_outlook: str | None = Field(default=None, max_length=120)
    salary_min: float | None = Field(default=None, ge=0)
    salary_max: float | None = Field(default=None, ge=0)
    is_active: bool = True
    required_skills: list[CareerSkillInput] = Field(default_factory=list)
