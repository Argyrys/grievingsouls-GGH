from fpdf import FPDF

W, H = 254, 143          # 16:9 landscape in mm
M = 14                   # margin
BLACK = (12, 14, 20)
PANEL = (22, 26, 38)
CYAN = (0, 210, 215)
WHITE = (238, 238, 238)
GRAY = (130, 140, 155)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
AMBER = (245, 158, 11)

pdf = FPDF(orientation="P", unit="mm", format=(W, H))
pdf.set_auto_page_break(False)
pdf.set_margins(M, M, M)

def new_slide():
    pdf.add_page()
    pdf.set_fill_color(*BLACK)
    pdf.rect(0, 0, W, H, "F")
    pdf.set_fill_color(*PANEL)
    pdf.rect(0, 0, W, 10, "F")
    pdf.set_fill_color(*CYAN)
    pdf.rect(0, 10, W, 0.8, "F")
    pdf.set_text_color(*GRAY)
    pdf.set_font("helvetica", "B", 9)
    pdf.set_xy(M, 1.6)
    pdf.cell(40, 6, "Veritas Vision", ln=0)
    pdf.set_font("helvetica", "", 8)
    pdf.set_xy(W - M - 60, 2.1)
    pdf.cell(60, 6, "Google Gemini Hackathon  |  23 Oct 2026", align="R", ln=0)

def footer(n):
    pdf.set_text_color(*GRAY)
    pdf.set_font("helvetica", "", 8)
    pdf.set_xy(M, H - 7.5)
    pdf.cell(70, 5, "Team Grieving Souls  |  grievingsouls-GGH", ln=0)
    pdf.set_xy(W - M - 18, H - 7.5)
    pdf.cell(18, 5, f"{n:02d}", align="R", ln=0)

def title(text, sub=None):
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "B", 25)
    pdf.set_xy(M, 16)
    pdf.cell(W - 2 * M, 13, text, ln=0)
    if sub:
        pdf.set_text_color(*CYAN)
        pdf.set_font("helvetica", "", 12.5)
        pdf.set_xy(M, 30)
        pdf.multi_cell(W - 2 * M, 6.5, sub)

def body(text, y=44, size=11.5, color=WHITE, bold=False, line=6.0):
    pdf.set_text_color(*color)
    pdf.set_font("helvetica", "B" if bold else "", size)
    pdf.set_xy(M, y)
    pdf.multi_cell(W - 2 * M, line, text)

def items(texts, y=44, size=11, gap=7.2, color=WHITE, marker="- "):
    pdf.set_text_color(*color)
    pdf.set_font("helvetica", "", size)
    ypos = y
    for t in texts:
        pdf.set_xy(M, ypos)
        pdf.multi_cell(W - 2 * M, gap, marker + t)
        ypos += pdf.get_y() - ypos + 0  # multi_cell already moved cursor
        ypos = pdf.get_y()

def badge(x, y, w, h, text, fill, tcolor=WHITE, size=9):
    pdf.set_fill_color(*fill)
    pdf.rect(x, y, w, h, "F")
    pdf.set_text_color(*tcolor)
    pdf.set_font("helvetica", "B", size)
    pdf.set_xy(x + 2, y + 1.3)
    pdf.cell(w - 4, h - 2.6, text, ln=0)

