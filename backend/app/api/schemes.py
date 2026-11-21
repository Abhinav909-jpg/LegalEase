from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/schemes", tags=["Schemes Directory"])

DETAILED_SCHEMES_DB = [
    {
        "id": "pm-usp-csss",
        "name": "PM-USP Central Sector Scheme of Scholarship for College and University Students",
        "short_name": "Central Sector Scholarship (PM-USP)",
        "ministry": "Ministry of Education (Department of Higher Education)",
        "target_audience": "Meritorious College and University Students across India",
        "benefits": "₹12,000 per annum for undergraduate studies (years 1-3); ₹20,000 per annum for postgraduate studies.",
        "quota": "82,000 fresh scholarships annually (50% earmarked for girls).",
        "eligibility": [
            "Scored above 80th percentile in relevant stream in Class 12 board exam.",
            "Enrolled in regular, full-time undergraduate or postgraduate course.",
            "Gross annual parental income must not exceed ₹4,50,000.",
            "Not receiving any other government scholarship or fee reimbursement."
        ],
        "required_documents": [
            "Class 12 Marksheet & Passing Certificate with Percentile",
            "Income Certificate issued by Revenue Authority (Tehsildar/SDM) <= 6 months",
            "Aadhaar Card with linked active DBT-enabled bank account",
            "Bonafide Student Certificate from College / University",
            "Category / Caste Certificate (SC/ST/OBC) if applicable"
        ],
        "application_procedure": [
            "1. Complete One-Time Registration (OTR) on the National Scholarship Portal (scholarships.gov.in).",
            "2. Fill in student profile, academic background, and institute details.",
            "3. Upload mandatory income, category, and student bonafide certificates.",
            "4. Submit online before closing deadline.",
            "5. Physical/online verification by Institutional Nodal Officer (INO) and State Nodal Officer (SNO)."
        ],
        "source_doc": "PM_USP_Central_Sector_Scholarship_Guidelines.pdf",
        "source_url": "https://scholarships.gov.in",
        "last_verified": "2024-08-15",
        "tags": ["Higher Education", "College", "University", "All India", "Merit-cum-Means"]
    },
    {
        "id": "punjab-post-matric-sc",
        "name": "Punjab Post Matric Scholarship Scheme for SC Students",
        "short_name": "Punjab SC Post Matric Scholarship",
        "ministry": "Department of Social Justice, Empowerment and Minorities, Govt of Punjab",
        "target_audience": "Scheduled Caste students resident in Punjab pursuing post-matric courses",
        "benefits": "100% Tuition and compulsory non-refundable fees reimbursement + up to ₹13,500/yr academic maintenance allowance.",
        "quota": "Open to all eligible SC students meeting income and residency norms.",
        "eligibility": [
            "Bonafide resident and domicile of Punjab state.",
            "Belongs to the Scheduled Caste (SC) category.",
            "Annual family income from all sources does not exceed ₹2,50,000.",
            "Enrolled in recognized Post-Matric course (Class 11, 12, ITI, Diploma, Degree, PG, PhD)."
        ],
        "required_documents": [
            "Punjab Domicile / Residence Certificate",
            "Valid SC Caste Certificate issued by Tehsildar / SDM",
            "Income Certificate for current financial year (<= ₹2.5 Lakh)",
            "Freeship Card from Dr. B.R. Ambedkar Portal",
            "College Bonafide and verified fee structure",
            "Aadhaar Card linked to Bank Account"
        ],
        "application_procedure": [
            "1. Register on Dr. B.R. Ambedkar SC Post Matric Portal (scholarships.punjab.gov.in).",
            "2. Apply for Freeship Card prior to college admission.",
            "3. Present Freeship Card to college so tuition is not charged upfront.",
            "4. Complete final scholarship submission on portal with college enrollment number."
        ],
        "source_doc": "Punjab_Post_Matric_Scholarship_SC_Guidelines.pdf",
        "source_url": "https://scholarships.punjab.gov.in",
        "last_verified": "2024-07-20",
        "tags": ["Punjab", "SC Students", "Tuition Reimbursement", "Post Matric"]
    },
    {
        "id": "pm-yasasvi",
        "name": "PM Young Achievers Scholarship Award Scheme for Vibrant India (PM-YASASVI)",
        "short_name": "PM-YASASVI Scheme",
        "ministry": "Ministry of Social Justice & Empowerment, Govt of India",
        "target_audience": "OBC, EBC, and DNT students studying in Top Class Schools",
        "benefits": "Up to ₹75,000 per annum for Class 9 & 10; up to ₹1,25,000 per annum for Class 11 & 12.",
        "quota": "Based on national merit list in identified Top Class Schools.",
        "eligibility": [
            "Must belong to OBC (Other Backward Classes), EBC, or DNT categories.",
            "Parental/Family income must not exceed ₹2,50,000 per annum.",
            "Studying in identified empaneled Top Class Schools in Class 9 or Class 11."
        ],
        "required_documents": [
            "Valid OBC / EBC / DNT Category Certificate",
            "Income Certificate signed by Competent Authority (<= ₹2.50 Lakh)",
            "Previous Class Marksheet (Class 8 or Class 10)",
            "Aadhaar Card",
            "School Bonafide Certificate"
        ],
        "application_procedure": [
            "1. Visit National Scholarship Portal (scholarships.gov.in) under Ministry of Social Justice & Empowerment.",
            "2. Select PM-YASASVI Top Class School Scheme.",
            "3. Submit academic details, category certificate, and school U-DISE code.",
            "4. School verification followed by central processing."
        ],
        "source_doc": "PM_YASASVI_Scholarship_Scheme_Guidelines.pdf",
        "source_url": "https://yet.nta.ac.in",
        "last_verified": "2024-09-01",
        "tags": ["OBC", "EBC", "DNT", "School Education", "Top Class Schools"]
    },
    {
        "id": "nmmss-scholarship",
        "name": "National Means-cum-Merit Scholarship Scheme (NMMSS)",
        "short_name": "NMMSS Merit Scholarship",
        "ministry": "Department of School Education & Literacy, Ministry of Education",
        "target_audience": "Meritorious Class 9 to 12 students from economically weaker sections",
        "benefits": "₹12,000 per annum (₹1,000 per month) from Class 9 to Class 12.",
        "quota": "1,00,000 fresh scholarships awarded each year across India.",
        "eligibility": [
            "Studying in a Government, Government-aided, or Local body school.",
            "Minimum 55% marks in Class 7 exam (50% for SC/ST).",
            "Selected through State-level MAT & SAT selection examination in Class 8.",
            "Annual parental income not exceeding ₹3,50,000 per annum."
        ],
        "required_documents": [
            "Class 7 & Class 8 Marksheets",
            "Income Certificate (<= ₹3.50 Lakh)",
            "State Selection Test (MAT/SAT) Admit Card and Scorecard",
            "Aadhaar-seeded Bank Account Passbook",
            "Govt School Enrollment Certificate"
        ],
        "application_procedure": [
            "1. Appear for State level NMMSS examination conducted in Class 8.",
            "2. Upon qualification, register on National Scholarship Portal (scholarships.gov.in).",
            "3. Submit application under NMMSS scheme with SBI/bank account details.",
            "4. School head certifies eligibility for annual DBT disbursement."
        ],
        "source_doc": "National_Means_cum_Merit_Scholarship_NMMSS.pdf",
        "source_url": "https://scholarships.gov.in",
        "last_verified": "2024-06-10",
        "tags": ["School Students", "Government School", "Class 9-12", "Monthly Stipend"]
    }
]

