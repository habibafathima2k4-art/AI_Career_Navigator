from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.assessment import Assessment, AssessmentSkill
from app.models.recommendation import Recommendation
from app.models.skill import Skill
from app.schemas.assessment import AssessmentCreate


def create_assessment(
    db: Session, payload: AssessmentCreate, user_id: int | None = None
) -> Assessment:
    skill_ids = [item.skill_id for item in payload.skills]
    if skill_ids:
        existing_skill_ids = set(
            db.scalars(select(Skill.id).where(Skill.id.in_(skill_ids))).all()
        )
        missing_ids = sorted(set(skill_ids) - existing_skill_ids)
        if missing_ids:
            raise ValueError(f"Unknown skill ids: {missing_ids}")

    assessment = Assessment(
        user_id=user_id,
        interest_area=payload.interest_area,
        education_level=payload.education_level,
        experience_level=payload.experience_level,
        preferred_domain=payload.preferred_domain,
        work_style=payload.work_style,
        goal_salary=payload.goal_salary,
    )

    for skill in payload.skills:
        assessment.selected_skills.append(
            AssessmentSkill(
                skill_id=skill.skill_id,
                proficiency_level=skill.proficiency_level,
                years_of_experience=skill.years_of_experience,
            )
        )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return get_assessment_by_id(db, assessment.id)


def get_assessment_by_id(db: Session, assessment_id: int) -> Assessment | None:
    statement = (
        select(Assessment)
        .where(Assessment.id == assessment_id)
        .options(
            selectinload(Assessment.selected_skills).selectinload(AssessmentSkill.skill),
            selectinload(Assessment.recommendations).selectinload(Recommendation.career),
        )
    )
    return db.scalar(statement)


def list_assessments(
    db: Session, limit: int = 20, user_id: int | None = None
) -> list[Assessment]:
    statement = (
        select(Assessment)
        .order_by(Assessment.created_at.desc())
        .limit(limit)
        .options(
            selectinload(Assessment.selected_skills).selectinload(AssessmentSkill.skill),
            selectinload(Assessment.recommendations).selectinload(Recommendation.career),
        )
    )
    if user_id is not None:
        statement = statement.where(Assessment.user_id == user_id)
    return list(db.scalars(statement).all())
