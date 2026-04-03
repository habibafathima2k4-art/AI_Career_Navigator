from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.assessment import Assessment, AssessmentSkill
from app.models.career import Career, CareerSkill
from app.models.enums import ImportanceLevelEnum, InterestAreaEnum, ProficiencyLevelEnum
from app.models.recommendation import Recommendation, RecommendationSkillGap


PROFICIENCY_SCORE = {
    ProficiencyLevelEnum.BEGINNER: 1.0,
    ProficiencyLevelEnum.INTERMEDIATE: 1.6,
    ProficiencyLevelEnum.ADVANCED: 2.2,
}

IMPORTANCE_WEIGHT = {
    ImportanceLevelEnum.LOW: 1,
    ImportanceLevelEnum.MEDIUM: 2,
    ImportanceLevelEnum.HIGH: 3,
}

CAREER_INTEREST_MAP = {
    "ai-engineer": {InterestAreaEnum.TECH, InterestAreaEnum.DATA},
    "data-analyst": {InterestAreaEnum.DATA, InterestAreaEnum.BUSINESS, InterestAreaEnum.TECH},
    "product-manager": {InterestAreaEnum.BUSINESS, InterestAreaEnum.MANAGEMENT},
}


def generate_recommendations_for_assessment(
    db: Session, assessment_id: int, top_n: int = 3
) -> list[Recommendation]:
    assessment = (
        db.scalar(
            select(Assessment)
            .where(Assessment.id == assessment_id)
            .options(
                selectinload(Assessment.selected_skills).selectinload(AssessmentSkill.skill)
            )
        )
    )
    if assessment is None:
        raise ValueError("Assessment not found.")

    careers = list(
        db.scalars(
            select(Career).options(
                selectinload(Career.required_skills).selectinload(CareerSkill.skill)
            )
        ).all()
    )

    user_skill_scores = {
        item.skill_id: PROFICIENCY_SCORE[item.proficiency_level]
        + min(item.years_of_experience or 0, 5) * 0.1
        for item in assessment.selected_skills
    }

    # Replace any previous generated results to keep the endpoint deterministic.
    for existing in list(assessment.recommendations):
        db.delete(existing)
    db.flush()

    ranked_rows = []
    for career in careers:
        ranked_rows.append(_score_career(assessment, career, user_skill_scores))
    ranked_rows.sort(key=lambda item: item["fit_score"], reverse=True)

    created: list[Recommendation] = []
    for rank, row in enumerate(ranked_rows[:top_n], start=1):
        recommendation = Recommendation(
            assessment_id=assessment.id,
            career_id=row["career"].id,
            fit_score=row["fit_score"],
            confidence_score=row["confidence_score"],
            rank=rank,
            reason_summary=row["reason_summary"],
        )
        recommendation.skill_gaps = [
            RecommendationSkillGap(
                skill_id=gap["skill_id"],
                gap_type=gap["gap_type"],
                note=gap["note"],
            )
            for gap in row["skill_gaps"]
        ]
        db.add(recommendation)
        created.append(recommendation)

    db.commit()
    return get_recommendations_for_assessment(db, assessment.id)


def get_recommendations_for_assessment(
    db: Session, assessment_id: int
) -> list[Recommendation]:
    statement = (
        select(Recommendation)
        .where(Recommendation.assessment_id == assessment_id)
        .order_by(Recommendation.rank.asc())
        .options(
            selectinload(Recommendation.career),
            selectinload(Recommendation.skill_gaps).selectinload(RecommendationSkillGap.skill),
        )
    )
    return list(db.scalars(statement).all())


def _score_career(
    assessment: Assessment, career: Career, user_skill_scores: dict[int, float]
) -> dict[str, object]:
    weighted_total = 0
    earned_total = 0.0
    matched_names: list[str] = []
    missing_gaps: list[dict[str, object]] = []
    recommended_gaps: list[dict[str, object]] = []

    for requirement in career.required_skills:
        requirement_weight = requirement.weight * IMPORTANCE_WEIGHT[requirement.importance_level]
        weighted_total += requirement_weight
        user_score = user_skill_scores.get(requirement.skill_id, 0.0)
        if user_score:
            earned_total += requirement_weight * min(user_score / 2.2, 1.0)
            matched_names.append(requirement.skill.name)
        elif requirement.is_required:
            missing_gaps.append(
                {
                    "skill_id": requirement.skill_id,
                    "gap_type": "missing",
                    "note": f"Add {requirement.skill.name} to improve fit for {career.title}.",
                }
            )
        else:
            recommended_gaps.append(
                {
                    "skill_id": requirement.skill_id,
                    "gap_type": "recommended",
                    "note": f"{requirement.skill.name} can strengthen your profile further.",
                }
            )

    skill_score = (earned_total / weighted_total) * 70 if weighted_total else 0

    interest_bonus = 0
    if assessment.interest_area in CAREER_INTEREST_MAP.get(career.slug, set()):
        interest_bonus = 15

    salary_bonus = 0
    if assessment.goal_salary is not None and career.salary_max is not None:
        goal_salary = float(assessment.goal_salary)
        if float(career.salary_max) >= goal_salary:
            salary_bonus = 5

    preference_bonus = 0
    if assessment.preferred_domain and assessment.preferred_domain.lower() in (
        career.title.lower(),
        (career.industry or "").lower(),
    ):
        preference_bonus = 5

    fit_score = round(min(skill_score + interest_bonus + salary_bonus + preference_bonus, 100), 2)
    confidence_score = round(min(55 + fit_score * 0.4, 95), 2)

    reason_bits = []
    if matched_names:
        reason_bits.append(f"Matched skills: {', '.join(matched_names[:3])}")
    if interest_bonus:
        reason_bits.append("interest area aligns well")
    if salary_bonus:
        reason_bits.append("salary goal is realistic for this path")
    if not reason_bits:
        reason_bits.append("baseline fit based on available profile signals")

    return {
        "career": career,
        "fit_score": fit_score,
        "confidence_score": confidence_score,
        "reason_summary": ". ".join(reason_bits).capitalize() + ".",
        "skill_gaps": missing_gaps + recommended_gaps,
    }
