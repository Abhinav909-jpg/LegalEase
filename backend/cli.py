"""
LegaleEase Interactive Terminal CLI
Allows interactive exploration of schemes, live RAG chat, and eligibility evaluations.
"""
import sys
import json
import urllib.request

BASE_URL = "http://127.0.0.1:8000"

def chat_interactive():
    print("\n--- LegaleEase Interactive Grounded RAG Chat ---")
    print("Type your questions in English, Hindi, or Punjabi.")
    print("Type 'lang:hi' or 'lang:pa' or 'lang:en' to switch language.")
    print("Type 'exit' or 'back' to return to menu.\n")
    
    current_lang = "en"
    while True:
        try:
            prompt_str = f"[{current_lang.upper()}] Ask Scheme Question > "
            user_input = input(prompt_str).strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "back", "quit"]:
                break
            if user_input.lower().startswith("lang:"):
                current_lang = user_input.split(":")[1].strip().lower()
                print(f"Language set to: {current_lang}\n")
                continue

            payload = json.dumps({"message": user_input, "language": current_lang}).encode("utf-8")
            req = urllib.request.Request(
                f"{BASE_URL}/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            res = urllib.request.urlopen(req)
            data = json.loads(res.read().decode("utf-8"))

            print("\n" + "-" * 60)
            print("Verified Answer:")
            print(data["answer"])
            print("-" * 60)
            if data.get("citations"):
                print("Official Citations:")
                for c in data["citations"]:
                    print(f" • [Doc: {c['document_name']}, Page {c['page_number']}] - {c['scheme_name']}")
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)

def check_eligibility_interactive():
    print("\n--- Deterministic Eligibility Checker ---")
    try:
        state = input("State of domicile (e.g. Punjab, Delhi, All India) [Punjab]: ").strip() or "Punjab"
        category = input("Category (General, SC, ST, OBC, EBC, DNT) [SC]: ").strip() or "SC"
        income_str = input("Annual family income in INR [200000]: ").strip() or "200000"
        education = input("Current Education (Class 10, Class 12, Undergraduate, Postgraduate) [Undergraduate]: ").strip() or "Undergraduate"
        percentile_str = input("Class 12 Board Percentile (if applicable) [82]: ").strip() or "82"
        
        payload = json.dumps({
            "state": state,
            "category": category,
            "family_income": float(income_str),
            "education": education,
            "board_percentile": float(percentile_str)
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/api/eligibility/check",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))

        print("\n" + "=" * 60)
        print("ELIGIBILITY EVALUATION REPORT")
        print("=" * 60)
        print(f"Total Evaluated: {data['total_evaluated']} schemes")
        print(f"Eligible: {data['eligible_count']} | Potentially Eligible: {data['potentially_eligible_count']} | Ineligible: {data['ineligible_count']}\n")

        for r in data["results"]:
            symbol = "[✓ ELIGIBLE]" if r["match_status"] == "ELIGIBLE" else "[? POTENTIAL]" if r["match_status"] == "POTENTIALLY_ELIGIBLE" else "[✗ INELIGIBLE]"
            print(f"{symbol} {r['scheme_name']}")
            print(f"    Award:   {r['award_summary']}")
            print(f"    Source:  {r['official_source_doc']} | {r['source_url']}")
            if r["failed_conditions"]:
                print(f"    Reason:  {r['failed_conditions'][0]['explanation']}")
            print()

    except Exception as e:
        print("Error checking eligibility:", e)

def main():
    while True:
        print("\n" + "=" * 60)
        print("       LEGALEASE SCHOLARSHIP & SCHEME NAVIGATOR CLI       ")
        print("=" * 60)
        print("1. Grounded RAG Chat (Ask questions in English/Hindi/Punjabi)")
        print("2. Run Deterministic Eligibility Check")
        print("3. Run Pre-configured Terminal Demo")
        print("4. Exit")
        choice = input("\nSelect an option [1-4]: ").strip()

        if choice == "1":
            chat_interactive()
        elif choice == "2":
            check_eligibility_interactive()
        elif choice == "3":
            import subprocess
            subprocess.run(["python", "demo_terminal.py"])
        elif choice in ["4", "exit", "quit", "q"]:
            print("Exiting LegaleEase CLI.")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
