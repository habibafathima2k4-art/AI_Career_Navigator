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
    ensure_resource_type_enum_values()


def ensure_resource_type_enum_values() -> None:
    # Postgres enum types are not altered by create_all, so extend the live enum
    # during startup before seed/update logic writes new resource types.
    if engine.dialect.name != "postgresql":
        return

    values = (
        "COURSE",
        "VIDEO",
        "ARTICLE",
        "PROJECT",
        "CERTIFICATION",
        "DOCUMENTATION",
    )

    with engine.begin() as connection:
        for value in values:
            connection.exec_driver_sql(
                f"ALTER TYPE resource_type_enum ADD VALUE IF NOT EXISTS '{value}'"
            )


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
