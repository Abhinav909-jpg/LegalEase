import re
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("legalease.generation")

PROMPT_TEMPLATES = {
    "en": {
        "system": (
            "You are LegalEase, a strict, factual, and direct AI Government Scheme & Scholarship Navigator.\n"
            "CRITICAL TO-THE-POINT INSTRUCTIONS:\n"
            "1. STRICTLY ANSWER ONLY WHAT WAS ASKED. Do NOT dump unrelated sections from the context.\n"
            "   - If asked for REQUIRED DOCUMENTS: List ONLY the required documents. Do NOT explain domicile, income limits, or application procedures.\n"
            "   - If asked for INCOME LIMIT: State ONLY the exact income ceiling and certificate authority.\n"
            "   - If asked for AMOUNT / SCHOLARSHIP RATE: State ONLY the financial rates and duration.\n"
            "   - If asked for ELIGIBILITY: List ONLY the concise eligibility criteria.\n"
            "2. ZERO BOILERPLATE / ZERO FILLER:\n"
            "   - Never begin with introductory sentences like 'The requirements for X scheme include...'.\n"
            "   - Jump straight to the point in 1 clean sentence or crisp numbered/bullet list immediately.\n"
            "3. ACCURACY & CITATIONS:\n"
            "   - Every claim must cite [Source: Document Name, Page X].\n"
            "   - Never fabricate or guess any criteria, numbers, or portals.\n"
            "4. Only if the queried scheme or information is completely missing from the context, state:\n"
            "   'I cannot verify this information from the official government documents currently available.'"
        ),
        "unverified_msg": "I cannot verify this information from the official government documents currently available."
    },
    "hi": {
        "system": (
            "आप LegalEase हैं, जो एक सटीक, तथ्यपरक और सीधा सरकारी योजना सहायक है।\n"
            "अत्यंत महत्वपूर्ण निर्देश (Strictly To The Point):\n"
            "1. केवल वही उत्तर दें जो पूछा गया है। अनावश्यक जानकारी न दें।\n"
            "   - यदि आवश्यक दस्तावेज पूछे गए हैं: केवल दस्तावेजों की सूची दें। आय सीमा या आवेदन प्रक्रिया न बताएं।\n"
            "   - यदि आय सीमा पूछी गई है: केवल आय सीमा और प्रमाण पत्र जारीकर्ता का उल्लेख करें।\n"
            "   - यदि छात्रवृत्ति राशि पूछी गई है: केवल राशि बताएं।\n"
            "2. कोई अनावश्यक परिचयात्मक वाक्य न लिखें (जैसे 'दिए गए संदर्भ के अनुसार...')। सीधे मुख्य उत्तर से शुरुआत करें।\n"
            "3. प्रत्येक तथ्य के साथ [स्रोत: दस्तावेज़ नाम, पृष्ठ संख्या] का उल्लेख करें।"
        ),
        "unverified_msg": "उपलब्ध आधिकारिक सरकारी दस्तावेजों में इस प्रश्न के सत्यापन हेतु जानकारी उपलब्ध नहीं है।"
    },
    "pa": {
        "system": (
            "ਤੁਸੀਂ LegalEase ਹੋ, ਜੋ ਕਿ ਇੱਕ ਸਪੱਸ਼ਟ ਅਤੇ ਸਿੱਧਾ ਸਰਕਾਰੀ ਸਕੀਮ ਸਹਾਇਕ ਹੈ।\n"
            "ਨਿਯਮ (Strictly To The Point):\n"
            "1. ਸਿਰਫ਼ ਉਹੀ ਜਵਾਬ ਦਿਓ ਜੋ ਪੁੱਛਿਆ ਗਿਆ ਹੈ। ਬੇਲੋੜੀ ਜਾਣਕਾਰੀ ਨਾ ਦਿਓ।\n"
            "   - ਜੇਕਰ ਜ਼ਰੂਰੀ ਦਸਤਾਵੇਜ਼ ਪੁੱਛੇ ਗਏ ਹਨ: ਸਿਰਫ਼ ਦਸਤਾਵੇਜ਼ਾਂ ਦੀ ਸੂਚੀ ਦਿਓ।\n"
            "   - ਜੇਕਰ ਆਮਦਨ ਹੱਦ ਪੁੱਛੀ ਗਈ ਹੈ: ਸਿਰਫ਼ ਆਮਦਨ ਹੱਦ ਦੱਸੋ।\n"
            "   - ਜੇਕਰ ਰਕਮ ਪੁੱਛੀ ਗਈ ਹੈ: ਸਿਰਫ਼ ਸਕਾਲਰਸ਼ਿਪ ਦੀ ਰਕਮ ਦੱਸੋ।\n"
            "2. ਕੋਈ ਵਾਧੂ ਜਾਣ-ਪਛਾਣ ਵਾਲੇ ਵਾਕ ਨਾ ਲਿਖੋ। ਸਿੱਧਾ ਮੁੱਖ ਉੱਤਰ ਦਿਓ।\n"
            "3. ਹਰ ਤੱਥ ਦੇ ਨਾਲ [ਸਰੋਤ: ਦਸਤਾਵੇਜ਼ ਦਾ ਨਾਮ, ਪੰਨਾ ਨੰਬਰ] ਜ਼ਰੂਰ ਲਿਖੋ।"
        ),
        "unverified_msg": "ਮੌਜੂਦਾ ਉਪਲਬਧ ਸਰਕਾਰੀ ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ ਇਸ ਸਵਾਲ ਦੀ ਪੁਸ਼ਟੀ ਲਈ ਜਾਣਕਾਰੀ ਨਹੀਂ ਮਿਲੀ।"
    }
}

