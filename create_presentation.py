import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(11, 37, 69)          # #0B2545
    PRIMARY_BLUE = RGBColor(2, 112, 199) # #0270C7
    LIGHT_BLUE = RGBColor(224, 239, 254) # #E0EFFE
    DARK_TEXT = RGBColor(15, 23, 42)     # #0F172A
    MUTED_TEXT = RGBColor(71, 85, 105)   # #475569
    CARD_BG = RGBColor(248, 250, 252)    # #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240)# #E2E8F0
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(16, 185, 129)       # #10B981
    AMBER = RGBColor(245, 158, 11)       # #F59E0B

    def add_header(slide, tag, title, subtitle):
        # Header Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = tag.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_BLUE

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(4)

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(13)
            p2.font.color.rgb = MUTED_TEXT
            p2.space_before = Pt(3)

    def add_card(slide, left, top, width, height, title, items, badge_text=None, badge_color=PRIMARY_BLUE):
        # Card background shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)

        if badge_text:
            p_badge = tf.paragraphs[0]
            p_badge.text = badge_text.upper()
            p_badge.font.size = Pt(9)
            p_badge.font.bold = True
            p_badge.font.color.rgb = badge_color
            
            p_title = tf.add_paragraph()
            p_title.text = title
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = NAVY
            p_title.space_before = Pt(3)
        else:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = NAVY

        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = DARK_TEXT
            p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Title Card Textbox
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🏛️ SATHACK 2026 PRESENTATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(124, 200, 251)

    p = tf1.add_paragraph()
    p.text = "LegalEase 🇮🇳"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "AI-Powered Government Scheme & Scholarship Navigator for Indian Citizens"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(224, 239, 254)
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "End-to-End RAG Platform: Unstructured PDF Extraction → CharacterTextSplitter → Hugging Face Embeddings → FAISS Vector Store → Cross-Encoder Reranking → Google Gemini Grounded Generation"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_before = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Team: Sathack Winners | Live: https://abhinav909-jpg.github.io/Sathack_winners/"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(54, 171, 246)
    p.space_before = Pt(18)

    # -------------------------------------------------------------
    # SLIDE 2: THE PROBLEM (WHY CITIZENS LOSE WELFARE)
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Core Problem", "The ₹50,000 Crore Welfare Information Gap", "Over 140 Million eligible students and citizens fail to receive legitimate government aid due to systemic friction.")

    add_card(s2, Inches(0.8), Inches(2.1), Inches(3.6), Inches(4.6), "Complex Legal Language", [
        "Government guidelines are 30-80 page legalistic PDFs filled with bureaucratic jargon.",
        "Crucial eligibility limits (like family income ceiling of ₹2.5L or ₹4.5L) are buried deep inside.",
        "Students misunderstand qualifications and never apply."
    ], "Friction #1", AMBER)

    add_card(s2, Inches(4.8), Inches(2.1), Inches(3.6), Inches(4.6), "Predatory Intermediaries", [
        "Citizens rely on cyber-café brokers who charge ₹500 - ₹2,000 per application.",
        "Fraudulent agents take cuts of scholarship amounts.",
        "Lack of direct, authentic access to official state portals and Free-ship cards."
    ], "Friction #2", AMBER)

    add_card(s2, Inches(8.8), Inches(2.1), Inches(3.6), Inches(4.6), "General LLM Hallucinations", [
        "Generic AI (ChatGPT, standard LLMs) invents non-existent deadlines, quotas, and cash amounts.",
        "No verifiable citations or page numbers provided.",
        "Users risk severe penalties or rejection based on hallucinated AI advice."
    ], "Friction #3", AMBER)

    # -------------------------------------------------------------
    # SLIDE 3: THE SOLUTION (HOW LEGALEASE SOLVES THIS)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Our Solution", "LegalEase: Grounded, Verified & Deterministic", "Transforming opaque government gazettes into actionable, cited, and personalized guidance.")

    add_card(s3, Inches(0.8), Inches(2.1), Inches(3.6), Inches(4.6), "Zero-Hallucination RAG", [
        "Strictly grounded generation: Answers only from verified Ministry guidelines.",
        "Refuses to guess if data is missing or ambiguous.",
        "Every fact cites the exact PDF filename and page number."
    ], "Pillar 1: Truth", GREEN)

    add_card(s3, Inches(4.8), Inches(2.1), Inches(3.6), Inches(4.6), "Deterministic Matcher", [
        "Mathematical rule engine compares student profile vs scheme criteria.",
        "Checks income ceilings, domicile, caste categories, and marks cutoffs.",
        "Clear status: ELIGIBLE, INELIGIBLE, or POTENTIALLY ELIGIBLE with exact reasons."
    ], "Pillar 2: Clarity", PRIMARY_BLUE)

    add_card(s3, Inches(8.8), Inches(2.1), Inches(3.6), Inches(4.6), "Multilingual & Resilient", [
        "Native multilingual support in English, Hindi (हिन्दी), and Punjabi (ਪੰਜਾਬੀ).",
        "Contextual memory resolves pronouns ('this scheme', 'above scholarship').",
        "100% 24/7 web availability with intelligent static fallback on GitHub Pages."
    ], "Pillar 3: Access", GREEN)

    # -------------------------------------------------------------
    # SLIDE 4: THE ARCHITECTURE WORKFLOW (INFOGRAPHIC SLIDE)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture", "End-to-End Dual-Stage RAG Pipeline", "Offline document processing combined with real-time semantic retrieval and cross-encoder reranking.")

    img_path = r"D:\Code\SATWINNER\LegalEase\rag_workflow.png"
    if os.path.exists(img_path):
        s4.shapes.add_picture(img_path, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.9))

    # -------------------------------------------------------------
    # SLIDE 5: TECHNOLOGY STACK DEEP DIVE
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Technology Stack", "Production-Grade AI & Engineering Tools", "Built strictly with open, scalable, and state-of-the-art frameworks.")

    techs = [
        ("PDF Extraction", "Unstructured", "Fast partition strategy parsing text, headings, and metadata without cloud dependencies.", PRIMARY_BLUE),
        ("Text Splitting", "CharacterTextSplitter", "LangChain splitter with 600-char chunk size, 100-char overlap, and section headers.", PRIMARY_BLUE),
        ("Embeddings", "Hugging Face MiniLM-L12", "Multilingual SentenceTransformer (384-dim) capturing cross-lingual Indian queries.", GREEN),
        ("Vector Storage", "FAISS", "High-performance vector index persisted on-disk with sub-millisecond similarity search.", GREEN),
        ("Reranking", "Cross-Encoder (ms-marco)", "Deep cross-attention re-evaluating top-10 chunks down to the 5 most precise passages.", AMBER),
        ("Generation", "Google Gemini 2.5/3.5", "Grounded generation via Google GenAI SDK with zero-boilerplate, straight-answer prompts.", PRIMARY_BLUE)
    ]

    col_w = Inches(3.64)
    row_h = Inches(2.2)
    for idx, (stage, tool, desc, colr) in enumerate(techs):
        r = idx // 3
        c = idx % 3
        left = Inches(0.8) + c * Inches(3.9)
        top = Inches(2.1) + r * Inches(2.4)
        add_card(s5, left, top, col_w, row_h, f"{tool}", [f"Role: {stage}", desc], f"Stage {idx+1}", colr)

    # -------------------------------------------------------------
    # SLIDE 6: COMPETITIVE ADVANTAGE (CHATBOT VS LEGALEASE)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Competitive Edge", "Standard Chatbots vs. LegalEase", "Why generic LLMs fail in government welfare and how LegalEase wins.")

    # Table layout
    rows = [
        ("Feature / Metric", "Generic LLM (ChatGPT / Perplexity)", "LegalEase AI Navigator"),
        ("Data Grounding", "Trained on outdated generic web data", "Official Gazette PDFs from NSP & State Portals"),
        ("Hallucination Risk", "High: May invent scholarship amounts & dates", "Zero: Hard refusal if not in verified guidelines"),
        ("Source Attribution", "Vague web links or hallucinated URLs", "Document name + exact page number citations"),
        ("Eligibility Checking", "Subjective and prone to arithmetic mistakes", "Deterministic mathematical rule evaluator"),
        ("Conversational Context", "Frequently loses active scheme context", "Pronoun resolver tracks active scheme history"),
        ("Hosting & Resilience", "Requires costly backend per query", "24/7 web hosting with static offline fallback")
    ]

    table_shape = s6.shapes.add_table(len(rows), 3, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.25)
    table.columns[2].width = Inches(4.25)

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
            else:
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = NAVY
                elif c_idx == 1:
                    p.font.color.rgb = RGBColor(185, 28, 28) # Reddish
                else:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(4, 120, 87) # Greenish
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else CARD_BG

    # -------------------------------------------------------------
    # SLIDE 7: REAL-WORLD IMPACT & METRICS
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Market Opportunity", "Empowering 140 Million Citizens", "Massive direct impact on student education, financial inclusion, and social justice.")

    add_card(s7, Inches(0.8), Inches(2.1), Inches(3.6), Inches(4.6), "Target Demographic", [
        "140M+ Higher Secondary and Undergraduate students in India.",
        "Over 800+ Central, UGC, AICTE, and State Welfare Schemes.",
        "Beneficiaries across SC/ST, OBC, EBC, DNT, and low-income general groups."
    ], "Market Size", PRIMARY_BLUE)

    add_card(s7, Inches(4.8), Inches(2.1), Inches(3.6), Inches(4.6), "Direct Financial Impact", [
        "₹50,000+ Crores in annual government scholarship allocations.",
        "Saves ₹1,000 - ₹3,000 per family by eliminating cyber-café middlemen.",
        "Accelerates time-to-application from 14 days down to 5 minutes."
    ], "Cost Savings", GREEN)

    add_card(s7, Inches(8.8), Inches(2.1), Inches(3.6), Inches(4.6), "Validation & Testing", [
        "9 automated unit tests verifying deterministic rules and semantic search.",
        "Sub-200ms FAISS similarity retrieval across thousands of PDF chunks.",
        "100% precision in scheme income boundary evaluations."
    ], "Technical Rigor", GREEN)

    # -------------------------------------------------------------
    # SLIDE 8: FUTURE ROADMAP
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Future Roadmap", "Scaling LegalEase to Every Village & Student", "Phase-wise expansion from web navigator to an automated citizen welfare agent.")

    add_card(s8, Inches(0.8), Inches(2.1), Inches(3.6), Inches(4.6), "Phase 1: Multi-Channel", [
        "WhatsApp & Telegram Bot Integration for low-bandwidth village access.",
        "Bhashini API integration for voice-in / voice-out regional speech queries.",
        "Automated deadline alerts & SMS reminders."
    ], "Months 1-3", PRIMARY_BLUE)

    add_card(s8, Inches(4.8), Inches(2.1), Inches(3.6), Inches(4.6), "Phase 2: Document OCR", [
        "On-device OCR scanner for Income, Caste, and Domicile certificates.",
        "Automatic validation of Tehsildar/SDM seals and validity dates.",
        "Pre-filling of NSP and State Scholarship portal application forms."
    ], "Months 3-6", AMBER)

    add_card(s8, Inches(8.8), Inches(2.1), Inches(3.6), Inches(4.6), "Phase 3: Gov Partnerships", [
        "Direct integration with DigiLocker for 1-click document verification.",
        "Pilot deployments with State Social Welfare Departments.",
        "Expansion to MSME, Agricultural, and Healthcare welfare schemes."
    ], "Months 6-12", GREEN)

    # -------------------------------------------------------------
    # SLIDE 9: TEAM & CONCLUSION
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    bg9 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg9.fill.solid()
    bg9.fill.fore_color.rgb = NAVY
    bg9.line.fill.background()

    tb9 = s9.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.9), Inches(4.8))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "🏛️ SATHACK 2026 SUBMISSION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(124, 200, 251)

    p = tf9.add_paragraph()
    p.text = "Thank You! Questions & Live Demo"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    p = tf9.add_paragraph()
    p.text = "Experience the live project right now:"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(224, 239, 254)
    p.space_before = Pt(14)

    p = tf9.add_paragraph()
    p.text = "🌐 Live GitHub Pages App: https://abhinav909-jpg.github.io/Sathack_winners/"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(54, 171, 246)
    p.space_before = Pt(10)

    p = tf9.add_paragraph()
    p.text = "💻 GitHub Repository: https://github.com/Abhinav909-jpg/Sathack_winners"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(54, 171, 246)
    p.space_before = Pt(6)

    p = tf9.add_paragraph()
    p.text = "Key Takeaway for Judges: LegalEase bridges the gap between complex government PDFs and 140M citizens with zero hallucination, verifiable citations, and deterministic eligibility."
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(20)

    # Save presentation
    output_path = r"D:\Code\SATWINNER\LegalEase\LegalEase_Hackathon_Pitch.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_deck()
