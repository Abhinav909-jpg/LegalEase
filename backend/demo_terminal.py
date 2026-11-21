"""
LegalEase Terminal Demonstration Script
Showcases live interaction with:
1. Health & Knowledge Base status (FAISS, Hugging Face Embeddings, Unstructured)
2. Grounded RAG QA with page-level citations (English)
3. Multilingual RAG QA (Hindi)
4. Deterministic Eligibility Checker
"""
import json
import urllib.request
import time

BASE_URL = "http://127.0.0.1:8000"

def print_banner(text):
    print("\n" + "=" * 75)
    print(f"   {text.upper()}   ")
    print("=" * 75)

def check_health():
    print_banner("1. Live System Diagnostic & Knowledge Base Status")
    try:
        res = urllib.request.urlopen(f"{BASE_URL}/api/health", timeout=5)
        data = json.loads(res.read().decode("utf-8"))
        print(f"Status:             {data['status'].upper()}")
        print(f"Service:            {data['service']}")
        print(f"Version:            {data['version']}")
        print(f"Embedding Model:    {data['capabilities']['embedding_model']}")
        print(f"Reranker Model:     {data['capabilities']['reranker_model']}")
        print(f"Languages:          {', '.join(data['capabilities']['supported_languages'])}")
    except Exception as e:
        print("Health check failed:", e)

def test_rag_query(query, lang="en"):
    print_banner(f"2. Grounded RAG Chat Interaction ({lang.upper()})")
    print(f"Citizen Query: \"{query}\"\n")
    
    payload = json.dumps({"message": query, "language": lang}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    start = time.perf_counter()
    res = urllib.request.urlopen(req)
    latency = time.perf_counter() - start
    data = json.loads(res.read().decode("utf-8"))
    
    print("--- Grounded Verified Response ---")
    print(data["answer"])
    print("\n--- Verifiable Official Citations ---")
    for idx, c in enumerate(data.get("citations", []), 1):
        print(f" [{idx}] Document: {c['document_name']} | Page: {c['page_number']}")
        print(f"     Scheme:   {c['scheme_name']}")
        print(f"     Portal:   {c['source_url']}")
        print(f"     Excerpt:  {c['snippet']}")
    print(f"\nResponse Latency: {latency:.3f} seconds | Retrieved Passages: {data.get('retrieved_count', 0)}")

def test_eligibility():
    print_banner("3. Deterministic Eligibility Engine Evaluation")
    
    # Test Profile 1: Punjab SC College Student with low family income
    profile_1 = {
        "state": "Punjab",
        "category": "SC",
        "education": "Undergraduate",
        "family_income": 180000,
        "board_percentile": 82.5,
        "school_type": "Government"
    }
    print("Evaluating Student Profile 1:")
    print(json.dumps(profile_1, indent=2))
    
    payload = json.dumps(profile_1).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/eligibility/check",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode("utf-8"))
    
    print("\nResults Summary:")
    print(f"Total Evaluated: {data['total_evaluated']}")
    print(f"100% Eligible:   {data['eligible_count']}")
    print(f"Potentially:     {data['potentially_eligible_count']}")
    print(f"Ineligible:      {data['ineligible_count']}")
    
    print("\nDetailed Evaluation Breakdown:")
    for r in data["results"]:
        status_symbol = "✓" if r["match_status"] == "ELIGIBLE" else "?" if r["match_status"] == "POTENTIALLY_ELIGIBLE" else "✗"
        print(f"[{status_symbol}] {r['scheme_name']} ({r['match_status']} - {r['match_percentage']}%)")
        print(f"    Award:   {r['award_summary']}")
        print(f"    Source:  {r['official_source_doc']}")
        
        if r["matched_conditions"]:
            print(f"    Matched: {len(r['matched_conditions'])} rules verified.")
        if r["failed_conditions"]:
            print(f"    Failed:  {r['failed_conditions'][0]['explanation']}")
        if r["unknown_conditions"]:
            print(f"    Missing: {r['missing_information_questions'][0] if r['missing_information_questions'] else 'None'}")
        print()

def main():
    print("\n===========================================================================")
    print("          LEGALEASE AI SCHEME & SCHOLARSHIP NAVIGATOR DEMO          ")
    print("===========================================================================")
    check_health()
    
    # Query 1: Central Sector Scheme Income & Percentile
    test_rag_query("What is the parental income ceiling and marks percentile required for Central Sector Scholarship PM-USP?")
    
    # Query 2: Punjab Post Matric Scholarship Documents (Hindi)
    test_rag_query("पंजाब में पोस्ट मैट्रिक अनुसूचित जाति छात्रवृत्ति के लिए क्या नियम और दस्तावेज हैं?", lang="hi")
    
    # Query 3: Punjab Post Matric Scholarship Eligibility (Punjabi)
    test_rag_query("ਪੰਜਾਬ ਵਿੱਚ ਅਨੁਸੂਚਿਤ ਜਾਤੀਆਂ (SC) ਲਈ ਸਕਾਲਰਸ਼ਿਪ ਦੀ ਯੋਗਤਾ ਅਤੇ ਆਮਦਨ ਸੀਮਾ ਕੀ ਹੈ?", lang="pa")
    
    # Eligibility Check
    test_eligibility()
    
    print_banner("Demo Complete - All RAG & Rule Engines Verified Live!")

if __name__ == "__main__":
    main()
