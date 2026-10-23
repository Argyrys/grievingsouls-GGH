"""Lexical fast-tier: pure-function URL analysis.

Zero network, zero Gemini quota. Scores lookalike/homoglyph/suspicious-URL
signals and returns a verdict only when the URL alone is conclusive:
high-confidence forgery -> block, registered brand domain -> allow,
anything ambiguous (including localhost / private hosts) -> None (escalate
to the multimodal vision pipeline).
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

from .models import ThreatVerdict

BLOCK_THRESHOLD = 0.75
ALLOW_CONFIDENCE = 0.9

# Registered domains we treat as the real thing (checked with suffix match).
TRUSTED: dict[str, str] = {
    "microsoft.com": "Microsoft",
    "microsoftonline.com": "Microsoft",
    "live.com": "Microsoft",
    "office.com": "Microsoft",
    "msn.com": "Microsoft",
    "google.com": "Google",
    "google.co.in": "Google",
    "gstatic.com": "Google",
    "paypal.com": "PayPal",
    "paypal.me": "PayPal",
    "venmo.com": "PayPal",
    "netflix.com": "Netflix",
    "chase.com": "Chase",
    "jpmorganchase.com": "Chase",
    "github.com": "GitHub",
    "githubusercontent.com": "GitHub",
    "amazon.com": "Amazon",
    "amazon.in": "Amazon",
    "facebook.com": "Facebook",
    "instagram.com": "Facebook",
    "whatsapp.com": "Meta",
    "meta.com": "Meta",
    "apple.com": "Apple",
    "icloud.com": "Apple",
    "linkedin.com": "LinkedIn",
    "x.com": "X (Twitter)",
    "twitter.com": "X (Twitter)",
    "swiggy.in": "Swiggy",
    "zomato.com": "Zomato",
    "stripe.com": "Stripe",
    "dropbox.com": "Dropbox",
}

# Brand tokens looked for in untrusted hosts / paths / usernames.
BRANDS: dict[str, str] = {
    "microsoft": "Microsoft",
    "office": "Microsoft",
    "office365": "Microsoft",
    "outlook": "Microsoft",
    "onedrive": "Microsoft",
    "google": "Google",
    "gmail": "Google",
    "youtube": "Google",
    "paypal": "PayPal",
    "venmo": "PayPal",
    "netflix": "Netflix",
    "chase": "Chase",
    "jpmorgan": "Chase",
    "github": "GitHub",
    "amazon": "Amazon",
    "aws": "Amazon",
    "facebook": "Facebook",
    "instagram": "Facebook",
    "whatsapp": "Meta",
    "apple": "Apple",
    "icloud": "Apple",
    "linkedin": "LinkedIn",
    "twitter": "X (Twitter)",
    "swiggy": "Swiggy",
    "zomato": "Zomato",
    "stripe": "Stripe",
    "dropbox": "Dropbox",
    "coinbase": "Coinbase",
    "binance": "Binance",
}

SUSPICIOUS_TLDS = (
    ".xyz", ".top", ".icu", ".ru", ".tk", ".zip", ".mov", ".click",
    ".loan", ".work", ".gq", ".cf", ".ml", ".rest", ".cfd", ".sbs", ".buzz",
)

SUSPICIOUS_WORDS = {
    "login", "signin", "verify", "verification", "secure", "security",
    "account", "accounts", "confirm", "update", "password", "passwd",
    "otp", "wallet", "billing", "unlock", "suspended", "recover",
}

# Common substitutions attackers use instead of letters.
_LEET_MAP: dict[str, tuple[str, ...]] = {
    "0": ("o",),
    "1": ("i", "l"),
    "3": ("e",),
    "4": ("a",),
    "5": ("s",),
    "7": ("t",),
    "@": ("a",),
    "$": ("s",),
}

_TOKEN_SPLIT = re.compile(r"[^a-z0-9]+")


def _lev_within_1(a: str, b: str) -> bool:
    """True when edit distance(a, b) <= 1 (substitution / one insert / delete)."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        return sum(1 for x, y in zip(a, b) if x != y) == 1
    if la > lb:
        a, b, la, lb = b, a, lb, la
    i = j = 0
    skipped = False
    while i < la and j < lb:
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            if skipped:
                return False
            skipped = True
            j += 1
    return True


def _leet_variants(token: str, cap: int = 32) -> list[str]:
    """Expand digit/symbol substitutions, e.g. paypa1 -> [paypai, paypal]."""
    variants = [token]
    for ch, alts in _LEET_MAP.items():
        if ch not in token:
            continue
        expanded: list[str] = []
        for v in variants:
            for alt in alts:
                expanded.append(v.replace(ch, alt))
        variants = expanded[:cap]
    return variants


def _match_brand(token: str) -> tuple[str, str, str] | None:
    """Return (keyword, brand, mode) if the token looks like a brand token."""
    t = token.lower()
    if len(t) < 4:
        return None
    for kw, brand in BRANDS.items():
        if t == kw or (len(kw) >= 6 and kw in t):
            return kw, brand, "exact"
    variants = _leet_variants(t)
    for kw, brand in BRANDS.items():
        for v in variants:
            if v == kw:
                return kw, brand, "leet"
    for kw, brand in BRANDS.items():
        if len(kw) < 5:
            continue
        for v in variants:
            if _lev_within_1(v, kw):
                return kw, brand, "fuzzy"
    return None


