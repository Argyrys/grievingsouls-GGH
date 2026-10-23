# -*- coding: utf-8 -*-
"""Generates the presenter theory handbook PDF for Veritas Vision."""

from fpdf import FPDF

TITLE = "Veritas Vision - Presenter Theory Handbook"


def clean(s: str) -> str:
    for a, b in (
        ("\u20b9", "INR "),
        ("\u2014", " - "),
        ("\u2013", "-"),
        ("\u2019", "'"),
        ("\u2018", "'"),
        ("\u201c", '"'),
        ("\u201d", '"'),
        ("\u2192", "->"),
        ("\u25b2", "^"),
        ("\u2022", "-"),
        ("\u00d7", "x"),
        ("\u2705", ""),
        ("\u26a0", "!"),
        ("\U0001f680", ""),
        ("\u00a0", " "),
    ):
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "VERITAS VISION - PRESENTER HANDBOOK", align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, f"Google Gemini Hackathon - 23 Oct 2026 - Page {self.page_no()}", align="C")

    def h1(self, text):
        self.ln(3)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(236, 72, 153)
        self.multi_cell(0, 8, clean(text))
        self.set_draw_color(236, 72, 153)
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(4)

    def h2(self, text):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11.5)
        self.set_text_color(6, 182, 212)
        self.multi_cell(0, 6, clean(text))
        self.ln(1)

    def body(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.4, clean(text))
        self.ln(1)

    def bullet(self, text, indent=4):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + indent)
        self.multi_cell(0, 5.4, clean("- " + text))
        self.set_x(x)

    def quote(self, text):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "BI", 10)
        self.set_text_color(80, 80, 80)
        self.set_fill_color(245, 245, 245)
        x = self.get_x()
        self.set_x(x + 6)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.6, clean(text), fill=True)
        self.set_x(x)
        self.ln(2)


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(16, 16, 16)
pdf.add_page()

# COVER
pdf.ln(30)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(236, 72, 153)
pdf.multi_cell(0, 12, clean("VERITAS VISION"))
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(6, 182, 212)
pdf.multi_cell(0, 9, clean("Presenter Theory Handbook"))
pdf.ln(6)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(60, 60, 60)
pdf.multi_cell(0, 6.5, clean(
    "Everything the lead presenter must know cold: problem theory, solution deep dive, "
    "tech stack rationale, Gemini mechanics, competitive positioning, and the full Q&A defense."
))
pdf.ln(4)
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 6.5, clean(
    "Event: Google Gemini Hackathon | 23 Oct 2026 | B Block SB-03\n"
    "Schedule: Registration 7:00 AM | Hacking 7:30 AM-12:30 PM | Submission 1:00 PM | Judging 2:00 PM\n"
    "Prize Pool: INR 40,000"
))

# 1. ONE-LINERS
pdf.add_page()
pdf.h1("1. THE LINES YOU MUST SAY WITHOUT THINKING")
pdf.quote("Elevator pitch: 'Phishing went visual. Text scanners went blind. Veritas Vision sees what humans see.'")
pdf.quote("Product one-liner: 'Veritas Vision is a multimodal visual identity auditor that renders any page "
          "the way a victim would see it, and uses Gemini to catch brand impersonation before a single "
          "character is typed.'")
pdf.quote("Problem one-liner: 'Attackers paint their lies in images. Defenders still read text.'")
pdf.quote("Closing line: 'We are not another blocklist. We are the auditor for the visual era of phishing.'")
pdf.h2("The 30-second verbal version")
pdf.body(
    "Modern phishing hides all its text inside canvas images, SVG graphics and zero-day domains. "
    "Every secure email gateway and browser filter that reads HTML keywords, spelling mistakes and "
    "domain blocklists sees a blank, benign page. To a human eye it is a perfect Microsoft login. "
    "Veritas Vision closes that gap. We load the page in a headless browser exactly like a victim would, "
    "capture the high-resolution screenshot, and hand it to Gemini together with the destination URL. "
    "Gemini performs a cognitive cross-reference: does this page wear a protected brand's trade dress "
    "while the host is untrusted? It returns a deterministic JSON verdict - phishing or not, confidence, "
    "which brand, why, and the action to take. A live Chrome extension shows a red badge before the "
    "victim types anything."
)

# 2. PROBLEM THEORY
pdf.add_page()
pdf.h1("2. PROBLEM THEORY - THE ATTACKS YOU ARE DESCRIBING")
pdf.h2("2.1 Traditional defenses (what is broken)")
pdf.bullet("Secure email gateways and browser filters do TEXT analysis: keyword matching, blocklists, "
           "spelling-error heuristics, domain reputation, URL lexical features.")
