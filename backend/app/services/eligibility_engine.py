import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("schemesathi.eligibility")

class UserProfile(BaseModel):
    age: Optional[int] = Field(None, description="Age in years")
    state: Optional[str] = Field(None, description="State of domicile (e.g. Punjab, Delhi, Maharashtra)")
    education: Optional[str] = Field(None, description="Highest current education level (e.g. Class 10, Class 12, Undergraduate, Postgraduate)")
    family_income: Optional[float] = Field(None, description="Annual gross family income in INR")
    category: Optional[str] = Field(None, description="Social category (General, SC, ST, OBC, EBC, DNT)")
    gender: Optional[str] = Field(None, description="Gender (Male, Female, Transgender)")
    board_percentile: Optional[float] = Field(None, description="Percentile secured in Class 12 examination")
    marks_percentage: Optional[float] = Field(None, description="Percentage of marks in previous qualifying exam")
    school_type: Optional[str] = Field(None, description="School type (Government, Govt-Aided, Private, Kendriya Vidyalaya)")
    course_type: Optional[str] = Field("Regular", description="Course mode (Regular/Full-Time, Distance/Correspondence)")
    other_scholarships: Optional[bool] = Field(False, description="Whether user already receives another government scholarship")
    disability_status: Optional[bool] = Field(False, description="Whether candidate has a benchmark disability")

class ConditionEvaluation(BaseModel):
    parameter: str
    criterion_description: str
    status: str  # "MATCHED", "FAILED", "UNKNOWN"
    user_value: Any
    explanation: str

class SchemeEvaluationResult(BaseModel):
    scheme_id: str
    scheme_name: str
    ministry_or_dept: str
    match_status: str  # "ELIGIBLE", "INELIGIBLE", "POTENTIALLY_ELIGIBLE", "INSUFFICIENT_DATA"
    match_percentage: int
    matched_conditions: List[ConditionEvaluation]
    failed_conditions: List[ConditionEvaluation]
    unknown_conditions: List[ConditionEvaluation]
    missing_information_questions: List[str]
    award_summary: str
    official_source_doc: str
    source_url: str
    last_verified: str
    disclaimer: str

# Structured Scheme Definitions
SCHEME_CRITERIA_CATALOG = [
    {
        "id": "pm-usp-csss",
        "name": "PM-USP Central Sector Scheme of Scholarship (CSSS)",
        "ministry": "Ministry of Education (Dept of Higher Education)",
        "source_doc": "PM_USP_Central_Sector_Scholarship_Guidelines.pdf",
        "source_url": "https://scholarships.gov.in",
        "last_verified": "2024-08-15",
        "award": "₹12,000/yr for Graduation (3 yrs), ₹20,000/yr for Post-Graduation",
        "rules": {
            "income_max": 450000,
            "min_percentile": 80.0,
            "allowed_education": ["Class 12 Passed", "Undergraduate", "Postgraduate", "College / University"],
            "disallowed_course_types": ["Distance", "Correspondence", "Private"],
            "disallow_other_scholarships": True,
            "applicable_states": ["All"]
        }
    },
    {
        "id": "punjab-post-matric-sc",
        "name": "Post Matric Scholarship Scheme for SC Students (Punjab)",
        "ministry": "Department of Social Justice, Empowerment and Minorities, Govt of Punjab",
        "source_doc": "Punjab_Post_Matric_Scholarship_SC_Guidelines.pdf",
        "source_url": "https://scholarships.punjab.gov.in",
        "last_verified": "2024-07-20",
        "award": "100% Tuition & Non-refundable fees reimbursement + up to ₹13,500/yr maintenance allowance",
        "rules": {
            "required_state": "Punjab",
            "required_category": ["SC"],
            "income_max": 250000,
            "allowed_education": ["Class 11", "Class 12", "ITI", "Diploma", "Undergraduate", "Postgraduate", "PhD"]
        }
    },
    {
        "id": "pm-yasasvi",
        "name": "PM Young Achievers Scholarship Scheme (PM-YASASVI)",
        "ministry": "Ministry of Social Justice & Empowerment",
        "source_doc": "PM_YASASVI_Scholarship_Scheme_Guidelines.pdf",
        "source_url": "https://yet.nta.ac.in",
        "last_verified": "2024-09-01",
        "award": "Up to ₹75,000/yr for Class 9-10; up to ₹1,25,000/yr for Class 11-12 in Top Class Schools",
        "rules": {
            "required_category": ["OBC", "EBC", "DNT"],
            "income_max": 250000,
            "allowed_education": ["Class 9", "Class 10", "Class 11", "Class 12", "Undergraduate"]
        }
    },
    {
        "id": "nmmss-scholarship",
        "name": "National Means-cum-Merit Scholarship Scheme (NMMSS)",
        "ministry": "Department of School Education & Literacy, Ministry of Education",
        "source_doc": "National_Means_cum_Merit_Scholarship_NMMSS.pdf",
        "source_url": "https://scholarships.gov.in",
        "last_verified": "2024-06-10",
        "award": "₹12,000 per annum (₹1,000 per month) from Class 9 to Class 12",
        "rules": {
            "income_max": 350000,
            "min_marks_percent": 55.0,
            "allowed_school_types": ["Government", "Govt-Aided", "Local Body"],
            "allowed_education": ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]
        }
    }
]

