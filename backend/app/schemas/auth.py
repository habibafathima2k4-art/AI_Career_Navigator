from pydantic import BaseModel, Field

from app.models.enums import EducationLevelEnum, ExperienceLevelEnum, RoleEnum
from app.schemas.common import ORMModel, TimestampedSchema


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    education_level: EducationLevelEnum | None = None
    experience_level: ExperienceLevelEnum | None = None


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class DirectPasswordResetRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    new_password: str = Field(min_length=8, max_length=128)


class UserResponse(TimestampedSchema):
    id: int
    full_name: str
    email: str
    role: RoleEnum
    education_level: EducationLevelEnum | None = None
    experience_level: ExperienceLevelEnum | None = None


class TokenResponse(ORMModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
