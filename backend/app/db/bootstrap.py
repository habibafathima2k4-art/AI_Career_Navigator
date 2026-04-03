from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.db.init_db import init_db
from app.db.seed_data import build_seed_entities
from app.models.career import Career
from app.models.enums import RoleEnum
from app.models.skill import Skill
from app.models.user import User


def seed_if_empty() -> None:
    with SessionLocal() as session:
        has_career = session.scalar(select(Career.id).limit(1))
        has_skill = session.scalar(select(Skill.id).limit(1))

        if has_career or has_skill:
            return

        skills, careers = build_seed_entities()
        session.add_all(skills)
        session.add_all(careers)
        session.commit()


def ensure_admin_user(
    *,
    full_name: str | None,
    email: str | None,
    password: str | None,
) -> None:
    if not full_name or not email or not password:
        return

    normalized_email = email.lower()

    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.email == normalized_email))

        if user is None:
            user = User(
                full_name=full_name,
                email=normalized_email,
                password_hash=hash_password(password),
                role=RoleEnum.ADMIN,
            )
            session.add(user)
            session.commit()
            return

        if user.role != RoleEnum.ADMIN:
            user.role = RoleEnum.ADMIN
            session.commit()


def bootstrap_database(
    *,
    admin_name: str | None = None,
    admin_email: str | None = None,
    admin_password: str | None = None,
) -> None:
    init_db()
    seed_if_empty()
    ensure_admin_user(
        full_name=admin_name,
        email=admin_email,
        password=admin_password,
    )