# ---------------- Slide 1: Title ----------------
new_slide()
pdf.set_fill_color(*CYAN)
pdf.rect(M, 46, 3, 52, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("helvetica", "B", 40)
pdf.set_xy(M + 10, 30)
pdf.cell(0, 22, "Veritas Vision", ln=0)
pdf.set_text_color(*CYAN)
pdf.set_font("helvetica", "B", 16)
pdf.set_xy(M + 10, 56)
pdf.cell(0, 9, "Multimodal Phishing Detector", ln=0)
pdf.set_text_color(*GRAY)
pdf.set_font("helvetica", "", 11.5)
pdf.set_xy(M + 10, 68)
pdf.multi_cell(W - 2 * M - 10, 6.5,
    "Reads the page the way a human victim sees it - and catches phishing "
    "URL scanners cannot see.")
pdf.set_text_color(*WHITE)
pdf.set_font("helvetica", "B", 12)
pdf.set_xy(M + 10, 96)
pdf.cell(0, 7, "Google Gemini Hackathon  |  RUVERSE TechFest  |  23 Oct 2026", ln=0)
pdf.set_font("helvetica", "", 11)
pdf.set_xy(M + 10, 106)
pdf.cell(0, 7, "Team: Grieving Souls   |   Presenter: Anshika Tiwari   |   Prize Pool: INR 40,000", ln=0)
pdf.set_text_color(*CYAN)
pdf.set_xy(M + 10, 116)
pdf.cell(0, 7, "Repo: github.com/Argyrys/grievingsouls-GGH", ln=0)
footer(1)

# ---------------- Slide 2: The Problem ----------------
new_slide()
title("The Problem", "Phishing still begins with one click")
items([
    "Phishing is the #1 initial access vector for breaches and costs consumers and enterprises billions of dollars every year.",
    "Attackers clone login pages pixel-for-pixel and hide the forgery where URL scanners cannot see: inside <canvas> elements, SVG images, and domains one character off the real brand.",
    "Modern defenses scan URLs. Attackers now hide phishing in the pixels - so URL-only tools miss it entirely.",
    "Who it affects: every browser user, every bank customer, every employee signing into a work portal.",
], y=42)
footer(2)

# ---------------- Slide 3: Our Solution ----------------
new_slide()
title("Our Solution", "Veritas Vision sees phishing like a human does")
items([
    "Three-layer detector: lexical fast-tier -> multimodal vision -> structured verdict.",
    "Layer 1 - Lexical fast-tier: pure-function URL scoring blocks obvious forgeries in milliseconds - zero screenshots, zero Gemini calls.",
    "Layer 2 - Multimodal vision: headless Chromium renders the page exactly as a victim sees it; Gemini reads brand trade dress and text baked into canvas/SVG. The decision is the mismatch between brand UI and host domain.",
    "Layer 3 - Verdict: structured JSON (is_phishing, confidence_score, brand, signals, block/warn/allow) shown on a dashboard and a Chrome extension badge.",
], y=42)
footer(3)

# ---------------- Slide 4: How It Works ----------------
new_slide()
title("How It Works", "Four steps, end to end")
steps = [
    ("1. Target", "A URL is submitted via the dashboard or the Chrome extension popup."),
    ("2. Fast tier", "The lexical engine scores the URL first; conclusive forgeries block instantly without rendering anything."),
    ("3. Vision check", "Playwright captures a 1280x800 screenshot; Gemini analyzes the image + URL and returns a machine-validated JSON verdict."),
    ("4. Surface", "Dashboard shows verdict, confidence gauge, extracted text, and the screenshot. Extension sets toolbar badge PH / ?? / OK."),
]
ypos = 42
for head, txt in steps:
    badge(M, ypos, 30, 12, head, CYAN, BLACK, 10.5)
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_xy(M + 34, ypos + 1)
    pdf.multi_cell(W - 2 * M - 40, 5.6, txt)
    ypos += 15.5
footer(4)

# ---------------- Slide 5: Lexical Fast-Tier ----------------
new_slide()
title("Lexical Fast-Tier (built today)", "Zero network. Zero quota. Runs before rendering.")
items([
    "Signals: leetspeak (paypa1), brand token on an untrusted domain (microsoft-login.com), punycode homoglyphs, raw IP hosts, '@' credential tricks, suspicious TLDs (.xyz, .top, .icu), credential keywords on unrelated hosts.",
    "Threshold: risk >= 0.75 = instant block; registered brand domain = instant allow; anything ambiguous - including localhost - escalates to multimodal vision.",
    "Live result: https://paypa1.com blocks in 23 ms, spending 0 Gemini calls.",
    "Why it matters: survives the free Gemini quota (20 calls/day per model) by spending calls only where vision is actually needed.",
], y=42)
footer(5)

# ---------------- Slide 6: Live Demo ----------------
new_slide()
title("Live Demo", "Three scans, ninety seconds")
demo_rows = [
    ("https://paypa1.com", "BLOCK", "0.92", "lexical", "0 ms, 0 Gemini calls", RED),
    ("canvas-cloaked Microsoft page", "BLOCK", "0.99", "multimodal", "Gemini reads brand text hidden in <canvas>", RED),
    ("legit portal mock", "ALLOW", "0.1", "multimodal", "Judges the mismatch, not the logo", GREEN),
]
ypos = 42
for inp, act, conf, tier, note, col in demo_rows:
    badge(M, ypos, 66, 10, inp, PANEL, WHITE, 9.5)
    badge(M + 70, ypos, 26, 10, act, col, WHITE, 10)
    badge(M + 100, ypos, 22, 10, "conf " + conf, CYAN, BLACK, 9)
    badge(M + 126, ypos, 30, 10, tier, GRAY, WHITE, 9)
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_xy(M + 160, ypos + 1)
    pdf.multi_cell(W - M - 160, 4.6, note)
    ypos += 13.5
pdf.set_text_color(*GRAY)
pdf.set_font("helvetica", "", 9.5)
pdf.set_xy(M, ypos + 4)
pdf.multi_cell(W - 2 * M, 5.5,
    "Chrome extension: on any tab, one click sets the toolbar badge PH (phishing), ?? (suspicious) or OK (safe).")
footer(6)

# ---------------- Slide 7: Tech Stack ----------------
new_slide()
title("Tech Stack", "Picked for speed and free-tier accessibility")
cols = [
    ("Backend", "FastAPI · Python · Pydantic · python-dotenv"),
    ("Browser", "Playwright (headless Chromium, 1280x800 screenshots)"),
    ("AI", "Google Gemini API · gemini-3.5-flash-lite · structured JSON output"),
    ("Frontend", "Vanilla HTML/CSS/JS dashboard - self-contained, no CDN, works on spotty venue Wi-Fi"),
    ("Extension", "Chrome Manifest V3 - toolbar badge PH / ?? / OK"),
    ("Tooling", "fpdf2 handbook generator · unittest suite (offline) · run.bat one-click launcher"),
]
xpos = M
cw = (W - 2 * M - 4 * 6) / 3
for i, (head, txt) in enumerate(cols):
    x = xpos + i * (cw + 6)
    badge(x, 44, cw, 10, head, CYAN, BLACK, 9.5)
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "", 9)
    pdf.set_xy(x, 56)
    pdf.multi_cell(cw, 4.8, txt)
