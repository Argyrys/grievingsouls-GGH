import asyncio
import base64
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types
from playwright.async_api import async_playwright

from .models import ThreatVerdict

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

MODEL = "gemini-3.5-flash-lite"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

PROMPT = """You are Veritas Vision, a multimodal visual identity auditor.
You receive a high-resolution screenshot of a web page exactly as a human victim would see it,
plus the destination URL the browser actually navigated to.

Perform a cognitive cross-reference:
1. VISUAL: Identify any protected brand trade dress present (logos, typography, color systems,
   MFA/login form structure, footer patterns). Extract any text that appears baked into images,
   canvas elements, or SVG graphics (text-cloaking).
2. URL CONTEXT: Judge whether the host domain plausibly belongs to that brand. Consider lookalike
   domains, unrelated hosts, localhost/internal hosts, IP addresses, and unusual TLDs.
3. DISCREPANCY: The core decision is the MISMATCH. Brand UI on the brand's real domain = allow.
   Brand UI on an untrusted/external host = phishing. Do not flag solely because a logo exists.
   Do not allow solely because a page looks polished.

Return only the structured verdict. recommended_action must be block for high-confidence phishing,
warn for suspicious mid-confidence cases, allow otherwise."""


def _load_keys() -> list[str]:
    raw = os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY") or ""
    return [k.strip() for k in raw.replace("\n", ",").split(",") if k.strip()]


# Keys that returned 429 this session — skipped until server restart.
_dead_keys: set[str] = set()
_key_cursor = 0


def _is_quota_error(e: Exception) -> bool:
    msg = str(e)
    return "429" in msg or "RESOURCE_EXHAUSTED" in msg


async def capture_screenshot(url: str) -> bytes:
    """Render the page in headless Chromium and return PNG bytes."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1280, "height": 800},
                ignore_https_errors=True,
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=20000)
            await page.wait_for_timeout(1200)
            return await page.screenshot(type="png", full_page=False)
        finally:
            await browser.close()


async def analyze_screenshot(screenshot: bytes, url: str) -> ThreatVerdict:
    """Send screenshot + URL to Gemini with multi-key rotation on quota errors."""
    global _key_cursor
    last_err: Exception | None = None

    for attempt in range(12):
        keys = _load_keys()
        if not keys:
            raise RuntimeError("No Gemini API keys in .env (GEMINI_API_KEYS)")
        live = [k for k in keys if k not in _dead_keys]
        if not live:
            raise RuntimeError(
                f"All {len(keys)} Gemini API keys are out of quota today. "
                "Add a fresh key (new project at aistudio.google.com/apikey) "
                "to GEMINI_API_KEYS, or wait for the reset."
            )
        key = live[_key_cursor % len(live)]
        try:
            client = genai.Client(api_key=key)
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model=MODEL,
                    contents=[
                        PROMPT,
                        f"Destination URL: {url}",
                        genai_types.Part.from_bytes(
                            data=screenshot, mime_type="image/png"
                        ),
                    ],
                    config=genai_types.GenerateContentConfig(
                        temperature=0.1,
                        response_mime_type="application/json",
                        response_schema=ThreatVerdict,
                        **(
                            {"thinking_config": genai_types.ThinkingConfig(thinking_budget=0)}
                            if "lite" not in MODEL
                            else {}
                        ),
                    ),
                ),
            )
            if response.parsed is not None:
                return response.parsed
            if response.text:
                return ThreatVerdict.model_validate_json(response.text)
            raise RuntimeError("Gemini returned empty response")
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            last_err = e
            if _is_quota_error(e):
                # Quota is per project per model: retire this key, try the next
                # one immediately — no sleep, this isn't transient.
                _dead_keys.add(key)
                _key_cursor += 1
                continue
            if attempt < 11:
                await asyncio.sleep(min(2 ** (attempt * 0.7), 12))

    raise RuntimeError(f"Gemini analysis failed after retries: {last_err}")


async def analyze_url(url: str) -> tuple[ThreatVerdict, str, int]:
    """Full pipeline: capture -> analyze. Returns (verdict, screenshot_b64, elapsed_ms)."""
    start = time.perf_counter()
    png = await capture_screenshot(url)
    verdict = await analyze_screenshot(png, url)
    elapsed = int((time.perf_counter() - start) * 1000)
    return verdict, base64.b64encode(png).decode("ascii"), elapsed


async def analyze_image(screenshot_b64: str, url: str) -> tuple[ThreatVerdict, int]:
    """Extension path: analyze an already-captured screenshot."""
    start = time.perf_counter()
    png = base64.b64decode(screenshot_b64)
    verdict = await analyze_screenshot(png, url)
    elapsed = int((time.perf_counter() - start) * 1000)
    return verdict, elapsed