def extract_direct_facts(query: str, text: str) -> List[str]:
    """Extracts clean full sentences directly answering the user's specific query."""
    q_lower = query.lower()
    
    clean_text = text.replace("\r", " ")
    clean_text = re.sub(r"\bRs\.\s*", "₹", clean_text)
    clean_text = re.sub(r"\b(Dr|Prof|Mr|Mrs|No)\.\s*", r"\1 ", clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)
    
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text) if s.strip()]
    matched_lines = []

    is_income = any(w in q_lower for w in ["income", "ceiling", "earn", "salary", "lakh", "limit", "आय", "ਆਮਦਨ"])
    is_docs = any(w in q_lower for w in ["document", "certificate", "paper", "required", "need", "दस्तावेज", "ਦਸਤਾਵੇਜ਼", "freeship", "marksheet"])
    is_marks = any(w in q_lower for w in ["percentile", "mark", "percentage", "cutoff", "प्रतिशत", "ਪ੍ਰਤੀਸ਼ਤ", "ਅੰਕ"])
    is_amount = any(w in q_lower for w in ["amount", "money", "quantum", "rupee", "₹", "fee", "stipend", "grant", "राशि", "ਰਕਮ", "ਕਿੰਨੇ"])
    is_eligibility = any(w in q_lower for w in ["eligible", "eligibility", "who can", "criteria", "पात्र", "ਯੋਗ"])

    for s_clean in sentences:
        if len(s_clean) < 15:
            continue
        if any(h in s_clean for h in ["GOVERNMENT OF INDIA", "LegalEase Verified", "OFFICIAL SCHEME GUIDELINES"]):
            continue

        s_lower = s_clean.lower()
        if is_income and any(k in s_lower for k in ["income", "ceiling", "exceed", "lakh", "₹2,50,000", "₹4,50,000", "₹3,50,000"]):
            matched_lines.append(s_clean)
        elif is_docs and (any(k in s_lower for k in ["certificate", "marksheet", "aadhaar", "freeship", "bonafide", "mandatory documents", "tehsildar"]) or re.match(r"^\d+\.", s_clean)):
            matched_lines.append(s_clean)
        elif is_marks and any(k in s_lower for k in ["percentile", "80th", "55%", "50%", "examination", "marks"]):
            matched_lines.append(s_clean)
        elif is_amount and any(k in s_lower for k in ["₹", "12,000", "20,000", "75,000", "1,25,000", "allowance", "tuition", "annum", "month"]):
            matched_lines.append(s_clean)
        elif is_eligibility and any(k in s_lower for k in ["must", "eligible", "resident", "domicile", "category", "regular", "recognized", "class"]):
            matched_lines.append(s_clean)

    return matched_lines

