from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.core.database import Base
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models import Career, LearningResource, Skill, User
from app.models.enums import ResourceTypeEnum, RoleEnum, SkillCategoryEnum


SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db_session: Session) -> User:
    user = User(
        full_name="Test User",
        email="test@example.com",
        password_hash=hash_password("Password@123"),
        role=RoleEnum.USER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def auth_headers(test_user: User) -> dict[str, str]:
    token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def test_resource(db_session: Session) -> LearningResource:
    skill = Skill(
        name="Testing Skill",
        category=SkillCategoryEnum.TECHNICAL,
        description="Skill for API tests",
    )
    career = Career(
        title="QA Engineer",
        slug="qa-engineer",
        description="Test software quality.",
        industry="Software",
        growth_outlook="High",
    )
    db_session.add_all([skill, career])
    db_session.commit()
    db_session.refresh(skill)
    db_session.refresh(career)

    resource = LearningResource(
        title="Testing Documentation",
        resource_type=ResourceTypeEnum.DOCUMENTATION,
        url="https://example.com/testing-docs",
        provider="Docs",
        difficulty_level="beginner",
        skill_id=skill.id,
        career_id=career.id,
        is_active=True,
    )
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource
