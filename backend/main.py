import os
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .analyzer import analyze_image, analyze_url
from .models import AnalyzeImageRequest, AnalyzeRequest, HistoryEntry, ThreatVerdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Veritas Vision", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_history: list[HistoryEntry] = []
MAX_HISTORY = 50


def _record(url: str, verdict: ThreatVerdict, elapsed_ms: int) -> HistoryEntry:
    entry = HistoryEntry(
        id=uuid.uuid4().int >> 64,
        url=url,
        verdict=verdict,
        captured_at=datetime.now(timezone.utc).isoformat(),
        elapsed_ms=elapsed_ms,
    )
    _history.insert(0, entry)
    del _history[MAX_HISTORY:]
    return entry


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "service": "veritas-vision"}


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest) -> dict:
    url = req.url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        verdict, shot_b64, elapsed = await analyze_url(url)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(e)) from e
    entry = _record(url, verdict, elapsed)
    return {
        "success": True,
        "url": url,
        "verdict": verdict.model_dump(),
        "screenshot_b64": shot_b64,
        "elapsed_ms": elapsed,
        "id": entry.id,
    }


@app.post("/api/analyze-url")
async def analyze_url_endpoint(req: AnalyzeImageRequest) -> dict:
    url = req.url.strip()
    try:
        verdict, elapsed = await analyze_image(req.screenshot_b64, url)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(e)) from e
    entry = _record(url, verdict, elapsed)
    return {
        "success": True,
        "url": url,
        "verdict": verdict.model_dump(),
        "elapsed_ms": elapsed,
        "id": entry.id,
    }


@app.get("/api/history")
async def history() -> dict:
    return {"success": True, "history": [h.model_dump() for h in _history]}


@app.api_route("/api/history/clear", methods=["GET", "POST"])
async def history_clear() -> dict:
    _history.clear()
    return {"success": True}


# Serve mock phishing pages and the dashboard from this one server.
app.mount(
    "/mocks",
    StaticFiles(directory=os.path.join(BASE_DIR, "mock-pages"), html=True),
    name="mocks",
)
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True),
    name="frontend",
)
