from app.core.database import Base, engine
from app.models import (
    Assessment,
    AssessmentSkill,
    Career,
    CareerSkill,
    LearningResource,
    Recommendation,
    RecommendationSkillGap,
    Skill,
    User,
    UserProgress,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