footer(7)

# ---------------- Slide 8: How Gemini Is Used ----------------
new_slide()
title("How Gemini Is Used", "gemini-3.5-flash-lite, multimodal, structured")
items([
    "Native multimodal input: destination URL + PNG screenshot, exactly as a victim sees the page.",
    "Every response is machine-validated: Gemini returns structured JSON via Pydantic response_schema (no fragile text parsing).",
    "Prompt performs a cognitive cross-reference: visual brand dress vs URL context vs the mismatch between them.",
    "Quota-conscious design: multi-key rotation on 429, lexical tier absorbs obvious cases for free, trusted brand domains skip the call entirely.",
], y=42)
footer(8)

# ---------------- Slide 9: Impact ----------------
new_slide()
title("Impact", "Who this helps, and how much")
items([
    "Everyday users: protects anyone who clicks links in email or messages - no security expertise needed.",
    "Banks and brands: catches lookalike domains and pixel-perfect login clones impersonating them.",
    "Enterprises and employees: defends work-portal credentials, a top initial-access vector.",
    "Accessibility: runs on the free Gemini tier - usable by students, small organizations, and individuals without budget for security tools.",
    "Detects what URL scanners miss: canvas-cloaked text, SVG brand art, homoglyph domains.",
], y=42)
footer(9)

