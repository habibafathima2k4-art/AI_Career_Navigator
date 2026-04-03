from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_current_user_optional
from app.core.database import get_db
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentListItem,
    AssessmentResponse,
)
from app.schemas.recommendation import (
    AssessmentRecommendationBundle,
)
from app.services.assessment_service import create_assessment as create_assessment_record
from app.services.assessment_service import get_assessment_by_id, list_assessments
from app.services.recommendation_service import (
    generate_recommendations_for_assessment,
    get_recommendations_for_assessment,
)

router = APIRouter()


@router.get("/", response_model=list[AssessmentListItem])
def get_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AssessmentListItem]:
    assessments = list_assessments(db, user_id=current_user.id)
    response: list[AssessmentListItem] = []
    for assessment in assessments:
        top_recommendation = None
        if assessment.recommendations:
            ranked = sorted(assessment.recommendations, key=lambda item: item.rank)
            best = ranked[0]
            top_recommendation = {
                "assessment_id": assessment.id,
                "recommendation_id": best.id,
                "rank": best.rank,
                "career_id": best.career_id,
                "career_title": best.career.title if best.career else None,
                "fit_score": float(best.fit_score),
                "confidence_score": float(best.confidence_score),
                "reason_summary": best.reason_summary,
            }

        response.append(
            AssessmentListItem(
                **AssessmentResponse.model_validate(assessment).model_dump(),
                top_recommendation=top_recommendation,
            )
        )
    return response


@router.post("/", response_model=AssessmentResponse)
def create_assessment(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> AssessmentResponse:
    try:
        assessment = create_assessment_record(
            db, payload, user_id=current_user.id if current_user else None
        )
        generate_recommendations_for_assessment(db, assessment.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AssessmentResponse.model_validate(assessment)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> AssessmentResponse:
    assessment = get_assessment_by_id(db, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    _enforce_assessment_access(assessment, current_user)
    return AssessmentResponse.model_validate(assessment)


@router.get("/{assessment_id}/recommendations", response_model=AssessmentRecommendationBundle)
def get_assessment_recommendations(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> AssessmentRecommendationBundle:
    assessment = get_assessment_by_id(db, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    _enforce_assessment_access(assessment, current_user)

    recommendations = get_recommendations_for_assessment(db, assessment_id)
    if not recommendations:
        recommendations = generate_recommendations_for_assessment(db, assessment_id)

    return AssessmentRecommendationBundle(
        assessment_id=assessment_id,
        recommendations=recommendations,
    )


def _enforce_assessment_access(
    assessment, current_user: User | None
) -> None:
    if assessment.user_id is None:
        return
    if current_user is None or assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this assessment.",
        )