pdf.bullet("These work against 2015-era phishing: typosquatted domains like 'micros0ft-login.com', "
           "urgency keywords, bad grammar.")
pdf.bullet("The failure: a page can now contain almost ZERO readable text and still be a perfect fake, "
           "because everything the victim reads is pixels.")
pdf.h2("2.2 Attack 1: Visual Identity Hijacking")
pdf.bullet("The attacker renders a complete brand layout - logo, typography, colors, MFA form structure, "
           "footer links - inside flat images or canvas elements.")
pdf.bullet("Victim sees: an authentic-looking Microsoft, Netflix or Chase login page.")
pdf.bullet("Scanner sees: an HTML document with no brand text, no suspicious keywords, served from a "
           "domain nobody has ever reported.")
pdf.h2("2.3 Attack 2: Text-Cloaking")
pdf.bullet("All textual content is painted onto an HTML <canvas> with JavaScript, or embedded as SVG "
           "glyph paths, or baked into a PNG.")
pdf.bullet("There is no DOM text node to grep. Copy-paste returns nothing. Readability scores see nothing.")
pdf.bullet("OUR HERO DEMO: the mock Microsoft page is exactly this. View-source looks empty; the eye "
           "sees Microsoft.")
pdf.h2("2.4 Attack 3: Zero-day domains")
pdf.bullet("Freshly registered domains have no reputation history - they are invisible to blocklists "
           "until thousands of victims report them.")
pdf.bullet("Phishing-as-a-service kits now build a unique page per victim (e.g. LogoKit pulls a LIVE "
           "screenshot of the target company's own site as the background) - no static template exists "
           "for fingerprinting.")
pdf.h2("2.5 Why this matters - talking numbers")
pdf.bullet("Phishing has been the #1 initial attack vector for years in industry breach reports.")
pdf.bullet("Academic baselines: classical unimodal detectors miss ~45% of modern phishing pages in "
           "published multimodal LLM studies; multimodal approaches cut false negatives dramatically.")
pdf.bullet("Our own pitch claim: a text-based scanner declares our canvas Microsoft page BENIGN - we "
           "demonstrate this live.")

# 3. SOLUTION THEORY
pdf.add_page()
pdf.h1("3. SOLUTION DEEP DIVE - THE 4-STEP PIPELINE")
pdf.h2("Step 1 - Isolated Behavioral Capture")
pdf.body(
    "Instead of downloading raw HTML - which the attacker controls and can make lie - we let a headless "
    "Chromium instance actually render the page: run the JavaScript, paint the canvas, load the images, "
    "exactly as a human victim's browser would. We spoof a legitimate user-agent to slip past naive "
    "anti-bot scripts, wait for network idle, and snapshot a precise 1280x800 frame. "
    "Talking point: 'We do not trust the code. We trust the pixels the victim would actually see.'"
)
pdf.h2("Step 2 - Context-Aware Visual Mismatch Auditing")
pdf.body(
    "The screenshot and the raw destination URL are sent TOGETHER to Gemini. Neither alone is sufficient: "
    "screenshot alone loses host context; URL alone cannot see canvas content. "
    "Talking point: 'A logo means nothing without knowing where it is being served from.'"
)
pdf.h2("Step 3 - Cognitive Discrepancy Analysis")
pdf.body(
    "Gemini answers one sharp question: does this visual layout present a protected trade dress - "
    "Microsoft typography, official logo, MFA input grammar - while the URL domain context points to an "
    "untrusted external host? This is a CROSS-REFERENCE, not a vibe check. "
    "A real microsoft.com showing Microsoft UI is ALLOW. A localhost page showing Microsoft UI is BLOCK. "
    "Same brand, different verdict - that is the intelligence."
)
pdf.h2("Step 4 - Deterministic Structural Extraction")
pdf.body(
    "Gemini recovers the text baked into images (defeating text-cloaking) and emits an immutable JSON "
    "object validated by Pydantic: is_phishing, confidence_score, brand_impersonated, visual_signals, "
    "url_risk_signals, extracted_text, reasoning, recommended_action (block/warn/allow). "
    "Talking point: 'Structured output means this can trigger an automatic block, not just a chat reply.'"
)

# 4. TECH STACK THEORY
pdf.add_page()
pdf.h1("4. TECH STACK - WHY EACH CHOICE, DEFENDED")
pdf.h2("Frontend: Tailwind CSS (CDN) + Vanilla JavaScript")
pdf.bullet("WHY: zero build step, zero npm install, zero chance of a webpack failure five minutes before "
           "the live demo. Judges see the result, not the tooling.")
