from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ImportanceLevelEnum
from app.models.mixins import TimestampMixin


class Career(TimestampMixin, Base):
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    industry: Mapped[str | None] = mapped_column(String(120), nullable=True)
    growth_outlook: Mapped[str | None] = mapped_column(String(120), nullable=True)
    salary_min: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    required_skills = relationship("CareerSkill", back_populates="career")
    recommendations = relationship("Recommendation", back_populates="career")
    learning_resources = relationship("LearningResource", back_populates="career")


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_id: Mapped[int] = mapped_column(ForeignKey("careers.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    importance_level: Mapped[ImportanceLevelEnum] = mapped_column(
        Enum(ImportanceLevelEnum, name="importance_level_enum"),
        default=ImportanceLevelEnum.MEDIUM,
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    career = relationship("Career", back_populates="required_skills")
    skill = relationship("Skill", back_populates="career_links")

