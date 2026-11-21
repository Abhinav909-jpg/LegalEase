import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_high_visibility_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE: LIGHT THEME WITH STRATEGIC DARK BLUE ACCENTS ---
    BG_LIGHT = RGBColor(245, 247, 250)         # #F5F7FA Soft Cool Off-White
    CARD_WHITE = RGBColor(255, 255, 255)       # #FFFFFF Pure White Card
    CARD_BORDER = RGBColor(203, 213, 225)      # #CBD5E1 High-visibility border
    
    # Dark Blue Elements
    DARK_BLUE = RGBColor(11, 37, 69)           # #0B2545 Deep Majestic Navy
    NAVY_SURFACE = RGBColor(19, 47, 81)        # #132F51 Rich Navy Card
    NAVY_LIGHT = RGBColor(224, 239, 254)       # #E0EFFE Soft Ice Blue
    
    # Typography Colors (Maximum Contrast & Readability)
    TEXT_DARK = RGBColor(15, 23, 42)           # #0F172A Pitch Dark Slate for body
    TEXT_MUTED = RGBColor(71, 85, 105)         # #475569 Clear Subtitle
    TEXT_WHITE = RGBColor(255, 255, 255)       # #FFFFFF High-Contrast White
    TEXT_CYAN = RGBColor(56, 189, 248)         # #38BDF8 Bright Cyan on Navy
    TEXT_GREEN = RGBColor(4, 120, 87)          # #047857 Dark Emerald Green
    TEXT_RED = RGBColor(185, 28, 28)           # #B91C1C High-contrast Dark Red
    TEXT_AMBER = RGBColor(180, 83, 9)          # #B45309 Warm Amber

    # Complementary Font Hierarchy
    FONT_HEADINGS = "Trebuchet MS"             # Distinct, modern, bold headings
    FONT_BODY = "Segoe UI"                     # Maximum readability for body text

    def apply_background(slide):
        # 1. Soft Light Slate Base
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

        # 2. Top Dark Blue Branding Accent Bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = DARK_BLUE
        top_bar.line.fill.background()

        # 3. Bottom Subtle Accent Stripe
        bottom_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.35), Inches(11.733), Inches(0.04))
        bottom_bar.fill.solid()
        bottom_bar.fill.fore_color.rgb = RGBColor(218, 226, 237)
        bottom_bar.line.fill.background()

        return bg

    def add_slide_header(slide, tag_text, bold_title, subtitle=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category Tag Badge in Dark Blue
        p0 = tf.paragraphs[0]
        p0.text = f"  {tag_text.upper()}  "
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = DARK_BLUE

        # Big Bold Title (28pt)
        p1 = tf.add_paragraph()
        p1.text = bold_title
        p1.font.name = FONT_HEADINGS
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = DARK_BLUE
        p1.space_before = Pt(4)

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = FONT_BODY
            p2.font.size = Pt(14)
            p2.font.bold = False
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(3)

    def add_light_card(slide, left, top, width, height, title, items, tag="", tag_color=DARK_BLUE, highlight_top=False):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_WHITE
        card.line.color.rgb = DARK_BLUE if highlight_top else CARD_BORDER
        card.line.width = Pt(2.0 if highlight_top else 1.25)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.28)
        tf.margin_bottom = Inches(0.25)

        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = tag.upper()
            p_tag.font.name = FONT_BODY
            p_tag.font.size = Pt(10.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = tag_color

            p_title = tf.add_paragraph()
            p_title.text = title
            p_title.font.name = FONT_HEADINGS
            p_title.font.size = Pt(18)
            p_title.font.bold = True
            p_title.font.color.rgb = DARK_BLUE
            p_title.space_before = Pt(4)
        else:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_HEADINGS
            p_title.font.size = Pt(18)
            p_title.font.bold = True
            p_title.font.color.rgb = DARK_BLUE

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = FONT_BODY
            p.font.size = Pt(13)          # Large, crisp body font!
            p.font.color.rgb = TEXT_DARK  # 100% visible dark text!
            p.space_before = Pt(7)

        return card

    def add_dark_blue_card(slide, left, top, width, height, title, items, tag=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_BLUE
        card.line.color.rgb = RGBColor(14, 165, 233)
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.28)
        tf.margin_bottom = Inches(0.25)

        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = tag.upper()
            p_tag.font.name = FONT_BODY
            p_tag.font.size = Pt(10.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = TEXT_CYAN

            p_title = tf.add_paragraph()
            p_title.text = title
            p_title.font.name = FONT_HEADINGS
            p_title.font.size = Pt(18)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_WHITE
            p_title.space_before = Pt(4)
        else:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_HEADINGS
            p_title.font.size = Pt(18)
            p_title.font.bold = True
            p_title.font.color.rgb = TEXT_WHITE

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = FONT_BODY
            p.font.size = Pt(13)
            p.font.color.rgb = RGBColor(226, 232, 240)
            p.space_before = Pt(7)

        return card

    # =========================================================================
    # SLIDE 1: TITLE & PURPOSE (DARK BLUE HERO CARD + CRISP STATS)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    # Hero Card in Majestic Dark Blue
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(3.4))
    hero.fill.solid()
    hero.fill.fore_color.rgb = DARK_BLUE
    hero.line.color.rgb = RGBColor(14, 165, 233)
    hero.line.width = Pt(1.5)

    htf = hero.text_frame
    htf.word_wrap = True
    htf.margin_left = Inches(0.55)
    htf.margin_top = Inches(0.4)
    htf.margin_right = Inches(0.55)

    p0 = htf.paragraphs[0]
    p0.text = "SATHACK 2026 • AI FOR PUBLIC EMPOWERMENT & CIVIC TECH"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_CYAN

    p1 = htf.add_paragraph()
    p1.text = "LegalEase 🇮🇳"
    p1.font.name = FONT_HEADINGS
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_before = Pt(6)

    p2 = htf.add_paragraph()
    p2.text = "Government Services Made Simple for Everyone"
    p2.font.name = FONT_HEADINGS
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_CYAN
    p2.space_before = Pt(4)

    p3 = htf.add_paragraph()
    p3.text = "Our Purpose: Ensuring no eligible student in India misses out on their legitimate government welfare due to dense legal jargon, fake middlemen, or confusing application procedures."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_before = Pt(10)

    # 3 Stat Cards Below Hero (White cards with Dark Blue Bold Numbers)
    m_cards = [
        ("140M+ Citizens", "Students across India eligible for government scholarships.", DARK_BLUE),
        ("₹50,000+ Crore", "Annual welfare budget allocated by Central & State governments.", TEXT_AMBER),
        ("Zero Middlemen", "Direct, verified guidance with legal proof and exact citations.", TEXT_GREEN)
    ]
    card_w = Inches(3.64)
    card_h = Inches(2.35)
    for i, (m_title, m_desc, m_col) in enumerate(m_cards):
        left = Inches(0.8) + i * Inches(4.04)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.45), card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_WHITE
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1.5)

        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.35)
        ctf.margin_right = Inches(0.3)

        p = ctf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_HEADINGS
        p.font.size = Pt(24)           # Large bold metric
        p.font.bold = True
        p.font.color.rgb = m_col

        p_desc = ctf.add_paragraph()
        p_desc.text = m_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(13)       # Highly readable description
        p_desc.font.color.rgb = TEXT_DARK
        p_desc.space_before = Pt(8)

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM (LARGE CRISP FONTS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_slide_header(s2, "The Real-World Problem", "Government Benefits Exist, But Access Remains Difficult", "Why millions of eligible students fail to receive the financial aid meant for them.")

    add_light_card(s2, Inches(0.8), Inches(2.05), Inches(3.64), Inches(4.8), "Dense 80-Page Guidelines", [
        "Government policies are published as 40 to 80 page legalistic PDFs.",
        "Written in dense legal terminology that ordinary students cannot understand.",
        "Crucial income ceilings (₹2.5L vs ₹4.5L) are buried deep inside complex clauses.",
        "Result: Students assume they are not eligible and never apply."
    ], "Friction 01", TEXT_AMBER, highlight_top=True)

    add_light_card(s2, Inches(4.84), Inches(2.05), Inches(3.64), Inches(4.8), "Extortionate Middlemen", [
        "Uneducated families are forced to visit cyber-café brokers to apply.",
        "Brokers charge ₹500 to ₹2,000 per application just to type details.",
        "In many cases, unscrupulous agents take a commission from the student's scholarship grant.",
        "Result: Needy families lose a large chunk of their aid."
    ], "Friction 02", TEXT_AMBER, highlight_top=True)

    add_light_card(s2, Inches(8.88), Inches(2.05), Inches(3.64), Inches(4.8), "General AI Hallucinates", [
        "Students asking ChatGPT or generic bots receive fake or outdated information.",
        "Normal AI invents non-existent deadlines, wrong amounts, and fabricated rules.",
        "Zero proof: Normal chatbots cannot cite the exact PDF or page number.",
        "Result: Students submit wrong forms and get rejected."
    ], "Friction 03", TEXT_RED, highlight_top=True)

    # =========================================================================
    # SLIDE 3: OUR SOLUTION (FEATURING DARK BLUE CENTER CARD)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_slide_header(s3, "Our Solution", "One Platform. Clear Guidance. Easier Access.", "LegalEase turns complex government rules into clear, verified, and honest answers.")

    # Left Card (White)
    add_light_card(s3, Inches(0.8), Inches(2.05), Inches(3.64), Inches(4.8), "Exact Page-Level Citations", [
        "Every single factual answer includes the exact document name and page number.",
        "Students can verify the legal clause themselves or show it to college authorities.",
        "Includes direct links to the official National Scholarship Portal (NSP) and State portals.",
        "Result: Complete transparency with zero middlemen."
    ], "Pillar 01", DARK_BLUE)

    # Center Hero Card in Dark Blue for Visual Contrast!
    add_dark_blue_card(s3, Inches(4.84), Inches(2.0), Inches(3.64), Inches(4.9), "100% Grounded in Official PDFs", [
        "LegalEase never browses random internet blogs or guesses answers.",
        "It answers questions strictly using verified Gazette guidelines from Ministry portals.",
        "If a rule is not mentioned in the official document, it honestly says so instead of guessing.",
        "Result: Absolute trust and zero hallucination."
    ], "Core Innovation")

    # Right Card (White)
    add_light_card(s3, Inches(8.88), Inches(2.05), Inches(3.64), Inches(4.8), "Deterministic Rule Checking", [
        "A mathematical rule checker tests applicant income, state, caste, and academic marks.",
        "Clearly shows: ELIGIBLE, INELIGIBLE, or POTENTIALLY ELIGIBLE.",
        "Explains the exact reason if someone does not qualify and what they can do next.",
        "Result: Instant clarity in seconds."
    ], "Pillar 03", DARK_BLUE)

    # =========================================================================
    # SLIDE 4: THE PROCESS (CITIZEN JOURNEY IN 4 CARDS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_slide_header(s4, "Citizen Journey", "A Simple Process Designed Around Citizens", "From confusion to an approved application in 4 simple steps.")

    process_cards = [
        ("Step 1", "Ask in Any Language", [
            "The student types their question naturally in English, Hindi, or Punjabi.",
            "No need to know official legal terms or scheme acronyms."
        ], DARK_BLUE),
        ("Step 2", "Instant Search", [
            "LegalEase scans official government PDFs in less than 200 milliseconds.",
            "Finds the exact official clauses related to the student's question."
        ], DARK_BLUE),
        ("Step 3", "Rule Evaluation", [
            "The system mathematically verifies eligibility criteria (Income ≤ ₹2.5L, Category, State).",
            "Confirms if the student meets every strict legal requirement."
        ], DARK_BLUE),
        ("Step 4", "Clear Action Plan", [
            "Delivers a crisp, to-the-point answer with verified page citations.",
            "Gives a complete checklist of documents required to apply."
        ], TEXT_GREEN)
    ]
    sw = Inches(2.7)
    sh = Inches(4.8)
    for idx, (st_tag, st_title, st_items, st_col) in enumerate(process_cards):
        left = Inches(0.8) + idx * Inches(3.01)
        add_light_card(s4, left, Inches(2.05), sw, sh, st_title, st_items, st_tag, st_col, highlight_top=True)

    # =========================================================================
    # SLIDE 5: TECHNOLOGIES (6 CLEAN CARDS WITH BOLD LABELS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_slide_header(s5, "Technology Stack", "The Technologies We Used & Why We Chose Them", "Every tool was carefully chosen to ensure speed, accuracy, and zero hallucination.")

    tech_items = [
        ("PDF Extraction", "Unstructured", "Reads and cleans complex government PDF guidelines, extracting text and tables cleanly.", DARK_BLUE),
        ("Text Splitting", "CharacterTextSplitter", "Splits policies into 600-character chunks with 100-character overlap to keep sentences complete.", DARK_BLUE),
        ("Embeddings", "Hugging Face MiniLM", "Converts sentences into 384-dimensional mathematical vectors to search by meaning rather than exact words.", DARK_BLUE),
        ("Vector Storage", "FAISS (Meta)", "An ultra-fast vector search library that searches through thousands of PDF chunks in sub-milliseconds.", DARK_BLUE),
        ("Reranking", "Cross-Encoder", "A smart second-stage filter that re-evaluates candidate paragraphs to pick only the exact answer.", TEXT_AMBER),
        ("Generation", "Google Gemini", "Generates crisp, direct answers using only the retrieved paragraphs with strict zero-guess rules.", TEXT_GREEN)
    ]
    tw = Inches(3.64)
    th = Inches(2.28)
    for idx, (role, name, desc, colr) in enumerate(tech_items):
        r = idx // 3
        c = idx % 3
        left = Inches(0.8) + c * Inches(4.04)
        top = Inches(2.05) + r * Inches(2.52)
        add_light_card(s5, left, top, tw, th, name, [f"Purpose: {role}", desc], f"Stage 0{idx+1}", colr, highlight_top=(idx>=3))

    # =========================================================================
    # SLIDE 6: COMPARATIVE ADVANTAGE (DARK BLUE TABLE HEADER)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_slide_header(s6, "Competitive Edge", "Why LegalEase Beats General AI & Official Portals", "The critical difference between guessing and verified legal accuracy.")

    table_data = [
        ("Feature", "Normal Chatbot (ChatGPT / Claude)", "LegalEase AI Navigator"),
        ("Where it gets data", "Trained on outdated generic internet text", "Verified Gazette PDFs directly from NSP & Ministries"),
        ("Risk of false info", "High — Often hallucinates deadlines & amounts", "Zero — Refuses to answer if fact is not in the PDF"),
        ("Source proof", "Vague links or completely made-up URLs", "Exact PDF document name and page number"),
        ("Checking eligibility", "Unreliable text guesses; prone to math errors", "Strict mathematical comparator with pass/fail reasons"),
        ("Remembering context", "Frequently forgets which scheme you asked about", "Pronoun resolver tracks 'this scheme' across messages"),
        ("Availability", "Requires high-cost cloud servers per question", "Runs 24/7 on web with offline static fallback")
    ]

    t_shape = s6.shapes.add_table(len(table_data), 3, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.9))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(4.466)
    tbl.columns[2].width = Inches(4.466)

    for r_idx, r_row in enumerate(table_data):
        for c_idx, val in enumerate(r_row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(12.5)       # Bigger table text!
            if r_idx == 0:
                p.font.name = FONT_HEADINGS
                p.font.bold = True
                p.font.size = Pt(13.5)
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE # Majestic Dark Blue Table Header!
            else:
                if c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = DARK_BLUE
                elif c_idx == 1:
                    p.font.bold = False
                    p.font.color.rgb = TEXT_RED   # High-contrast readable red
                else:
                    p.font.bold = True
                    p.font.color.rgb = TEXT_GREEN # High-contrast readable green
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD_WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)

    # =========================================================================
    # SLIDE 7: LIVE DEMO & FUTURE (DARK BLUE DEMO HERO CARD + CLEAN WHITE ROADMAP)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_slide_header(s7, "Conclusion & Live Demo", "Working Today, Ready to Scale Tomorrow", "A live, functional platform ready to empower students immediately.")

    # Left Hero Card in Deep Navy Dark Blue
    add_dark_blue_card(s7, Inches(0.8), Inches(2.05), Inches(5.6), Inches(4.8), "Experience The Live App", [
        "Live Website: https://abhinav909-jpg.github.io/Sathack_winners/",
        "GitHub Repository: https://github.com/Abhinav909-jpg/Sathack_winners",
        "Full-Stack Tested: 9 automated unit tests verifying retrieval and eligibility rules.",
        "Zero-Downtime Architecture: Works 24/7 on CDN edges with built-in client-side grounding.",
        "Try Asking: 'What is the parental income limit for Central Sector Scholarship?' to see exact page citations!"
    ], "Live Now")

    # Right Card in Pure White with Dark Blue Title
    add_light_card(s7, Inches(6.8), Inches(2.05), Inches(5.733), Inches(4.8), "Our Next Steps for Growth", [
        "WhatsApp & Telegram Bot: Bringing scheme navigation directly to low-end smartphones in villages.",
        "Voice Navigation in 12 Languages: Integrating Bhashini voice AI so illiterate citizens can simply speak their queries.",
        "On-Device Document Scanner: Point phone camera at an income or caste certificate to automatically check validity and Tehsildar seals.",
        "DigiLocker Integration: 1-click verified document import directly into government scholarship application forms."
    ], "Roadmap", DARK_BLUE, highlight_top=True)

    # Save to both file names so whichever the user opens, it's ready!
    target_files = [
        r"D:\Code\SATWINNER\LegalEase\LegalEase_High_Visibility_Presentation.pptx",
        r"D:\Code\SATWINNER\LegalEase\LegalEase_Presentation.pptx"
    ]
    for out_path in target_files:
        try:
            prs.save(out_path)
            print(f"Successfully saved to: {out_path}")
        except Exception as e:
            print(f"Could not overwrite {out_path} (likely open in PowerPoint): {e}")

if __name__ == "__main__":
    build_high_visibility_deck()