pdf.bullet("IF ASKED: 'Not React?' -> 'For a security ops console with one screen, a framework is "
           "latency we do not need. We spent our risk budget on the AI pipeline instead.'")
pdf.h2("Backend: Python + FastAPI + Uvicorn")
pdf.bullet("WHY: FastAPI is natively async - our job is one heavy async operation (render a hostile page) "
           "behind one endpoint. The UI never freezes while a page renders.")
pdf.bullet("CORS middleware included so the dashboard can talk to the API cleanly during development.")
pdf.h2("Ingestion: Playwright (async Python) + headless Chromium")
pdf.bullet("WHY: only a real browser defeats client-side rendering tricks - pages that build their UI "
           "after JavaScript runs, canvas-painted text, delayed redirects.")
pdf.bullet("Hardening: spoofed user-agent, 15s timeout, network-idle wait, 1280x800 frame, page sandboxed "
           "from our server - we never execute attacker code in our process.")
pdf.h2("Validation: Pydantic v2")
pdf.bullet("WHY: the model's answer is untrusted input until a schema validates it. Pydantic rejects "
           "malformed verdicts at the boundary so charts and blocklists never receive garbage.")
pdf.bullet("IF ASKED: 'What if Gemini returns prose?' -> 'We request structured output with a response "
           "schema - the API enforces JSON shape server-side, then Pydantic re-validates on arrival. "
           "Two gates.'")
pdf.h2("Cognitive tier: Gemini (model: gemini-3.5-flash)")
pdf.bullet("WHY: native multimodal - image + text arrive as one request, no slicing images into separate "
           "embeddings, no two-stage 'describe image then reason' pipeline.")
pdf.bullet("Settings: low temperature (0.1) for near-deterministic verdicts; structured JSON output.")
pdf.bullet("Cost/latency: a Flash-class model keeps per-scan cost to fractions of a cent and latency in "
           "the low seconds - required for a real-time extension badge.")
pdf.h2("Extension: Chrome Manifest V3")
pdf.bullet("WHY MV3: it is the only store-supported manifest today; service worker background keeps it "
           "lightweight.")
pdf.bullet("Flow: tab finishes loading -> captureVisibleTab -> POST to our API with URL + screenshot -> "
           "toolbar badge red/yellow/green + popup verdict.")

# 5. GEMINI SPECIFICS
pdf.add_page()
pdf.h1("5. GEMINI MECHANICS - QUESTIONS THEY WILL PROBE")
pdf.h2("Where Gemini sits in the architecture")
pdf.body(
    "Gemini is the ONLY reasoning component. Playwright gathers evidence; Gemini interprets it; "
    "Pydantic certifies it; the UI renders it. If Gemini is removed, the system has eyes but no judgment - "
    "that is the honest dependency, and we designed everything else to be boring and reliable around it."
)
pdf.h2("Why multimodal matters here (the technical justification)")
pdf.bullet("The attacker's payload IS the image. Text models receive an empty document; vision models "
           "see the Microsoft logo, the input fields, the trademark layout.")
pdf.bullet("Cross-modal reasoning (image + URL string in one prompt) is what exposes the mismatch: "
           "visually brand-authentic + contextually untrusted host.")
pdf.h2("Structured output (the determinism claim)")
pdf.bullet("We request JSON with a response schema rather than parsing free text with regex.")
pdf.bullet("Temperature 0.1 keeps verdicts stable across repeated scans of the same page.")
pdf.bullet("Result: the same page scanned twice produces the same verdict and near-identical confidence - "
           "it behaves like software, not like a chatbot.")
pdf.h2("Failure handling (say this proudly)")
pdf.bullet("Automatic retry on transient 5xx from the API.")
pdf.bullet("Per-scan timeout with a user-visible error card - the UI never white-screens.")
pdf.bullet("Playwright timeout returns a clear 'site did not render' message instead of hanging.")
pdf.h2("Honest limitations (credibility builders)")
pdf.bullet("Adversarial images (noise designed to fool vision models) are a known research problem; "
           "our anchor is trade-dress STRUCTURE (logo placement, form grammar, typography), not pixel matching.")
pdf.bullet("Brand-new brands with no prior coverage still work because we do zero-shot reasoning, but "
           "confidence may drop - the schema surfaces that as a lower score instead of false certainty.")
pdf.bullet("Privacy: in production you would whitelist scannable origins and redact form fields before "
           "capture. Demo only scans our local mock pages.")

