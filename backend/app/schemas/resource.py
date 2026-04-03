from app.models.enums import ResourceTypeEnum, SkillCategoryEnum
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel, TimestampedSchema


class ResourceSkillSummary(ORMModel):
    id: int
    name: str
    category: SkillCategoryEnum


class LearningResourceResponse(TimestampedSchema):
    id: int
    title: str
    resource_type: ResourceTypeEnum
    url: str
    provider: str | None = None
    difficulty_level: str | None = None
    is_active: bool
    skill_id: int | None = None
    career_id: int | None = None
    skill: ResourceSkillSummary | None = None


class LearningResourceCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    resource_type: ResourceTypeEnum
    url: str = Field(min_length=5, max_length=500)
    provider: str | None = Field(default=None, max_length=120)
    difficulty_level: str | None = Field(default=None, max_length=50)
    is_active: bool = True
    skill_id: int | None = Field(default=None, gt=0)
    career_id: int | None = Field(default=None, gt=0)
