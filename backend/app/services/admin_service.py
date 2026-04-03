from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.career import Career, CareerSkill
from app.models.learning_resource import LearningResource
from app.models.skill import Skill
from app.schemas.career import CareerCreate, SkillCreate
from app.schemas.resource import LearningResourceCreate


def create_skill(db: Session, payload: SkillCreate) -> Skill:
    existing = db.scalar(select(Skill).where(Skill.name == payload.name))
    if existing is not None:
        raise ValueError("A skill with this name already exists.")

    skill = Skill(
        name=payload.name,
        category=payload.category,
        description=payload.description,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill_id: int, payload: SkillCreate) -> Skill:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise ValueError("Skill not found.")

    existing = db.scalar(select(Skill).where(Skill.name == payload.name, Skill.id != skill_id))
    if existing is not None:
        raise ValueError("A skill with this name already exists.")

    skill.name = payload.name
    skill.category = payload.category
    skill.description = payload.description
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill_id: int) -> None:
    skill = db.get(Skill, skill_id)
    if skill is None:
        raise ValueError("Skill not found.")
    db.delete(skill)
    db.commit()


def create_career(db: Session, payload: CareerCreate) -> Career:
    if db.scalar(select(Career).where(Career.slug == payload.slug)) is not None:
        raise ValueError("A career with this slug already exists.")

    skill_ids = [item.skill_id for item in payload.required_skills]
    if skill_ids:
        existing_ids = set(db.scalars(select(Skill.id).where(Skill.id.in_(skill_ids))).all())
        missing_ids = sorted(set(skill_ids) - existing_ids)
        if missing_ids:
            raise ValueError(f"Unknown skill ids: {missing_ids}")

    career = Career(
        title=payload.title,
        slug=payload.slug,
        description=payload.description,
        industry=payload.industry,
        growth_outlook=payload.growth_outlook,
        salary_min=payload.salary_min,
        salary_max=payload.salary_max,
        is_active=payload.is_active,
    )

    for item in payload.required_skills:
        career.required_skills.append(
            CareerSkill(
                skill_id=item.skill_id,
                importance_level=item.importance_level,
                is_required=item.is_required,
                weight=item.weight,
            )
        )

    db.add(career)
    db.commit()
    db.refresh(career)
    return db.scalar(
        select(Career)
        .where(Career.id == career.id)
        .options(selectinload(Career.required_skills).selectinload(CareerSkill.skill))
    )


def update_career(db: Session, career_id: int, payload: CareerCreate) -> Career:
    career = db.scalar(
        select(Career)
        .where(Career.id == career_id)
        .options(selectinload(Career.required_skills))
    )
    if career is None:
        raise ValueError("Career not found.")

    existing = db.scalar(select(Career).where(Career.slug == payload.slug, Career.id != career_id))
    if existing is not None:
        raise ValueError("A career with this slug already exists.")

    skill_ids = [item.skill_id for item in payload.required_skills]
    if skill_ids:
        existing_ids = set(db.scalars(select(Skill.id).where(Skill.id.in_(skill_ids))).all())
        missing_ids = sorted(set(skill_ids) - existing_ids)
        if missing_ids:
            raise ValueError(f"Unknown skill ids: {missing_ids}")

    career.title = payload.title
    career.slug = payload.slug
    career.description = payload.description
    career.industry = payload.industry
    career.growth_outlook = payload.growth_outlook
    career.salary_min = payload.salary_min
    career.salary_max = payload.salary_max
    career.is_active = payload.is_active
    career.required_skills.clear()

    for item in payload.required_skills:
        career.required_skills.append(
            CareerSkill(
                skill_id=item.skill_id,
                importance_level=item.importance_level,
                is_required=item.is_required,
                weight=item.weight,
            )
        )

    db.add(career)
    db.commit()
    return db.scalar(
        select(Career)
        .where(Career.id == career.id)
        .options(selectinload(Career.required_skills).selectinload(CareerSkill.skill))
    )


def delete_career(db: Session, career_id: int) -> None:
    career = db.get(Career, career_id)
    if career is None:
        raise ValueError("Career not found.")
    db.delete(career)
    db.commit()


def create_learning_resource(db: Session, payload: LearningResourceCreate) -> LearningResource:
    resource = LearningResource(
        title=payload.title,
        resource_type=payload.resource_type,
        url=payload.url,
        provider=payload.provider,
        difficulty_level=payload.difficulty_level,
        is_active=payload.is_active,
        skill_id=payload.skill_id,
        career_id=payload.career_id,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def update_learning_resource(
    db: Session, resource_id: int, payload: LearningResourceCreate
) -> LearningResource:
    resource = db.get(LearningResource, resource_id)
    if resource is None:
        raise ValueError("Resource not found.")

    resource.title = payload.title
    resource.resource_type = payload.resource_type
    resource.url = payload.url
    resource.provider = payload.provider
    resource.difficulty_level = payload.difficulty_level
    resource.is_active = payload.is_active
    resource.skill_id = payload.skill_id
    resource.career_id = payload.career_id
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def delete_learning_resource(db: Session, resource_id: int) -> None:
    resource = db.get(LearningResource, resource_id)
    if resource is None:
        raise ValueError("Resource not found.")
    db.delete(resource)
    db.commit()