@router.get("", response_model=List[Dict[str, Any]])
async def get_all_schemes(
    query: Optional[str] = Query(None, description="Search keyword"),
    state: Optional[str] = Query(None, description="Filter by state"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Returns official government schemes matching filter criteria."""
    schemes = DETAILED_SCHEMES_DB
    
    if query:
        q = query.lower()
        schemes = [
            s for s in schemes 
            if q in s["name"].lower() or q in s["ministry"].lower() or any(q in t.lower() for t in s["tags"])
        ]
        
    if state and state.lower() != "all":
        st = state.lower()
        schemes = [
            s for s in schemes 
            if "all india" in [t.lower() for t in s["tags"]] or st in [t.lower() for t in s["tags"]] or st in s["name"].lower()
        ]
        
    if category and category.lower() != "all":
        cat = category.lower()
        schemes = [
            s for s in schemes 
            if "merit-cum-means" in [t.lower() for t in s["tags"]] or any(cat in t.lower() for t in s["tags"])
        ]

    return schemes

@router.get("/{scheme_id}", response_model=Dict[str, Any])
async def get_scheme_by_id(scheme_id: str):
    """Returns detailed scheme data including eligibility, documents, procedure, and official sources."""
    for scheme in DETAILED_SCHEMES_DB:
        if scheme["id"].lower() == scheme_id.lower():
            return scheme
    raise HTTPException(status_code=404, detail=f"Scheme with ID '{scheme_id}' not found.")
