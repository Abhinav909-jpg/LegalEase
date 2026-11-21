from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.eligibility_engine import (
    UserProfile, 
    DeterministicEligibilityEngine, 
    SchemeEvaluationResult
)

router = APIRouter(prefix="/api/eligibility", tags=["Eligibility Engine"])

class EligibilityCheckResponse(BaseModel):
    total_evaluated: int
    eligible_count: int
    potentially_eligible_count: int
    ineligible_count: int
    results: List[SchemeEvaluationResult]

@router.post("/check", response_model=EligibilityCheckResponse)
async def check_eligibility(profile: UserProfile):
    """
    Deterministic Eligibility Check:
    Evaluates user attributes (age, state, income, category, education, percentile)
    against structured official scheme rules without guessing or hallucinating.
    """
    results = DeterministicEligibilityEngine.evaluate_all_schemes(profile)
    
    eligible = sum(1 for r in results if r.match_status == "ELIGIBLE")
    potential = sum(1 for r in results if r.match_status == "POTENTIALLY_ELIGIBLE")
    ineligible = sum(1 for r in results if r.match_status == "INELIGIBLE")

    return EligibilityCheckResponse(
        total_evaluated=len(results),
        eligible_count=eligible,
        potentially_eligible_count=potential,
        ineligible_count=ineligible,
        results=results
    )
