from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.career import Career, CareerSkill
from app.models.learning_resource import LearningResource


def list_active_careers(db: Session) -> list[Career]:
    statement = (
        select(Career)
        .where(Career.is_active.is_(True))
        .order_by(Career.title.asc())
    )
    return list(db.scalars(statement).all())


def get_career_by_id(db: Session, career_id: int) -> Career | None:
    statement = (
        select(Career)
        .where(Career.id == career_id)
        .options(
            selectinload(Career.required_skills).selectinload(CareerSkill.skill),
            selectinload(Career.learning_resources).selectinload(LearningResource.skill),
        )
    )
    return db.scalar(statement)