DISCLAIMER_TEXT = (
    "Disclaimer: LegaleEase provides eligibility evaluations solely based on verified government criteria. "
    "This evaluation does NOT guarantee sanction, award, or financial benefit. Final approval depends entirely "
    "on document verification, quota allocation, and sanction by the respective government authority."
)

class DeterministicEligibilityEngine:
    @staticmethod
    def evaluate_scheme(profile: UserProfile, scheme: Dict[str, Any]) -> SchemeEvaluationResult:
        matched: List[ConditionEvaluation] = []
        failed: List[ConditionEvaluation] = []
        unknown: List[ConditionEvaluation] = []
        questions: List[str] = []

        rules = scheme["rules"]

        # 1. State / Domicile Check
        if "required_state" in rules:
            target_state = rules["required_state"]
            if profile.state is None or not profile.state.strip():
                unknown.append(ConditionEvaluation(
                    parameter="state",
                    criterion_description=f"Must be a resident and domicile of {target_state}",
                    status="UNKNOWN",
                    user_value=None,
                    explanation=f"State of domicile has not been provided. Please confirm if you are from {target_state}."
                ))
                questions.append(f"Are you a bonafide resident/domicile of {target_state}?")
            elif profile.state.strip().lower() == target_state.lower():
                matched.append(ConditionEvaluation(
                    parameter="state",
                    criterion_description=f"Must be a resident of {target_state}",
                    status="MATCHED",
                    user_value=profile.state,
                    explanation=f"Matches required domicile of {target_state}."
                ))
            else:
                failed.append(ConditionEvaluation(
                    parameter="state",
                    criterion_description=f"Must be a resident of {target_state}",
                    status="FAILED",
                    user_value=profile.state,
                    explanation=f"Requires {target_state} domicile, but your state is set to {profile.state}."
                ))

        # 2. Social Category Check
        if "required_category" in rules:
            cats = [c.upper() for c in rules["required_category"]]
            if profile.category is None or not profile.category.strip():
                unknown.append(ConditionEvaluation(
                    parameter="category",
                    criterion_description=f"Candidate must belong to {'/'.join(cats)} category",
                    status="UNKNOWN",
                    user_value=None,
                    explanation=f"Category not specified. This scheme is reserved for {'/'.join(cats)} students."
                ))
                questions.append(f"Do you possess a valid certificate for {'/'.join(cats)} category?")
            elif profile.category.strip().upper() in cats:
                matched.append(ConditionEvaluation(
                    parameter="category",
                    criterion_description=f"Candidate must belong to {'/'.join(cats)} category",
                    status="MATCHED",
                    user_value=profile.category,
                    explanation=f"Your category ({profile.category.upper()}) matches the eligible criteria."
                ))
            else:
                failed.append(ConditionEvaluation(
                    parameter="category",
                    criterion_description=f"Candidate must belong to {'/'.join(cats)} category",
                    status="FAILED",
                    user_value=profile.category,
                    explanation=f"Scheme is designated exclusively for {'/'.join(cats)} category. You selected {profile.category}."
                ))

        # 3. Annual Family Income Check
        if "income_max" in rules:
            max_inc = rules["income_max"]
            if profile.family_income is None:
                unknown.append(ConditionEvaluation(
                    parameter="family_income",
                    criterion_description=f"Annual gross parental income must not exceed ₹{max_inc:,}",
                    status="UNKNOWN",
                    user_value=None,
                    explanation=f"Annual income not provided. Income ceiling for this scheme is ₹{max_inc:,}."
                ))
                questions.append(f"Is your gross annual parental family income less than or equal to ₹{max_inc:,}?")
            elif profile.family_income <= max_inc:
                matched.append(ConditionEvaluation(
                    parameter="family_income",
                    criterion_description=f"Annual gross parental income must not exceed ₹{max_inc:,}",
                    status="MATCHED",
                    user_value=profile.family_income,
                    explanation=f"Your annual family income (₹{profile.family_income:,.0f}) is within the permissible limit of ₹{max_inc:,}."
                ))
            else:
                failed.append(ConditionEvaluation(
                    parameter="family_income",
                    criterion_description=f"Annual gross parental income must not exceed ₹{max_inc:,}",
                    status="FAILED",
                    user_value=profile.family_income,
                    explanation=f"Your annual family income (₹{profile.family_income:,.0f}) exceeds the ceiling of ₹{max_inc:,}."
                ))

        # 4. Education Level Check
        if "allowed_education" in rules:
            allowed = [e.lower() for e in rules["allowed_education"]]
            if profile.education is None or not profile.education.strip():
                unknown.append(ConditionEvaluation(
                    parameter="education",
                    criterion_description=f"Enrolled in: {', '.join(rules['allowed_education'])}",
                    status="UNKNOWN",
                    user_value=None,
                    explanation="Current education stage not specified."
                ))
                questions.append("What is your current class or course of study?")
            else:
                user_edu = profile.education.strip().lower()
                is_match = any(a in user_edu or user_edu in a for a in allowed)
                if is_match:
                    matched.append(ConditionEvaluation(
                        parameter="education",
                        criterion_description=f"Enrolled in: {', '.join(rules['allowed_education'])}",
                        status="MATCHED",
                        user_value=profile.education,
                        explanation=f"Your education level ({profile.education}) is eligible."
                    ))
                else:
                    failed.append(ConditionEvaluation(
                        parameter="education",
                        criterion_description=f"Enrolled in: {', '.join(rules['allowed_education'])}",
                        status="FAILED",
                        user_value=profile.education,
                        explanation=f"Your education level ({profile.education}) is not supported by this scheme."
                    ))

        # 5. Class 12 Percentile Check (if applicable)
        if "min_percentile" in rules:
            min_perc = rules["min_percentile"]
            if profile.board_percentile is None:
                unknown.append(ConditionEvaluation(
                    parameter="board_percentile",
                    criterion_description=f"Must score above {min_perc}th percentile in Class 12 Board Exam",
                    status="UNKNOWN",
                    user_value=None,
                    explanation=f"Class 12 board percentile not provided. Requires > {min_perc}th percentile."
                ))
                questions.append(f"Did you score above the 80th percentile in your Class 12 board exams?")
            elif profile.board_percentile >= min_perc:
                matched.append(ConditionEvaluation(
                    parameter="board_percentile",
                    criterion_description=f"Must score above {min_perc}th percentile in Class 12 Board Exam",
                    status="MATCHED",
                    user_value=profile.board_percentile,
                    explanation=f"Your percentile ({profile.board_percentile}) meets the requirement of > {min_perc}th percentile."
                ))
            else:
                failed.append(ConditionEvaluation(
                    parameter="board_percentile",
                    criterion_description=f"Must score above {min_perc}th percentile in Class 12 Board Exam",
                    status="FAILED",
                    user_value=profile.board_percentile,
                    explanation=f"Your percentile ({profile.board_percentile}) is below the required {min_perc}th percentile cutoff."
                ))

        # 6. School Type Check (for NMMSS)
        if "allowed_school_types" in rules:
            allowed_types = [st.lower() for st in rules["allowed_school_types"]]
            if profile.school_type is None or not profile.school_type.strip():
                unknown.append(ConditionEvaluation(
                    parameter="school_type",
                    criterion_description=f"Must study in a Government, Govt-Aided, or Local Body school",
                    status="UNKNOWN",
                    user_value=None,
                    explanation="School type not provided. Private school and Kendriya Vidyalaya students are not eligible."
                ))
                questions.append("Do you attend a Government, Govt-aided, or Local body school?")
            else:
                user_st = profile.school_type.strip().lower()
                if any(st in user_st for st in allowed_types):
                    matched.append(ConditionEvaluation(
                        parameter="school_type",
                        criterion_description=f"Must study in a Government, Govt-Aided, or Local Body school",
                        status="MATCHED",
                        user_value=profile.school_type,
                        explanation=f"Your school type ({profile.school_type}) is eligible."
                    ))
                else:
                    failed.append(ConditionEvaluation(
                        parameter="school_type",
                        criterion_description=f"Must study in a Government, Govt-Aided, or Local Body school",
                        status="FAILED",
                        user_value=profile.school_type,
                        explanation=f"Students of {profile.school_type} schools are excluded from this scheme."
                    ))

        # Determine overall match status
        total_conditions = len(matched) + len(failed) + len(unknown)
        match_pct = int((len(matched) / total_conditions) * 100) if total_conditions > 0 else 0

        if failed:
            match_status = "INELIGIBLE"
        elif unknown and not matched:
            match_status = "INSUFFICIENT_DATA"
        elif unknown and matched:
            match_status = "POTENTIALLY_ELIGIBLE"
        else:
            match_status = "ELIGIBLE"

        return SchemeEvaluationResult(
            scheme_id=scheme["id"],
            scheme_name=scheme["name"],
            ministry_or_dept=scheme["ministry"],
            match_status=match_status,
            match_percentage=match_pct,
            matched_conditions=matched,
            failed_conditions=failed,
            unknown_conditions=unknown,
            missing_information_questions=questions,
            award_summary=scheme["award"],
            official_source_doc=scheme["source_doc"],
            source_url=scheme["source_url"],
            last_verified=scheme["last_verified"],
            disclaimer=DISCLAIMER_TEXT
        )

    @classmethod
    def evaluate_all_schemes(cls, profile: UserProfile) -> List[SchemeEvaluationResult]:
        """Evaluates user profile across all structured schemes in catalog."""
        results = []
        for scheme in SCHEME_CRITERIA_CATALOG:
            eval_result = cls.evaluate_scheme(profile, scheme)
            results.append(eval_result)
        
        # Sort so ELIGIBLE and POTENTIALLY_ELIGIBLE appear first
        priority = {
            "ELIGIBLE": 1,
            "POTENTIALLY_ELIGIBLE": 2,
            "INSUFFICIENT_DATA": 3,
            "INELIGIBLE": 4
        }
        results.sort(key=lambda r: (priority.get(r.match_status, 5), -r.match_percentage))
        return results
