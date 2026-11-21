"""
LegalEase Standalone Example Runner
Run directly from terminal without needing any server:
  python run_example.py
"""
import json
from app.rag.pipeline import RAGPipeline
from app.services.eligibility_engine import UserProfile, DeterministicEligibilityEngine

def print_separator(title):
    print("\n" + "=" * 70)
    print(f"  {title.upper()}")
    print("=" * 70)

def main():
    print_separator("LegalEase AI RAG Navigator - Example Run")
    print("Initializing FAISS Vector Store, Hugging Face Embeddings & Gemini...")
    rag = RAGPipeline.get_instance()
    print("Knowledge base ready! Total chunks indexed:", len(rag.retriever.chunks_corpus))

    # --- EXAMPLE 1: RAG Question on Income Criteria ---
    q1 = "What is the parental income ceiling for the PM-USP Central Sector Scholarship?"
    print_separator("Example 1: Direct RAG Query (English)")
    print(f"Citizen Query: \"{q1}\"\n")
    
    res1 = rag.query(q1, language="en")
    print("🎯 DIRECT ANSWER:")
    print(res1["answer"])
    print("\n📚 OFFICIAL DOCUMENT CITATIONS:")
    for c in res1.get("citations", []):
        print(f" • {c['document_name']} (Page {c['page_number']}) -> {c['source_url']}")

    # --- EXAMPLE 2: RAG Question on Required Documents ---
    q2 = "What documents are required for Post Matric Scholarship in Punjab for SC students?"
    print_separator("Example 2: Required Documents Query")
    print(f"Citizen Query: \"{q2}\"\n")
    
    res2 = rag.query(q2, language="en")
    print("🎯 DIRECT ANSWER:")
    print(res2["answer"])
    print("\n📚 OFFICIAL DOCUMENT CITATIONS:")
    for c in res2.get("citations", []):
        print(f" • {c['document_name']} (Page {c['page_number']}) -> {c['source_url']}")

    # --- EXAMPLE 3: Deterministic Eligibility Engine ---
    print_separator("Example 3: Deterministic Eligibility Checker")
    student_profile = {
        "state": "Punjab",
        "category": "SC",
        "education": "Undergraduate",
        "family_income": 180000,
        "board_percentile": 82.0
    }
    print("Evaluating Student Profile:")
    print(json.dumps(student_profile, indent=2))
    
    profile_obj = UserProfile(**student_profile)
    eval_results = DeterministicEligibilityEngine.evaluate_all_schemes(profile_obj)
    
    eligible = sum(1 for r in eval_results if r.match_status == "ELIGIBLE")
    print(f"\nEvaluated Schemes: {len(eval_results)}")
    print(f"Matched Eligible:  {eligible}")
    
    for r in eval_results:
        status = "✓ MATCH" if r.match_status == "ELIGIBLE" else "✗ NOT MATCHED"
        print(f"\n[{status}] {r.scheme_name} ({r.match_percentage}%)")
        print(f"  Award: {r.award_summary}")
        print(f"  Official Source: {r.official_source_doc}")

    print_separator("Example Completed Successfully")

if __name__ == "__main__":
    main()
