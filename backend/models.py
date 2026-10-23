from typing import Literal, Optional

from pydantic import BaseModel, Field


class ThreatVerdict(BaseModel):
    is_phishing: bool = Field(description="Whether the page is a phishing attempt")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence 0-1")
    brand_impersonated: Optional[str] = Field(
        default=None, description="Brand being impersonated, null if none"
    )
    visual_signals: list[str] = Field(
        default_factory=list, description="Visual evidence found on the rendered page"
    )
    url_risk_signals: list[str] = Field(
        default_factory=list, description="Suspicious signals from the destination URL"
    )
    extracted_text: str = Field(
        default="", description="Text recovered from images/canvas/SVG on the page"
    )
    reasoning: str = Field(
        description="1-2 sentence cognitive cross-reference explanation"
    )
    tier: Literal["lexical", "multimodal"] = Field(
        default="multimodal",
        description="Engine that produced the verdict: lexical fast-tier or Gemini multimodal",
    )
    recommended_action: Literal["block", "warn", "allow"] = Field(
        description="Deterministic action to take"
    )


class AnalyzeRequest(BaseModel):
    url: str = Field(min_length=4, max_length=2048)


class AnalyzeImageRequest(BaseModel):
    url: str = Field(min_length=4, max_length=2048)
    screenshot_b64: str = Field(min_length=16)


class HistoryEntry(BaseModel):
    id: int
    url: str
    verdict: ThreatVerdict
    captured_at: str
    elapsed_ms: int
