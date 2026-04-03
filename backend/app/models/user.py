from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import EducationLevelEnum, ExperienceLevelEnum, RoleEnum
from app.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False
    )
    education_level: Mapped[EducationLevelEnum | None] = mapped_column(
        Enum(EducationLevelEnum, name="education_level_enum"), nullable=True
    )
    experience_level: Mapped[ExperienceLevelEnum | None] = mapped_column(
        Enum(ExperienceLevelEnum, name="experience_level_enum"), nullable=True
    )

    assessments = relationship("Assessment", back_populates="user")
    progress_entries = relationship("UserProgress", back_populates="user")

