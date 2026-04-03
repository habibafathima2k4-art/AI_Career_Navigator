from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import SkillCategoryEnum


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[SkillCategoryEnum] = mapped_column(
        Enum(SkillCategoryEnum, name="skill_category_enum"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    career_links = relationship("CareerSkill", back_populates="skill")
    assessment_links = relationship("AssessmentSkill", back_populates="skill")
    recommendation_gaps = relationship("RecommendationSkillGap", back_populates="skill")
    learning_resources = relationship("LearningResource", back_populates="skill")
    progress_entries = relationship("UserProgress", back_populates="skill")

