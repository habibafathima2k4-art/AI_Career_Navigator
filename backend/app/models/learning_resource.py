from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ProgressStatusEnum, ResourceTypeEnum
from app.models.mixins import TimestampMixin


class LearningResource(TimestampMixin, Base):
    __tablename__ = "learning_resources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    resource_type: Mapped[ResourceTypeEnum] = mapped_column(
        Enum(ResourceTypeEnum, name="resource_type_enum"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(120), nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id"), nullable=True)
    career_id: Mapped[int | None] = mapped_column(ForeignKey("careers.id"), nullable=True)

    skill = relationship("Skill", back_populates="learning_resources")
    career = relationship("Career", back_populates="learning_resources")
    progress_entries = relationship("UserProgress", back_populates="resource")


class UserProgress(TimestampMixin, Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id"), nullable=True)
    resource_id: Mapped[int | None] = mapped_column(
        ForeignKey("learning_resources.id"), nullable=True
    )
    status: Mapped[ProgressStatusEnum] = mapped_column(
        Enum(ProgressStatusEnum, name="progress_status_enum"), nullable=False
    )

    user = relationship("User", back_populates="progress_entries")
    skill = relationship("Skill", back_populates="progress_entries")
    resource = relationship("LearningResource", back_populates="progress_entries")