# ---------------- Slide 10: Team ----------------
new_slide()
title("Team - Grieving Souls", "4 members · lead presenter · repo pushed before 9:00 AM checkpoint")
hdr = ["Name", "Role", "Contribution"]
rows = [
    ("Rajat Sharma", "Backend & AI Lead", "FastAPI + Gemini pipeline, lexical fast-tier, capture fix"),
    ("Arpita", "Security & Testing", "Threat model, mock victim pages, unit test suite"),
    ("Anshika Tiwari", "Presenter & Pitch", "Pitch deck, 90-second demo narration, judge Q&A prep"),
    ("Ritik Kumar", "Frontend Developer", "Dashboard UI, Chrome extension badge"),
]
ypos = 42
for c, wdt in zip(hdr, [55, 55, W - 2 * M - 110]):
    badge(M + (0 if c == "Name" else 55 + (55 if c == "Role" else 0)), ypos, wdt, 9, c, PANEL, WHITE, 9.5)
ypos += 10.5
for name, role, contrib in rows:
    badge(M, ypos, 55, 8.5, name, BLACK, WHITE, 9.5)
    badge(M + 55, ypos, 55, 8.5, role, PANEL, WHITE, 9)
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "", 9)
    pdf.set_xy(M + 110, ypos + 0.6)
    pdf.multi_cell(W - 2 * M - 110, 4.4, contrib)
    ypos += 9.5
footer(10)

# ---------------- Slide 11: 60% Rule ----------------
new_slide()
title("Honesty under the 60% Rule", "Pre-event core vs. built on the day")
rows = [
    ("Pre-event MVP (<= 60%)", "FastAPI backend + Playwright + Gemini multimodal pipeline, dashboard, Chrome extension, 4 mock victim pages, run.bat launcher.", GREEN),
    ("Built on 23 Oct (>= 40%)", "Lexical fast-tier + auto-fire pre-check, capture hardening, file-backed persistent history, offline unit test suite, 3 new mocks (PayPal, GitHub, Swiggy), presentation materials.", CYAN),
]
ypos = 44
for head, txt, col in rows:
    badge(M, ypos, 72, 11, head, col, BLACK, 9.5)
    pdf.set_text_color(*WHITE)
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_xy(M + 76, ypos + 1)
    pdf.multi_cell(W - 2 * M - 80, 5.2, txt)
    ypos += 15.5
pdf.set_text_color(*GRAY)
pdf.set_font("helvetica", "", 9.5)
pdf.set_xy(M, ypos + 6)
pdf.multi_cell(W - 2 * M, 5.4,
    "Commit history is intact and real: every teammate commits from their own GitHub account, no history rewriting, no .env or secrets committed.")
footer(11)

# ---------------- Slide 12: Credits ----------------
new_slide()
title("Credits", "Everything we reused, and how")
items([
    "Playwright (Apache-2.0) - headless browser capture.",
    "Google Gemini API / Google GenAI SDK - multimodal analysis.",
    "FastAPI (MIT), Pydantic (MIT), python-dotenv (MIT) - backend.",
    "fpdf2 (LGPL-3.0) - presenter handbook generator.",
    "All mock pages hand-written for this project. Brands are referenced nominatively for impersonation research - no logos, fonts, or assets copied.",
    "Presenter handbook (11 pages): Veritas_Vision_Presenter_Handbook.pdf.",
    "No copied or plagiarised project, code, or design.",
], y=42)
footer(12)

# ---------------- Slide 13: Close ----------------
new_slide()
title("Close", "Thank you")
pdf.set_fill_color(*PANEL)
pdf.rect(M, 44, W - 2 * M, 52, "F")
pdf.set_text_color(*WHITE)
pdf.set_font("helvetica", "B", 14)
pdf.set_xy(M + 10, 52)
pdf.multi_cell(W - 2 * M - 20, 7,
    "Problem first -> live demo -> how it works -> close.\n\n"
    '"We stopped looking at URLs and started looking at screens."\n\n'
    "Repo: github.com/Argyrys/grievingsouls-GGH\n"
    "Live demo: run.bat -> http://127.0.0.1:8000/\n\n"
    "Grieving Souls - Google Gemini Hackathon, 23 Oct 2026")
footer(13)

out = r"C:\Users\rs987\Desktop\veritas-vision\Veritas_Vision_Pitch_Deck.pdf"
pdf.output(out)
print("saved", out)
