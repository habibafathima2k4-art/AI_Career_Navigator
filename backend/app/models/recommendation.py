from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Recommendation(TimestampMixin, Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    career_id: Mapped[int] = mapped_column(ForeignKey("careers.id"), nullable=False)
    fit_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    reason_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    assessment = relationship("Assessment", back_populates="recommendations")
    career = relationship("Career", back_populates="recommendations")
    skill_gaps = relationship(
        "RecommendationSkillGap",
        back_populates="recommendation",
        cascade="all, delete-orphan",
    )


class RecommendationSkillGap(Base):
    __tablename__ = "recommendation_skill_gaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey("recommendations.id"), nullable=False
    )
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    gap_type: Mapped[str] = mapped_column(String(20), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    recommendation = relationship("Recommendation", back_populates="skill_gaps")
    skill = relationship("Skill", back_populates="recommendation_gaps")

