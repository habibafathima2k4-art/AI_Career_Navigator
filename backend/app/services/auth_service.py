from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import RoleEnum
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserRegister


def register_user(db: Session, payload: UserRegister) -> User:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing is not None:
        raise ValueError("An account with this email already exists.")

    user = User(
        full_name=payload.full_name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=RoleEnum.USER,
        education_level=payload.education_level,
        experience_level=payload.experience_level,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLogin) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise ValueError("Invalid email or password.")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, user=user)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)
