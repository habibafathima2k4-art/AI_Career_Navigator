from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models.enums import ProgressStatusEnum
from app.models.learning_resource import LearningResource, UserProgress


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


def get_resource(db: Session, resource_id: int) -> LearningResource | None:
    statement = select(LearningResource).where(LearningResource.id == resource_id)
    return db.scalar(statement)


def list_user_resource_progress(
    db: Session,
    user_id: int,
    career_id: int | None = None,
) -> list[UserProgress]:
    statement: Select[tuple[UserProgress]] = (
        select(UserProgress)
        .where(UserProgress.user_id == user_id, UserProgress.resource_id.is_not(None))
        .options(selectinload(UserProgress.resource))
        .order_by(UserProgress.updated_at.desc())
    )

    if career_id is not None:
        statement = statement.join(LearningResource, UserProgress.resource_id == LearningResource.id).where(
            LearningResource.career_id == career_id
        )

    return list(db.scalars(statement).all())


def upsert_user_resource_progress(
    db: Session,
    user_id: int,
    resource_id: int,
    status: ProgressStatusEnum,
) -> UserProgress:
    statement = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.resource_id == resource_id,
    )
    progress = db.scalar(statement)

    if progress is None:
        progress = UserProgress(
            user_id=user_id,
            resource_id=resource_id,
            status=status,
        )
        db.add(progress)
    else:
        progress.status = status

    db.commit()
    db.refresh(progress)
    return progress


def delete_user_resource_progress(db: Session, user_id: int, resource_id: int) -> bool:
    statement = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.resource_id == resource_id,
    )
    progress = db.scalar(statement)
    if progress is None:
        return False

    db.delete(progress)
    db.commit()
    return True