class GroundedGenerator:
    _instance = None

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.client = None
        self.candidate_models = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"]
        
        if self.api_key and self.api_key.strip():
            try:
                import google.genai as genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Gemini client initialized. Preferred model: {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            logger.info("GEMINI_API_KEY not configured. Running in deterministic grounded synthesis mode.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GroundedGenerator()
        return cls._instance

    def _build_context_prompt(self, passages: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks into numbered context blocks with document citations."""
        blocks = []
        for i, passage in enumerate(passages, 1):
            doc_name = passage.get("document_name", "Official Guideline")
            page_num = passage.get("page_number", 1)
            scheme_name = passage.get("scheme_name", "")
            source_url = passage.get("source_url", "")
            text = passage.get("text", "").strip()

            block = (
                f"--- CONTEXT BLOCK {i} ---\n"
                f"Document: {doc_name}\n"
                f"Page: {page_num}\n"
                f"Scheme: {scheme_name}\n"
                f"Source URL: {source_url}\n"
                f"Content:\n{text}\n"
                f"-------------------------"
            )
            blocks.append(block)
        return "\n\n".join(blocks)

    def _deterministic_synthesis(
        self, 
        query: str, 
        passages: List[Dict[str, Any]], 
        lang: str
    ) -> Dict[str, Any]:
        """
        Grounded deterministic synthesis providing a strictly to-the-point answer.
        """
        config = PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES["en"])
        if not passages:
            return {
                "answer": config["unverified_msg"],
                "citations": [],
                "confidence": "unverified",
                "suggested_follow_ups": [
                    "What documents do I need for Punjab Post Matric Scholarship?",
                    "What is the income criteria for Central Sector Scholarship?",
                    "How to apply for PM-YASASVI scheme?"
                ],
                "language": lang
            }

        q_lower = query.lower()

        def scheme_priority(p):
            doc = p.get("document_name", "").lower()
            scheme = p.get("scheme_name", "").lower()
            target = doc + " " + scheme
            if ("central sector" in q_lower or "csss" in q_lower or "pm-usp" in q_lower) and ("central" in target or "pm-usp" in target):
                return 0
            if ("punjab" in q_lower or "sc" in q_lower) and "punjab" in target:
                return 0
            if ("yasasvi" in q_lower or "obc" in q_lower) and "yasasvi" in target:
                return 0
            if ("means" in q_lower or "nmmss" in q_lower) and "nmmss" in target:
                return 0
            return 1

        ordered_passages = sorted(passages, key=scheme_priority)
        top_passage = ordered_passages[0]
        scheme_name = top_passage.get("scheme_name", "Government Scheme")
        doc_name = top_passage.get("document_name", "Official Guidelines")
        page_num = top_passage.get("page_number", 1)

        citations = []
        seen_pages = set()
        all_relevant_text = []

        for p in ordered_passages[:4]:
            d_name = p.get("document_name")
            p_num = p.get("page_number")
            key = (d_name, p_num)
            if key not in seen_pages:
                seen_pages.add(key)
                citations.append({
                    "document_name": d_name,
                    "page_number": p_num,
                    "scheme_name": p.get("scheme_name"),
                    "source_url": p.get("source_url"),
                    "snippet": p.get("text", "")[:180] + "..."
                })
            all_relevant_text.append(p.get("text", ""))

        combined_text = "\n\n".join(all_relevant_text)
        direct_facts = extract_direct_facts(query, combined_text)

        if not direct_facts:
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", top_passage.get("text", "")) if len(s.strip()) > 25]
            direct_facts = sents[:3]

        unique_facts = []
        for f in direct_facts:
            clean_f = f.strip()
            if clean_f and clean_f not in unique_facts:
                unique_facts.append(clean_f)

        # Format clean, to-the-point list
        formatted_items = "\n".join([f"• {f}" for f in unique_facts[:6]])
        answer = f"{formatted_items}\n\n[Source: {doc_name}, Page {page_num}]"

        return {
            "answer": answer,
            "citations": citations,
            "confidence": "high",
            "suggested_follow_ups": [
                f"What are the eligibility requirements for {scheme_name}?",
                f"What documents are required to apply for {scheme_name}?",
                f"How do I apply for {scheme_name}?"
            ],
            "language": lang
        }

    def generate_grounded_answer(
        self,
        query: str,
        passages: List[Dict[str, Any]],
        language: str = "en",
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generates strictly to-the-point grounded response using Gemini API with citations.
        """
        lang = language.lower() if language in ["en", "hi", "pa"] else "en"
        config = PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES["en"])

        if not passages:
            return {
                "answer": config["unverified_msg"],
                "citations": [],
                "confidence": "unverified",
                "suggested_follow_ups": [
                    "What scholarships are available for Class 12 passed students?",
                    "Are there post-matric scholarships for SC students in Punjab?",
                    "What is the eligibility for PM-USP Central Sector Scholarship?"
                ],
                "language": lang
            }

        citations = []
        seen = set()
        for p in passages:
            key = (p.get("document_name"), p.get("page_number"))
            if key not in seen:
                seen.add(key)
                citations.append({
                    "document_name": p.get("document_name"),
                    "page_number": p.get("page_number"),
                    "scheme_name": p.get("scheme_name"),
                    "source_url": p.get("source_url"),
                    "snippet": p.get("text", "")[:180] + "..."
                })

        if not self.client:
            return self._deterministic_synthesis(query, passages, lang)

        context_str = self._build_context_prompt(passages)
        user_prompt = (
            f"USER QUESTION: {query}\n\n"
            f"OFFICIAL DOCUMENT CONTEXT:\n{context_str}\n\n"
            f"TASK: Answer ONLY what was specifically asked in {lang.upper()} language.\n"
            f"CRITICAL DIRECTNESS RULES:\n"
            f"1. Zero boilerplate: Do NOT write introductory paragraphs or summarize the whole scheme.\n"
            f"2. If asked for DOCUMENTS: list ONLY the documents required.\n"
            f"3. If asked for INCOME LIMIT: state ONLY the income limit and authority.\n"
            f"4. If asked for AMOUNT: state ONLY the grant / scholarship amount.\n"
            f"5. Keep it crisp, numbered or bulleted, and append [Source: Document Name, Page X]."
        )

        try:
            from google.genai import types

            models_to_try = [self.model_name] + [m for m in self.candidate_models if m != self.model_name]
            last_err = None

            for model_cand in models_to_try:
                try:
                    response = self.client.models.generate_content(
                        model=model_cand,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=config["system"],
                            temperature=0.0,  # Zero temperature for maximum precision and conciseness
                            max_output_tokens=400
                        )
                    )
                    generated_text = response.text or ""
                    
                    if "cannot verify" in generated_text.lower():
                        det_res = self._deterministic_synthesis(query, passages, lang)
                        if det_res.get("confidence") == "high":
                            return det_res

                    if generated_text.strip():
                        return {
                            "answer": generated_text.strip(),
                            "citations": citations,
                            "confidence": "high",
                            "suggested_follow_ups": [
                                "What are the required documents for this scheme?",
                                "How is the annual family income verified?",
                                "What is the official application portal and deadline?"
                            ],
                            "language": lang
                        }
                except Exception as model_err:
                    last_err = model_err
                    logger.warning(f"Model {model_cand} generation failed: {model_err}")
                    continue

            logger.error(f"All Gemini models failed ({last_err}). Falling back to deterministic synthesis.")
            return self._deterministic_synthesis(query, passages, lang)

        except Exception as e:
            logger.error(f"Gemini API call failed ({e}). Falling back to deterministic synthesis.")
            return self._deterministic_synthesis(query, passages, lang)

grounded_generator_service = GroundedGenerator.get_instance
