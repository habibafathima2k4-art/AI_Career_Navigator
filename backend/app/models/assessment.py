from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import (
    EducationLevelEnum,
    ExperienceLevelEnum,
    InterestAreaEnum,
    ProficiencyLevelEnum,
    WorkStyleEnum,
)
from app.models.mixins import TimestampMixin


class Assessment(TimestampMixin, Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    interest_area: Mapped[InterestAreaEnum] = mapped_column(
        Enum(InterestAreaEnum, name="interest_area_enum"), nullable=False
    )
    education_level: Mapped[EducationLevelEnum] = mapped_column(
        Enum(EducationLevelEnum, name="assessment_education_level_enum"), nullable=False
    )
    experience_level: Mapped[ExperienceLevelEnum] = mapped_column(
        Enum(ExperienceLevelEnum, name="assessment_experience_level_enum"),
        nullable=False,
    )
    preferred_domain: Mapped[str | None] = mapped_column(String(120), nullable=True)
    work_style: Mapped[WorkStyleEnum | None] = mapped_column(
        Enum(WorkStyleEnum, name="work_style_enum"), nullable=True
    )
    goal_salary: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    user = relationship("User", back_populates="assessments")
    selected_skills = relationship(
        "AssessmentSkill", back_populates="assessment", cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "Recommendation", back_populates="assessment", cascade="all, delete-orphan"
    )


class AssessmentSkill(Base):
    __tablename__ = "assessment_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    proficiency_level: Mapped[ProficiencyLevelEnum] = mapped_column(
        Enum(ProficiencyLevelEnum, name="proficiency_level_enum"), nullable=False
    )
    years_of_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    assessment = relationship("Assessment", back_populates="selected_skills")
    skill = relationship("Skill", back_populates="assessment_links")

