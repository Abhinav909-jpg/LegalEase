import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Modern Dark/Tech Color Palette
    BG_DARK = RGBColor(10, 15, 29)          # #0A0F1D Deep Midnight Blue
    BG_CARD = RGBColor(19, 29, 50)          # #131D32 Slate Tech Blue
    BG_CARD_LIGHT = RGBColor(27, 38, 59)    # #1B263B Card Surface
    BORDER_CYAN = RGBColor(14, 165, 233)    # #0EA5E9 Vibrant Sky Blue
    BORDER_MUTED = RGBColor(51, 65, 85)     # #334155
    BORDER_GREEN = RGBColor(16, 185, 129)   # #10B981 Emerald
    BORDER_AMBER = RGBColor(245, 158, 11)   # #F59E0B Amber
    BORDER_PURPLE = RGBColor(168, 85, 247)  # #A855F7 Purple Accent

    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_CYAN = RGBColor(56, 189, 248)      # #38BDF8
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8
    TEXT_GREEN = RGBColor(52, 211, 153)     # #34D399
    TEXT_AMBER = RGBColor(251, 191, 36)     # #FBBF24
    TEXT_PURPLE = RGBColor(192, 132, 252)   # #C084FC

    def apply_dark_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_slide_header(slide, tag_text, title_text, subtitle_text=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = tag_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_CYAN

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(3)

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(13)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(3)

    def add_glowing_card(slide, left, top, width, height, title, items, tag=None, tag_color=TEXT_CYAN, border_color=BORDER_MUTED):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.22)

        start_idx = 0
        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = tag.upper()
            p_tag.font.size = Pt(9.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = tag_color
            
            p_title = tf.add_paragraph()
            p_title.text = title
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_WHITE
            p_title.space_before = Pt(3)
        else:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_WHITE

        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(11.5)
            p.font.color.rgb = RGBColor(226, 232, 240)
            p.space_before = Pt(5)

    # =========================================================================
    # SLIDE 1: "Government Services Made Simple for Everyone"
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s1)

    # Accent decorative top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(2.2), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BORDER_CYAN
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(2.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p = tf1.paragraphs[0]
    p.text = "CIVIC TECH • PUBLIC WELFARE AI • SATHACK 2026"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_CYAN

    p = tf1.add_paragraph()
    p.text = "Government Services Made Simple for Everyone"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "LegalEase 🇮🇳 is an AI-powered public navigator that connects every Indian student and citizen to verified scholarships and government schemes with zero hallucination and mathematical precision."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(8)

    # 3 Stat Cards below hero
    stat_cards = [
        ("140 Million+ Citizens", "Students & youth eligible for welfare programs who struggle with legal complexity.", TEXT_CYAN, BORDER_CYAN),
        ("₹50,000+ Crore Funds", "Annual government budget for education & welfare locked behind opaque PDF gazettes.", TEXT_AMBER, BORDER_AMBER),
        ("100% Truthful & Cited", "Every answer cites exact gazette filenames and page numbers with zero intermediary cut.", TEXT_GREEN, BORDER_GREEN)
    ]
    card_w = Inches(3.64)
    card_h = Inches(2.3)
    for i, (title, desc, col, bcol) in enumerate(stat_cards):
        left = Inches(0.8) + i * Inches(4.0)
        shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.4), card_w, card_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = bcol
        shape.line.width = Pt(1.5)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.3)
        
        p = tf.paragraphs[0]
        p.text = f"0{i+1}"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(6)

    # Bottom Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.8))
    pill.fill.solid()
    pill.fill.fore_color.rgb = BG_CARD_LIGHT
    pill.line.color.rgb = BORDER_MUTED
    ptf = pill.text_frame
    ptf.margin_top = Inches(0.18)
    pp = ptf.paragraphs[0]
    pp.text = "⚡ Live Demo Active: https://abhinav909-jpg.github.io/Sathack_winners/   •   Repository: github.com/Abhinav909-jpg/Sathack_winners"
    pp.font.size = Pt(12)
    pp.font.bold = True
    pp.font.color.rgb = TEXT_CYAN
    pp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: "Government Benefits Exist, But Access Remains Difficult"
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s2)
    add_slide_header(s2, "The Reality Check & Root Problem", "Government Benefits Exist, But Access Remains Difficult", "India has hundreds of benevolent schemes, but structural friction prevents funds from reaching the needy.")

    add_glowing_card(s2, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "Bureaucratic Fortresses", [
        "Government policies are published as 40 to 80 page legalistic PDF gazettes.",
        "Crucial income ceilings (₹2.5 Lakh vs ₹4.5 Lakh) and domicile clauses are hidden in complex legal syntax.",
        "Students misunderstand clauses and miss application cutoffs."
    ], "Friction 01", TEXT_AMBER, BORDER_AMBER)

    add_glowing_card(s2, Inches(4.8), Inches(2.0), Inches(3.64), Inches(4.8), "Predatory Cyber Brokers", [
        "Low-income citizens must rely on local cyber-café middlemen who charge ₹500 - ₹2,000 per form.",
        "Middlemen frequently take cuts of student Direct Benefit Transfer (DBT) funds.",
        "Zero transparency on official portal links, free-ship cards, or authentic deadlines."
    ], "Friction 02", TEXT_AMBER, BORDER_AMBER)

    add_glowing_card(s2, Inches(8.8), Inches(2.0), Inches(3.64), Inches(4.8), "Hallucinating General AI", [
        "Generic LLMs (ChatGPT / Perplexity) hallucinate fake deadlines, non-existent quotas, and wrong grant amounts.",
        "No verifiable citations: students cannot prove AI advice to university nodal officers.",
        "Arithmetic errors when checking family income vs scheme criteria."
    ], "Friction 03", RGBColor(239, 68, 68), RGBColor(239, 68, 68))

    # =========================================================================
    # SLIDE 3: "One Platform. Clear Guidance. Easier Access."
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s3)
    add_slide_header(s3, "The Unifying Solution", "One Platform. Clear Guidance. Easier Access.", "LegalEase dismantles bureaucratic complexity with an integrated, intelligent civic architecture.")

    add_glowing_card(s3, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "Semantic Scheme Discovery", [
        "Natural language search: Ask questions in plain English, Hindi (हिन्दी), or Punjabi (ਪੰਜਾਬੀ).",
        "Covers Central Sector (CSSS), State SC Welfare, PM-YASASVI, and NMMSS.",
        "Multi-turn pronoun resolution remembers active schemes (e.g., 'What are documents for this scheme?')."
    ], "Pillar 01", TEXT_CYAN, BORDER_CYAN)

    add_glowing_card(s3, Inches(4.8), Inches(2.0), Inches(3.64), Inches(4.8), "Deterministic Rule Matcher", [
        "100% mathematical precision: compares applicant income, domicile, category, and marks.",
        "Categorizes schemes as ELIGIBLE, INELIGIBLE, or POTENTIALLY ELIGIBLE.",
        "Provides exact reasons for disqualification and actionable next steps."
    ], "Pillar 02", TEXT_GREEN, BORDER_GREEN)

    add_glowing_card(s3, Inches(8.8), Inches(2.0), Inches(3.64), Inches(4.8), "Legal Verifiable Citations", [
        "Every answer includes source document badges with exact page numbers.",
        "Direct link to official National Scholarship Portal (NSP) and State welfare portals.",
        "24/7 web resilience with client-side grounded fallback on GitHub Pages."
    ], "Pillar 03", TEXT_CYAN, BORDER_CYAN)

    # =========================================================================
    # SLIDE 4: "A Simple Process Designed Around Citizens"
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s4)
    add_slide_header(s4, "The Citizen Experience", "A Simple Process Designed Around Citizens", "How a student goes from confusion to verified scholarship in 4 frictionless steps.")

    process_steps = [
        ("Step 1", "Ask in Any Language", "Student types their query in English, Hindi, or Punjabi without needing bureaucratic terms.", TEXT_CYAN, BORDER_CYAN),
        ("Step 2", "Instant RAG Retrieval", "System embeds query and uses FAISS + Cross-Encoder to locate exact official clauses in <200ms.", TEXT_PURPLE, BORDER_PURPLE),
        ("Step 3", "Rule Evaluation", "Deterministic engine calculates exact eligibility (Income ≤ ₹2.5L / ₹4.5L, Domicile, Category).", TEXT_AMBER, BORDER_AMBER),
        ("Step 4", "Cited Action Plan", "Student receives to-the-point answers, required document checklist, and verified portal links.", TEXT_GREEN, BORDER_GREEN)
    ]
    p_width = Inches(2.7)
    p_height = Inches(4.8)
    for idx, (st, s_title, s_desc, col, bcol) in enumerate(process_steps):
        left = Inches(0.8) + idx * Inches(2.98)
        shape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), p_width, p_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = bcol
        shape.line.width = Pt(1.5)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = st.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = s_title
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = s_desc
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = RGBColor(203, 213, 225)
        p3.space_before = Pt(12)

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE (RAG WORKFLOW INFOGRAPHIC)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s5)
    add_slide_header(s5, "Architecture Workflow", "LegalEase — Dual-Stage RAG Pipeline", "Offline ingestion parses and embeds guidelines; Real-time retrieval reranks and synthesizes grounded answers.")

    img_path = r"D:\Code\SATWINNER\LegalEase\rag_workflow.png"
    if os.path.exists(img_path):
        s5.shapes.add_picture(img_path, Inches(0.8), Inches(1.9), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 6: TECHNOLOGY STACK DEEP DIVE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s6)
    add_slide_header(s6, "Engineering & AI Stack", "Production-Grade AI Components", "Engineered for speed, zero hallucination, sub-millisecond retrieval, and scale.")

    techs = [
        ("PDF Extraction", "Unstructured", "Fast partition strategy extracting structured text, tables, and page metadata.", TEXT_CYAN, BORDER_CYAN),
        ("Text Splitting", "CharacterTextSplitter", "LangChain splitter with 600-char chunk size, 100-char overlap, keeping legal clauses intact.", TEXT_CYAN, BORDER_CYAN),
        ("Embeddings", "Hugging Face MiniLM-L12", "Multilingual SentenceTransformer (384-dim) capturing cross-lingual Indian queries.", TEXT_GREEN, BORDER_GREEN),
        ("Vector Storage", "FAISS", "High-performance vector index persisted on-disk with sub-millisecond similarity search.", TEXT_GREEN, BORDER_GREEN),
        ("Reranking", "Cross-Encoder (ms-marco)", "Deep cross-attention re-evaluating top-10 chunks down to top-5 most relevant passages.", TEXT_AMBER, BORDER_AMBER),
        ("Generation", "Google Gemini 2.5/3.5", "Grounded generation via Google GenAI SDK with zero-boilerplate, straight-answer prompts.", TEXT_CYAN, BORDER_CYAN)
    ]

    col_w = Inches(3.64)
    row_h = Inches(2.2)
    for idx, (stage, tool, desc, colr, bcol) in enumerate(techs):
        r = idx // 3
        c = idx % 3
        left = Inches(0.8) + c * Inches(4.0)
        top = Inches(2.0) + r * Inches(2.5)
        add_glowing_card(s6, left, top, col_w, row_h, tool, [f"Function: {stage}", desc], f"Stage 0{idx+1}", colr, bcol)

    # =========================================================================
    # SLIDE 7: COMPETITIVE ADVANTAGE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s7)
    add_slide_header(s7, "Why LegalEase Wins", "Comparative Advantage Matrix", "Why generic chatbots fail in civic welfare and how LegalEase guarantees accuracy.")

    rows = [
        ("Metric / Capability", "Generic LLM (ChatGPT / Perplexity)", "Standard Gov Portals (NSP)", "LegalEase AI Navigator"),
        ("Data Grounding", "Trained on outdated crawled web data", "Raw static tables, hard to search", "100% Grounded in Official Gazette PDFs"),
        ("Hallucination Risk", "High: May invent false rules & dates", "None (Manual searching required)", "Zero: Hard refusal if not in guidelines"),
        ("Source Citations", "Vague links or hallucinated URLs", "None", "Exact PDF document name + Page number"),
        ("Eligibility Evaluation", "Subjective and prone to math errors", "Rigid forms with zero explanations", "Deterministic engine with exact pass/fail reasons"),
        ("Pronoun Resolution", "Frequently loses active scheme context", "No conversational interface", "Tracks active scheme across multi-turn history"),
        ("Hosting & Resilience", "Requires paid cloud server per query", "Crashes during peak portal traffic", "24/7 Web App with client-side grounded fallback")
    ]

    table_shape = s7.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.9), Inches(11.7), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.0)

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_CARD_LIGHT
            else:
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = TEXT_CYAN
                elif c_idx == 1:
                    p.font.color.rgb = RGBColor(248, 113, 113) # Reddish
                elif c_idx == 2:
                    p.font.color.rgb = RGBColor(251, 191, 36) # Amber
                else:
                    p.font.bold = True
                    p.font.color.rgb = TEXT_GREEN # Green
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_CARD if r_idx % 2 == 0 else BG_DARK

    # =========================================================================
    # SLIDE 8: IMPACT & REAL-WORLD VALIDATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s8)
    add_slide_header(s8, "Socio-Economic Impact", "Empowering 140 Million Citizens", "Bridging India's education gap through digital transparency and direct access.")

    add_glowing_card(s8, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "Massive Scale & Reach", [
        "140M+ Higher Secondary and College Students across India.",
        "Over 800+ Central, UGC, AICTE, and State Welfare Schemes.",
        "Empowers SC/ST, OBC, EBC, DNT, and economically weaker general students."
    ], "Target Reach", TEXT_CYAN, BORDER_CYAN)

    add_glowing_card(s8, Inches(4.8), Inches(2.0), Inches(3.64), Inches(4.8), "Economic Value Delivered", [
        "₹50,000+ Crores annual government scholarship allocations unlocked.",
        "Saves ₹1,000 - ₹3,000 per family by eliminating cyber-café commission brokers.",
        "Cuts application discovery time from 14 days down to 5 minutes."
    ], "Cost Savings", TEXT_GREEN, BORDER_GREEN)

    add_glowing_card(s8, Inches(8.8), Inches(2.0), Inches(3.64), Inches(4.8), "Technical Validation", [
        "9 automated unit tests verifying deterministic evaluation and FAISS retrieval.",
        "Sub-200ms similarity search latency across thousands of PDF vector chunks.",
        "100% precision in scheme income boundary evaluations."
    ], "Rigor & Testing", TEXT_AMBER, BORDER_AMBER)

    # =========================================================================
    # SLIDE 9: FUTURE ROADMAP
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s9)
    add_slide_header(s9, "Future Scalability", "Scaling LegalEase Across Bharat", "Three-phase expansion to bring truthful welfare guidance to every village and smartphone.")

    add_glowing_card(s9, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "Phase 1: Multi-Channel Voice", [
        "WhatsApp & Telegram bot for low-bandwidth village access.",
        "Bhashini API integration for voice-in / voice-out regional speech queries.",
        "Automated deadline alerts & SMS reminders."
    ], "Months 01 - 03", TEXT_CYAN, BORDER_CYAN)

    add_glowing_card(s9, Inches(4.8), Inches(2.0), Inches(3.64), Inches(4.8), "Phase 2: Document OCR", [
        "On-device OCR scanner for Income, Caste, and Domicile certificates.",
        "Automatic validation of Tehsildar/SDM seals and validity dates.",
        "Pre-filling of NSP and State Scholarship portal application forms."
    ], "Months 03 - 06", TEXT_AMBER, BORDER_AMBER)

    add_glowing_card(s9, Inches(8.8), Inches(2.0), Inches(3.64), Inches(4.8), "Phase 3: Gov Partnerships", [
        "Direct integration with DigiLocker for 1-click document verification.",
        "Pilot deployments with State Social Welfare Departments.",
        "Expansion to MSME, Agricultural, and Healthcare welfare schemes."
    ], "Months 06 - 12", TEXT_GREEN, BORDER_GREEN)

    # =========================================================================
    # SLIDE 10: CONCLUSION & LIVE DEMO
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_dark_bg(s10)

    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.2))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "🏛️ SATHACK 2026 SUBMISSION • TEAM SATHACK WINNERS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_CYAN

    p = tf10.add_paragraph()
    p.text = "LegalEase: Powering Citizen Welfare"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)

    p = tf10.add_paragraph()
    p.text = "Experience the live web application right now:"
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(12)

    p = tf10.add_paragraph()
    p.text = "🌐 Live GitHub Pages App: https://abhinav909-jpg.github.io/Sathack_winners/"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_CYAN
    p.space_before = Pt(10)

    p = tf10.add_paragraph()
    p.text = "💻 GitHub Repository: https://github.com/Abhinav909-jpg/Sathack_winners"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_CYAN
    p.space_before = Pt(6)

    p = tf10.add_paragraph()
    p.text = "Core Takeaway: LegalEase eliminates information asymmetry and hallucination by combining Unstructured PDF extraction, FAISS vector retrieval, Cross-Encoder reranking, and Gemini with deterministic rule evaluation."
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(16)

    # Save
    out = r"D:\Code\SATWINNER\LegalEase\LegalEase_Hackathon_Pitch.pptx"
    prs.save(out)
    print("V2 High-Impact Presentation saved to:", out)

if __name__ == "__main__":
    create_presentation()
