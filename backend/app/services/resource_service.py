from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models.learning_resource import LearningResource


def list_resources(
    db: Session,
    career_id: int | None = None,
    skill_id: int | None = None,
    limit: int | None = None,
) -> list[LearningResource]:
    statement: Select[tuple[LearningResource]] = (
        select(LearningResource)
        .where(LearningResource.is_active.is_(True))
        .options(selectinload(LearningResource.skill))
        .order_by(LearningResource.title.asc())
    )

    if career_id is not None:
        statement = statement.where(LearningResource.career_id == career_id)

    if skill_id is not None:
        statement = statement.where(LearningResource.skill_id == skill_id)

    if limit is not None:
        statement = statement.limit(limit)

    return list(db.scalars(statement).all())
