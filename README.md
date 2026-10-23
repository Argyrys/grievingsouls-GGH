# Veritas Vision — Multimodal Visual Identity Auditor

**One-line pitch:** We stop phishing by reading the page the way a human sees it — Gemini's multimodal vision catches brand impersonation hidden inside pixels, canvas, and SVG text that URL scanners cannot see.

## The problem, and who it affects

Phishing still begins with a click. Modern kits clone a brand's login page pixel-for-pixel and hide the forgery in two places conventional scanners ignore: **the visual layer** (logos, fonts, trade dress rendered in images, `<canvas>`, and SVG graphics) and **lookalike URLs** one character away from the real domain. Every email user, bank customer, and employee who authenticates through a browser is affected — phishing and brand impersonation cost consumers and enterprises billions of dollars each year and remain the #1 initial access vector for breaches.

## Our solution

Veritas Vision is a three-layer phishing detector:

1. **Lexical fast-tier** — a pure-function URL engine scores lookalike patterns (homoglyphs like `paypa1`, brand tokens on untrusted domains, punycode, IP hosts, suspicious TLDs) in milliseconds. High-confidence forgeries are blocked **before a single screenshot or API call is made** — zero quota spent.
2. **Multimodal vision** — for anything ambiguous, a headless Chromium renders the page exactly as a victim would see it (1280×800 screenshot) and Gemini reads it: brand trade dress, text **extracted from canvas/SVG image cloaking**, and the mismatch between brand UI and the actual host domain. The core decision is the *mismatch* — brand UI on a trusted domain is allowed; brand UI on an untrusted host is blocked.
3. **Verdict layer** — structured JSON verdict (Pydantic): `is_phishing`, `confidence_score`, `brand_impersonated`, signals, and `recommended_action` (block/warn/allow), surfaced on a dashboard and a Chrome extension.

## How Gemini is used

- **Model:** `gemini-3.5-flash-lite` via the Google GenAI SDK, called with native multimodal input (prompt + destination URL + PNG screenshot) and **structured output** (`response_schema=ThreatVerdict`) so every response is a machine-valid verdict.
- **Free-tier engineering:** multi-key rotation (`.env` `GEMINI_API_KEYS`, comma-separated) with automatic 429 retirement across keys, exponential backoff, and the lexical pre-check so obvious cases never spend a Gemini call.
- Screenshots are sent exactly as a human would see them; the prompt instructs Gemini to perform a cognitive cross-reference of visual brand cues vs. URL context.

## Tech stack

- **Backend:** Python, FastAPI, Pydantic, python-dotenv
- **Browser engine:** Playwright (headless Chromium)
- **AI:** Google Gemini API (Google GenAI SDK)
- **Frontend:** Vanilla HTML/CSS/JS dashboard (self-contained, no CDN — works on venue Wi-Fi)
- **Extension:** Chrome Manifest V3
- **Tooling:** fpdf2 (presenter handbook generator)

## Setup and run

1. Install: `pip install fastapi uvicorn google-genai playwright pydantic python-dotenv` then `playwright install chromium`
2. Put keys in `.env` (never commit it): `GEMINI_API_KEYS=key1,key2`
3. **Double-click `run.bat`** — server window opens, dashboard loads at `http://127.0.0.1:8000/`
4. Mock victim pages: `http://127.0.0.1:8000/mocks/`
5. Extension: `chrome://extensions` → Load unpacked → select `extension/`

## Team & roles

| Name | Role |
|------|------|
| Rajat Sharma | Backend & AI Lead |
| Arpita | Security & Testing |
| Anshika Tiwari | Presenter & Pitch |
| Ritik Kumar | Frontend Developer |

## What existed before vs. built on the day

**Before the event (pre-event MVP, ≤60%):** FastAPI backend with Playwright screenshot capture and Gemini multimodal verdict pipeline (multi-key quota rotation), dark-cyber dashboard, Chrome MV3 extension, four hand-built mock victim pages (Microsoft canvas-cloaking, Netflix SVG, Chase MFA, legitimate control), `run.bat` launcher.

**Built on the day (23 Oct):**
- Lexical fast-tier URL engine with auto-fire pre-check (two-stage pipeline; Tier field on every verdict)
- Capture hardening (domcontentloaded + paint-wait fallback for real-world sites)
- Persistent history and verdict trend on the dashboard
- Extension auto-scan on page navigation
- PayPal and GitHub mock victim pages
- Unit test suite for the lexical tier
- This README, documentation, and presentation materials

## Credits

- [Playwright](https://playwright.dev) (Apache-2.0) — headless browser capture
- [Google Gemini API](https://ai.google.dev) / Google GenAI SDK (MIT) — multimodal analysis
- [FastAPI](https://fastapi.tiangolo.com) (MIT), [Pydantic](https://docs.pydantic.dev) (MIT), [python-dotenv](https://github.com/theskumar/python-dotenv) (MIT)
- [fpdf2](https://pypdf2.readthedocs.io) (LGPL-3.0) — handbook generator
- All mock pages are original hand-built HTML/CSS written for this project. No brand logos, fonts, or proprietary assets were copied; brands are referenced nominatively for impersonation research.
- No code, design, or project was copied or plagiarised.