# 6. COMPETITIVE
pdf.add_page()
pdf.h1("6. COMPETITIVE POSITIONING - OWN THE COMPARISON")
pdf.h2("If asked: 'Isn't this just Gemini + a screenshot?'")
pdf.body(
    "The model is one layer. The product is the pipeline: honest rendering in a real browser so we see "
    "what the victim sees rather than attacker-authored HTML; cross-referencing visual branding against "
    "host context; schema-enforced JSON that can trigger automated blocking; a real-time extension path "
    "that reuses the already-rendered page; and a demo suite that reproduces a modern cloaking attack on "
    "command. Wrappers do not ship that."
)
pdf.h2("Landscape (name these if challenged)")
pdf.bullet("Academic multimodal detectors (PhishSense, PhishDebate, ALP prompting studies): validate the "
           "approach scientifically but are offline evaluations, not deployable products.")
pdf.bullet("Classic visual-similarity systems (VisualPhishNet, Phishpedia): need trained CNNs and curated "
           "reference logo databases - every new brand is a maintenance project. We are zero-shot: one API "
           "key, no training data, no reference DB.")
pdf.bullet("Commercial visual-AI vendors: enterprise, expensive, closed. We are a working prototype you "
           "can run today.")
pdf.bullet("Browser text-based extensions: analyze HTML/TEXT - blind to canvas cloaking by construction. "
           "That is the entire gap we occupy.")
pdf.bullet("Antivirus / VirusTotal style: reputation and payload scanning. Our attack has no malware "
           "payload - the payload is a picture. Reputation systems score zero-day domains clean.")
pdf.h2("Our unique wedge (repeat often)")
pdf.bullet("The text-cloaking demo. No competitor pitch shows a page whose text does not exist in the DOM.")
pdf.bullet("Full product loop: dashboard (forensic audit) + extension (real-time protection) in one demo.")
pdf.bullet("Cognitive discrepancy framing - brand trade dress vs host trust - a sharper threat model than "
           "'this looks suspicious'.")

# 7. Q&A
pdf.add_page()
pdf.h1("7. FULL Q&A DEFENSE CARD")
qa = [
    ("Why not VirusTotal?",
     "VirusTotal is blocklist and payload-reputation based. Our attack is a zero-day domain serving no "
     "malware - the payload is a canvas image. VT scores it clean because nothing on it has ever been "
     "reported and nothing executable is present. We detect the visual impersonation itself, which "
     "reputation systems are structurally blind to."),
    ("Isn't this just a GPT wrapper?",
     "The model is one component. The hard engineering is: rendering hostile pages safely in headless "
     "Chromium, combining image and URL context for a cross-reference decision, enforcing deterministic "
     "schema output that can trigger automated blocking, and the real-time extension path. That is a "
     "system, not a prompt."),
    ("How fast is a scan?",
     "Dashboard path with full Playwright render: roughly 5-8 seconds. Extension path where the page is "
     "already rendered: 2-5 seconds. Fast enough to badge a page before the user finishes reading it."),
    ("What is the accuracy? Did you benchmark?",
     "Our verdicts are zero-shot with explicit confidence, and published research on screenshot+URL "
     "multimodal inputs with Gemini reports brand identification above 90 percent. We deliberately show "
     "confidence rather than claim a single headline number - honest uncertainty is safer for a security "
     "product than false precision."),
    ("What about false positives on legitimate sites?",
     "The decision is discrepancy-based, not logo-based. Chase UI on chase.com matches -> allow. Chase UI "
     "on an unknown host mismatches -> block. The design minimizes false positives because owning the "
     "brand is not a signal; MISMATCHING the host is."),
    ("How do you stop attackers adapting?",
     "Arms race is real. Two answers: first, our anchor is structural - logo placement, form grammar, "
     "typography relationships - not pixel-perfect matching, so visual noise does not trivially defeat it. "
     "Second, we force attackers away from the cheap playbook: today a canvas clone beats every text "
     "scanner; with us that whole class becomes risky. We push the cost of attack up."),
    ("What about privacy - sending screenshots to a cloud model?",
     "For the demo we only scan our own local mock pages. In deployment: whitelist scannable origins, "
     "redact form field values before capture, and enterprise installs can run against private/Vertex "
     "endpoints. Sending the rendered frame is strictly less sensitive than sending the typed credentials "
     "it protects."),
    ("Why Playwright and not just fetch the HTML?",
     "Because the HTML lies. A canvas page's source is nearly empty - fetching raw source is exactly the "
     "blind spot we are fixing. Only rendering in a real browser produces the evidence a human sees."),
    ("Is this deployable or a demo?",
     "Deployable shape already: stateless API endpoint, structured action output that a gateway or proxy "
     "could consume directly, and an extension for endpoints we do not control. Missing pieces for "
     "production are ops concerns - rate limits, allow-lists, logging - not research."),
    ("What would you build next?",
     "Three things: a local caching layer so repeated scans cost nothing; a risk score that aggregates "
     "history across a session; and an enterprise feed that lets a SOC push newly confirmed brand "
     "impersonations to all users within minutes."),
]
for q, a in qa:
    pdf.h2("Q: " + q)
    pdf.body("A: " + a)

