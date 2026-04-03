from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.assessment import Assessment
from app.models.career import Career, CareerSkill
from app.models.learning_resource import LearningResource
from app.models.recommendation import Recommendation
from app.models.skill import Skill
from app.models.user import User
from app.schemas.admin import AdminAnalyticsResponse, AdminRecentAssessment
from app.schemas.career import CareerCreate, CareerDetailResponse, SkillBase, SkillCreate
from app.schemas.resource import LearningResourceCreate, LearningResourceResponse
from app.services.admin_service import (
    create_career,
    create_learning_resource,
    create_skill,
    delete_career,
    delete_learning_resource,
    delete_skill,
    update_career,
    update_learning_resource,
    update_skill,
)

router = APIRouter()


@router.get("/analytics", response_model=AdminAnalyticsResponse)
def admin_analytics(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> AdminAnalyticsResponse:
    total_users = db.scalar(select(func.count()).select_from(User)) or 0
    total_assessments = db.scalar(select(func.count()).select_from(Assessment)) or 0
    total_careers = db.scalar(select(func.count()).select_from(Career)) or 0
    total_skills = db.scalar(select(func.count()).select_from(Skill)) or 0
    total_resources = db.scalar(select(func.count()).select_from(LearningResource)) or 0

    assessments = db.scalars(
        select(Assessment)
        .order_by(Assessment.created_at.desc())
        .limit(5)
        .options(selectinload(Assessment.recommendations).selectinload(Recommendation.career))
    ).all()

    recent_items: list[AdminRecentAssessment] = []
    for assessment in assessments:
        top_career = None
        fit_score = None
        if assessment.recommendations:
            best = sorted(assessment.recommendations, key=lambda item: item.rank)[0]
            top_career = best.career.title if best.career else None
            fit_score = float(best.fit_score)

        recent_items.append(
            AdminRecentAssessment(
                assessment_id=assessment.id,
                created_at=assessment.created_at,
                interest_area=assessment.interest_area.value,
                top_career=top_career,
                fit_score=fit_score,
            )
        )

    return AdminAnalyticsResponse(
        total_users=int(total_users),
        total_assessments=int(total_assessments),
        total_careers=int(total_careers),
        total_skills=int(total_skills),
        total_resources=int(total_resources),
        recent_assessments=recent_items,
    )


@router.get("/skills", response_model=list[SkillBase])
def admin_list_skills(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[SkillBase]:
    skills = db.scalars(select(Skill).order_by(Skill.name.asc())).all()
    return [SkillBase.model_validate(skill) for skill in skills]


@router.get("/careers", response_model=list[CareerDetailResponse])
def admin_list_careers(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[CareerDetailResponse]:
    careers = db.scalars(
        select(Career).order_by(Career.title.asc())
    ).all()
    hydrated = []
    for career in careers:
        loaded = db.scalar(
            select(Career)
            .where(Career.id == career.id)
            .options(
                selectinload(Career.required_skills).selectinload(CareerSkill.skill)
            )
        )
        if loaded is not None:
            hydrated.append(loaded)
    return [CareerDetailResponse.model_validate(career) for career in hydrated]


@router.get("/resources", response_model=list[LearningResourceResponse])
def admin_list_resources(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[LearningResourceResponse]:
    resources = db.scalars(
        select(LearningResource).order_by(LearningResource.title.asc())
    ).all()
    return [LearningResourceResponse.model_validate(resource) for resource in resources]


@router.post("/skills", response_model=SkillBase)
def admin_create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> SkillBase:
    try:
        skill = create_skill(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SkillBase.model_validate(skill)


@router.put("/skills/{skill_id}", response_model=SkillBase)
def admin_update_skill(
    skill_id: int,
    payload: SkillCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> SkillBase:
    try:
        skill = update_skill(db, skill_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SkillBase.model_validate(skill)


@router.delete("/skills/{skill_id}")
def admin_delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, str]:
    try:
        delete_skill(db, skill_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"message": "Skill deleted."}


@router.post("/careers", response_model=CareerDetailResponse)
def admin_create_career(
    payload: CareerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> CareerDetailResponse:
    try:
        career = create_career(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CareerDetailResponse.model_validate(career)


@router.put("/careers/{career_id}", response_model=CareerDetailResponse)
def admin_update_career(
    career_id: int,
    payload: CareerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> CareerDetailResponse:
    try:
        career = update_career(db, career_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CareerDetailResponse.model_validate(career)


@router.delete("/careers/{career_id}")
def admin_delete_career(
    career_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, str]:
    try:
        delete_career(db, career_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"message": "Career deleted."}


@router.post("/resources", response_model=LearningResourceResponse)
def admin_create_resource(
    payload: LearningResourceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> LearningResourceResponse:
    resource = create_learning_resource(db, payload)
    return LearningResourceResponse.model_validate(resource)


@router.put("/resources/{resource_id}", response_model=LearningResourceResponse)
def admin_update_resource(
    resource_id: int,
    payload: LearningResourceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> LearningResourceResponse:
    try:
        resource = update_learning_resource(db, resource_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return LearningResourceResponse.model_validate(resource)


@router.delete("/resources/{resource_id}")
def admin_delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, str]:
    try:
        delete_learning_resource(db, resource_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"message": "Resource deleted."}
