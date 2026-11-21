import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_minimalist_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- UNIFORM LIGHT THEME PALETTE ---
    BG_LIGHT = RGBColor(248, 250, 252)       # #F8FAFC Soft Slate White
    CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF Pure White
    CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0 Subtle Border
    
    PRIMARY_BLUE = RGBColor(2, 112, 199)    # #0270C7 Brand Primary Blue
    DEEP_NAVY = RGBColor(15, 23, 42)         # #0F172A Bold Dark Heading
    TEXT_BODY = RGBColor(51, 65, 85)         # #334155 Clean Body Text
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B Subtitle Text
    
    ACCENT_TEAL = RGBColor(13, 148, 136)     # #0D9488 Subtle Verification
    ACCENT_AMBER = RGBColor(217, 119, 6)     # #D97706 Warning/Problem
    ACCENT_RED = RGBColor(220, 38, 38)       # #DC2626 Problem Alert
    ACCENT_LINE = RGBColor(186, 224, 253)    # #BAE0FD Light Decorative Accent

    FONT_FAMILY = "Segoe UI"

    def apply_minimalist_background(slide):
        # 1. Base clean background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

        # 2. Subtle top gradient-like decorative strip (Minimalist Pattern)
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = PRIMARY_BLUE
        top_bar.line.fill.background()

        # 3. Soft decorative pattern element in bottom right (Minimalist geometric accent)
        accent_circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(12.2), Inches(6.4), Inches(1.8), Inches(1.8))
        accent_circle.fill.solid()
        accent_circle.fill.fore_color.rgb = RGBColor(241, 245, 249) # #F1F5F9
        accent_circle.line.fill.background()

        return bg

    def add_header(slide, category_tag, bold_heading, subtitle=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_tag.upper()
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_BLUE

        p1 = tf.add_paragraph()
        p1.text = bold_heading
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(25)
        p1.font.bold = True
        p1.font.color.rgb = DEEP_NAVY
        p1.space_before = Pt(4)

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(13)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(3)

    def add_card(slide, left, top, width, height, title, bullet_points, pill_tag=None, pill_color=PRIMARY_BLUE, highlight_border=False):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = PRIMARY_BLUE if highlight_border else CARD_BORDER
        card.line.width = Pt(1.5 if highlight_border else 1.0)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.28)
        tf.margin_right = Inches(0.28)
        tf.margin_top = Inches(0.28)
        tf.margin_bottom = Inches(0.28)

        if pill_tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = pill_tag.upper()
            p_tag.font.name = FONT_FAMILY
            p_tag.font.size = Pt(9.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = pill_color

            p_title = tf.add_paragraph()
            p_title.text = title
            p_title.font.name = FONT_FAMILY
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = DEEP_NAVY
            p_title.space_before = Pt(4)
        else:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_FAMILY
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = DEEP_NAVY

        for pt in bullet_points:
            p = tf.add_paragraph()
            p.text = f"•  {pt}"
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_BODY
            p.space_before = Pt(6)

        return card

    # =========================================================================
    # SLIDE 1: TITLE & PURPOSE (NOT BEGINNING WITH FEATURES)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s1)

    # Hero Banner Card
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(3.2))
    hero.fill.solid()
    hero.fill.fore_color.rgb = CARD_BG
    hero.line.color.rgb = CARD_BORDER
    hero.line.width = Pt(1.0)
    
    htf = hero.text_frame
    htf.word_wrap = True
    htf.margin_left = Inches(0.5)
    htf.margin_top = Inches(0.4)
    htf.margin_right = Inches(0.5)

    p = htf.paragraphs[0]
    p.text = "SATHACK 2026 • AI FOR PUBLIC EMPOWERMENT"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p = htf.add_paragraph()
    p.text = "LegalEase 🇮🇳"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = DEEP_NAVY
    p.space_before = Pt(6)

    p = htf.add_paragraph()
    p.text = "Government Services Made Simple for Everyone"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_before = Pt(4)

    p = htf.add_paragraph()
    p.text = "Our Purpose: Ensuring no eligible student in India misses out on their legitimate government welfare due to complex legal jargon, fake middlemen, or confusing application procedures."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(8)

    # 3 Simple Metric Cards
    m_data = [
        ("140M+ Citizens", "Students across India eligible for government scholarships.", PRIMARY_BLUE),
        ("₹50,000+ Crore", "Annual welfare budget allocated by Central & State governments.", ACCENT_AMBER),
        ("Zero Middlemen", "Direct, verified guidance with legal proof and exact citations.", ACCENT_TEAL)
    ]
    card_w = Inches(3.64)
    card_h = Inches(2.2)
    for i, (m_title, m_desc, m_col) in enumerate(m_data):
        left = Inches(0.8) + i * Inches(4.04)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.4), card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.0)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.3)
        ctf.margin_right = Inches(0.3)

        p = ctf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = m_col

        p2 = ctf.add_paragraph()
        p2.text = m_desc
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM (DESCRIBED SIMPLY)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s2)
    add_header(s2, "The Real-World Problem", "Government Benefits Exist, But Access Remains Difficult", "Why millions of eligible students fail to receive the financial aid meant for them.")

    add_card(s2, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "Dense 80-Page Guidelines", [
        "Official guidelines are published as 40 to 80 page legalistic PDFs.",
        "Written in dense legal terminology that ordinary students cannot understand.",
        "Crucial income limits (₹2.5 Lakh vs ₹4.5 Lakh) and category cutoffs are buried inside complex clauses.",
        "Result: Students assume they are not eligible and give up."
    ], "Friction 01", ACCENT_AMBER)

    add_card(s2, Inches(4.84), Inches(2.0), Inches(3.64), Inches(4.8), "Extortionate Middlemen", [
        "Uneducated families are forced to visit cyber-café brokers to apply.",
        "Brokers charge ₹500 to ₹2,000 per application just to type details.",
        "In many cases, unscrupulous agents take a commission from the student's scholarship grant.",
        "Result: Needy families lose a large chunk of their aid."
    ], "Friction 02", ACCENT_AMBER)

    add_card(s2, Inches(8.88), Inches(2.0), Inches(3.64), Inches(4.8), "General AI Hallucinates", [
        "Students asking ChatGPT or Perplexity often receive fake or outdated information.",
        "Generic AI invents non-existent deadlines, wrong amounts, and fabricated rules.",
        "Zero proof: Normal chatbots cannot cite the exact PDF or page number.",
        "Result: Students submit wrong forms and get rejected."
    ], "Friction 03", ACCENT_RED)

    # =========================================================================
    # SLIDE 3: OUR SOLUTION (WHAT LEGALEASE DOES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s3)
    add_header(s3, "Our Solution", "One Platform. Clear Guidance. Easier Access.", "LegalEase turns complex government rules into clear, verified, and honest answers.")

    add_card(s3, Inches(0.8), Inches(2.0), Inches(3.64), Inches(4.8), "100% Grounded in Official PDFs", [
        "LegalEase never browses random internet blogs or guess answers.",
        "It answers questions strictly using verified Gazette guidelines from Ministry portals.",
        "If a rule is not mentioned in the official document, it honestly says so instead of guessing.",
        "Result: Absolute trust and zero hallucination."
    ], "Pillar 01", PRIMARY_BLUE, highlight_border=True)

    add_card(s3, Inches(4.84), Inches(2.0), Inches(3.64), Inches(4.8), "Exact Page-Level Citations", [
        "Every single factual answer includes the exact document name and page number.",
        "Students can verify the legal clause themselves or show it to college authorities.",
        "Includes direct links to the official National Scholarship Portal (NSP) and State portals.",
        "Result: Full transparency with zero middlemen."
    ], "Pillar 02", ACCENT_TEAL)

    add_card(s3, Inches(8.88), Inches(2.0), Inches(3.64), Inches(4.8), "Deterministic Rule Evaluation", [
        "A mathematical rule checker tests applicant income, state, caste, and academic marks.",
        "Clearly shows: ELIGIBLE, INELIGIBLE, or POTENTIALLY ELIGIBLE.",
        "Explains the exact reason if someone does not qualify and what they can do next.",
        "Result: Instant clarity in seconds."
    ], "Pillar 03", PRIMARY_BLUE)

    # =========================================================================
    # SLIDE 4: THE SIMPLE PROCESS (CITIZEN JOURNEY)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s4)
    add_header(s4, "How It Works For The Citizen", "A Simple Process Designed Around Citizens", "From confusion to an approved application in 4 simple steps.")

    steps = [
        ("Step 1", "Ask in Any Language", [
            "The student types their question naturally in English, Hindi, or Punjabi.",
            "No need to know official legal terms or scheme acronyms."
        ], PRIMARY_BLUE),
        ("Step 2", "Instant Search", [
            "LegalEase scans official government PDFs in less than 200 milliseconds.",
            "Finds the exact official clauses related to the student's question."
        ], ACCENT_TEAL),
        ("Step 3", "Rule Check", [
            "The system mathematically verifies eligibility criteria (Income ≤ ₹2.5L, Category, State).",
            "Confirms if the student meets every strict legal requirement."
        ], ACCENT_AMBER),
        ("Step 4", "Clear Action Plan", [
            "Delivers a crisp, to-the-point answer with verified page citations.",
            "Gives a complete checklist of documents required to apply."
        ], PRIMARY_BLUE)
    ]
    sw = Inches(2.7)
    sh = Inches(4.8)
    for idx, (st_num, st_name, st_pts, st_col) in enumerate(steps):
        left = Inches(0.8) + idx * Inches(3.01)
        add_card(s4, left, Inches(2.0), sw, sh, st_name, st_pts, st_num, st_col)

    # =========================================================================
    # SLIDE 5: TECHNOLOGIES USED IN OUR PROJECT (EXPLAINED SIMPLY)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s5)
    add_header(s5, "Technology Stack", "The Technologies We Used & Why We Chose Them", "Every tool was carefully chosen to ensure speed, accuracy, and zero hallucination.")

    tech_stack = [
        ("PDF Extraction", "Unstructured", "Reads and cleans complex government PDF guidelines, extracting text and tables cleanly.", PRIMARY_BLUE),
        ("Text Splitting", "CharacterTextSplitter", "Splits long legal policies into 600-character chunks with 100-character overlap to keep sentences complete.", PRIMARY_BLUE),
        ("Embeddings", "Hugging Face MiniLM", "Converts sentences into 384-dimensional mathematical vectors so we can search by meaning rather than exact words.", ACCENT_TEAL),
        ("Vector Storage", "FAISS (Meta)", "An ultra-fast vector search library that searches through thousands of PDF chunks in sub-milliseconds.", ACCENT_TEAL),
        ("Reranking", "Cross-Encoder", "A smart second-stage filter that re-evaluates the top candidate paragraphs to select only the exact answer.", ACCENT_AMBER),
        ("Generation", "Google Gemini", "Generates crisp, direct answers using only the retrieved paragraphs with strict zero-guess rules.", PRIMARY_BLUE)
    ]
    tw = Inches(3.64)
    th = Inches(2.25)
    for idx, (role, name, desc, colr) in enumerate(tech_stack):
        r = idx // 3
        c = idx % 3
        left = Inches(0.8) + c * Inches(4.04)
        top = Inches(2.0) + r * Inches(2.5)
        add_card(s5, left, top, tw, th, name, [f"Purpose: {role}", desc], f"Component 0{idx+1}", colr)

    # =========================================================================
    # SLIDE 6: WHY THIS IS BETTER THAN A NORMAL CHATBOT
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s6)
    add_header(s6, "Competitive Advantage", "Why LegalEase Beats General AI & Official Portals", "The critical difference between guessing and verified legal accuracy.")

    comparison_rows = [
        ("Feature", "Normal Chatbot (ChatGPT / Claude)", "LegalEase AI Navigator"),
        ("Where it gets data", "Trained on outdated generic internet text", "Verified Gazette PDFs directly from NSP & Ministries"),
        ("Risk of false info", "High — Often hallucinates deadlines & amounts", "Zero — Refuses to answer if fact is not in the PDF"),
        ("Source proof", "Vague links or completely made-up URLs", "Exact PDF document name and page number"),
        ("Checking eligibility", "Unreliable text guesses; prone to math errors", "Strict mathematical comparator with pass/fail reasons"),
        ("Remembering context", "Frequently forgets which scheme you asked about", "Pronoun resolver tracks 'this scheme' across messages"),
        ("Availability", "Requires high-cost servers per question", "Runs 24/7 on web with offline static fallback")
    ]

    t_shape = s6.shapes.add_table(len(comparison_rows), 3, Inches(0.8), Inches(1.95), Inches(11.733), Inches(4.9))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(4.466)
    tbl.columns[2].width = Inches(4.466)

    for r_idx, r_data in enumerate(comparison_rows):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = DEEP_NAVY
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(226, 232, 240)
            else:
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = DEEP_NAVY
                elif c_idx == 1:
                    p.font.color.rgb = ACCENT_RED
                else:
                    p.font.bold = True
                    p.font.color.rgb = ACCENT_TEAL
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 0 else BG_LIGHT

    # =========================================================================
    # SLIDE 7: LIVE DEMO & WHAT'S NEXT
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_minimalist_background(s7)
    add_header(s7, "Conclusion & Live Demo", "Working Today, Ready to Scale Tomorrow", "A live, functional platform ready to empower students immediately.")

    # Left Card: Live Demo & Links
    add_card(s7, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Experience The Live App", [
        "Live Website: https://abhinav909-jpg.github.io/Sathack_winners/",
        "GitHub Repository: https://github.com/Abhinav909-jpg/Sathack_winners",
        "Full-Stack Tested: 9 automated unit tests verifying retrieval and eligibility rules.",
        "Zero-Downtime Architecture: Works 24/7 on CDN edges with built-in client-side grounding.",
        "Try Asking: 'What is the parental income limit for Central Sector Scholarship?' to see exact page citations!"
    ], "Live Now", PRIMARY_BLUE, highlight_border=True)

    # Right Card: What's Next
    add_card(s7, Inches(6.8), Inches(2.0), Inches(5.733), Inches(4.8), "Our Next Steps for Growth", [
        "WhatsApp & Telegram Bot: Bringing scheme navigation directly to low-end smartphones in villages.",
        "Voice Navigation in 12 Languages: Integrating Bhashini voice AI so illiterate citizens can simply speak their queries.",
        "On-Device Document Scanner: Point phone camera at an income or caste certificate to automatically check validity and Tehsildar seals.",
        "DigiLocker Integration: 1-click verified document import directly into government scholarship application forms."
    ], "Roadmap", ACCENT_TEAL)

    output_file = r"D:\Code\SATWINNER\LegalEase\LegalEase_Presentation.pptx"
    prs.save(output_file)
    print(f"Minimalist Light Deck created successfully at: {output_file}")

if __name__ == "__main__":
    build_minimalist_deck()