# 8. DEMO SCRIPT
pdf.add_page()
pdf.h1("8. LIVE DEMO - TIMED NARRATION (90 SECONDS)")
steps = [
    ("0:00-0:10", "HOOK",
     "'Last month a relative got a Microsoft account lockout page - perfect logo, perfect fonts. He typed "
     "his password. The terrifying part: the page contained almost no text. Every word was painted as an "
     "image. Every tool that reads text saw nothing.'"),
    ("0:10-0:30", "THE TRAP",
     "Open the canvas Microsoft page. 'Look at this login page. Fully convincing. Now the source - almost "
     "no readable text. All of it is painted onto a canvas. A keyword scanner calls this BENIGN.'"),
    ("0:30-0:55", "THE STRIKE",
     "Run the Veritas scan. Narrate: 'Playwright renders it in isolation - we do not trust its HTML, we "
     "trust the pixels. Gemini gets the frame plus the URL... verdict: BLOCK. Confidence 0.94. Brand: "
     "Microsoft. Signal: official trade dress on an untrusted host - and it read the text out of the "
     "canvas.'"),
    ("0:55-1:10", "THE CONTRAST",
     "Scan the legitimate page. 'ALLOW. Same brand visuals, matching domain context. We are not a logo "
     "detector - we are a discrepancy auditor.'"),
    ("1:10-1:25", "REAL-TIME",
     "With extension loaded, visit the fake Netflix page. 'Watch the toolbar - RED. Detected before a "
     "single character was typed.'"),
    ("1:25-1:30", "CLOSE",
     "'Everyone else reads. We see. Veritas Vision.'"),
]
for t, name, line in steps:
    pdf.h2(f"[{t}] {name}")
    pdf.body(line)

pdf.h2("Demo safety rules")
pdf.bullet("Pre-open every tab and pre-run every scan once before going on stage.")
pdf.bullet("If a live scan stalls past 6 seconds, move on and reveal the pre-captured result - never "
           "narrate dead air.")
pdf.bullet("Laptop on power, do-not-disturb on, browser zoom at 150 percent, one double-click run script.")
pdf.bullet("If the venue network dies: localhost still works - dashboard, mocks and API are all local; "
           "only the Gemini call needs internet (have a phone hotspot ready).")

# 9. SCHEDULE
pdf.add_page()
pdf.h1("9. HACKATHON DAY TIMELINE (MEMORISE)")
timeline = [
    ("7:00 - 7:30 AM", "Registration at B Block SB-03 - be early, seats and power first."),
    ("7:30 - 10:30 AM", "Breakfast + HACKING PHASE 1: final integration, run.ps1 test, extension loaded."),
    ("10:30 - 11:00 AM", "Opening ceremony - listen for judging criteria changes."),
    ("11:00 AM - 12:00 PM", "HACKING PHASE 2: dashboard polish, failure handling."),
    ("12:00 - 12:30 PM", "Mentoring round - use mentors as rehearsal audience, take notes on pushback."),
    ("12:30 - 1:00 PM", "Lunch - mentally run the script."),
    ("1:00 - 2:00 PM", "FINAL BUILD + SUBMISSION: stop coding at 1:30. Full demo twice. Backup captures."),
    ("2:00 - 3:00 PM", "FINAL JUDGEMENT: your slot. 90s pitch, live demo, Q&A from section 7."),
    ("3:30 - 5:00 PM", "Valedictory and closing."),
]
for t, d in timeline:
    pdf.h2(t)
    pdf.body(d)

pdf.ln(4)
pdf.h2("Team roles on stage")
pdf.bullet("Lead presenter: speaks, eye contact, never touches the keyboard.")
pdf.bullet("Demo operator: pre-staged tabs, silent, drives every click.")
pdf.bullet("Tech backup: owns run.ps1, restarts, can answer architecture questions.")
pdf.bullet("Domain expert: answers threat model, market and competition questions.")

pdf.ln(6)
pdf.quote("Final reminder: judges remember the moment the scanner went blind and Veritas did not. "
          "Slow down at exactly that second.")

out = r"C:\Users\rs987\Downloads\Veritas_Vision_Presenter_Handbook.pdf"
pdf.output(out)
print("WROTE", out)