def _tokens(text: str) -> list[str]:
    return [tok for tok in _TOKEN_SPLIT.split(text.lower()) if tok]


def _verdict(
    action: str,
    confidence: float,
    brand: str | None,
    signals: list[str],
    reasoning: str,
) -> ThreatVerdict:
    return ThreatVerdict(
        is_phishing=action == "block",
        confidence_score=confidence,
        brand_impersonated=brand,
        visual_signals=[],
        url_risk_signals=signals,
        extracted_text="",
        reasoning=reasoning,
        tier="lexical",
        recommended_action=action,  # type: ignore[arg-type]
    )


def _is_local(host: str) -> bool:
    if host in ("localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"):
        return True
    try:
        return ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def check_url(url: str) -> ThreatVerdict | None:
    """Return a lexical verdict (block/allow) or None = escalate to vision."""
    try:
        parsed = urlparse(url if "://" in url else "https://" + url)
    except Exception:
        return None
    host = (parsed.hostname or "").lower()
    if not host:
        return None

    # Local / internal hosts are always judged visually, never auto-decided.
    if _is_local(host):
        return None

    # Registered brand domain -> instant allow (no rendering, no Gemini).
    for dom, brand in TRUSTED.items():
        if host == dom or host.endswith("." + dom):
            return _verdict(
                "allow",
                ALLOW_CONFIDENCE,
                brand,
                [f"host '{host}' matches trusted {brand} domain '{dom}'"],
                f"Lexical fast-tier: '{host}' is a registered {brand} domain; "
                "URL alone shows no impersonation risk.",
            )

    signals: list[str] = []
    score = 0.0
    brand: str | None = None
    primary = ""

    # Raw IP host.
    try:
        ipaddress.ip_address(host)
        score += 0.5
        signals.append("host is a raw IP address")
        primary = primary or "the host is a bare IP address"
    except ValueError:
        pass

    # Punycode / IDN homoglyph.
    if "xn--" in host:
        score += 0.4
        signals.append("punycode (IDN) host — possible homoglyph")
        primary = primary or "the host uses punycode homoglyphs"

    # '@' credential trick: everything before @ is a decoy.
    if parsed.username:
        score += 0.5
        signals.append("decoy credentials '@' embedded before the host")
        for tok in _tokens(parsed.username):
            m = _match_brand(tok)
            if m and not brand:
                score += 0.5
                brand = m[1]
                signals.append(f"brand token '{m[0]}' hidden in URL username")
                primary = primary or "the URL hides a real host behind '@'"

    # Brand token inside the host itself.
    for tok in _tokens(host):
        m = _match_brand(tok)
        if m and not brand:
            kw, b, mode = m
            brand = b
            if mode == "exact":
                score += 0.6
                signals.append(f"brand token '{kw}' in untrusted host '{host}'")
                primary = primary or f"host '{host}' contains '{kw}' but is not a registered {b} domain"
            else:
                score += 0.75
                signals.append(f"{mode} lookalike '{tok}' resembles '{kw}' ({b})")
                primary = primary or f"'{tok}' is a {mode} lookalike of {b}"
    if "-" in host and brand:
        score += 0.1
        signals.append("brand token combined with hyphenated host")

    # Brand token only in the path/query (host unrelated).
    if not brand:
        for tok in _tokens(parsed.path + " " + parsed.query):
            m = _match_brand(tok)
            if m:
                brand = m[1]
                score += 0.4
                signals.append(f"brand '{m[1]}' referenced in path on unrelated host")
                primary = primary or f"path references {m[1]} on unrelated host '{host}'"
                break

    # Suspicious TLD.
    if any(host.endswith(t) for t in SUSPICIOUS_TLDS):
        tld = "." + host.rsplit(".", 1)[-1]
        score += 0.3 if brand else 0.15
        signals.append(f"suspicious TLD '{tld}'")

    # login/verify style words anywhere on an untrusted host.
    blob = set(_tokens(host)) | set(_tokens(parsed.path + " " + parsed.query))
    if blob & SUSPICIOUS_WORDS:
        score += 0.2
        hit = sorted(blob & SUSPICIOUS_WORDS)[:3]
        signals.append(f"credential keywords on untrusted host: {', '.join(hit)}")
        primary = primary or "credential-harvesting keywords on an unrelated host"

    # Deep subdomain chains.
    if host.count(".") >= 4:
        score += 0.15
        signals.append("deep subdomain chain (4+ levels)")

    score = min(score, 1.0)

    if score >= BLOCK_THRESHOLD:
        conf = round(min(0.95, 0.7 + score * 0.3), 2)
        return _verdict(
            "block",
            conf,
            brand,
            signals,
            f"Lexical fast-tier: blocked before rendering — {primary}. "
            f"(risk score {score:.2f} >= {BLOCK_THRESHOLD})",
        )
    return None
