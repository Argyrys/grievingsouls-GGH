# Veritas Vision — 90-Second Pitch Script (Anshika)

## Hook (15s)
Imagine you get a "Microsoft 365 session expired" email. You click — the logo,
fonts, footer all look identical. The URL is one character off. Modern tools
scan URLs. Attackers hide the forgery in the pixels.

## Problem (20s)
Phishing is the #1 entry point for breaches and costs billions every year.
New kits clone brand logins pixel-for-pixel and hide text inside canvas and
SVG images — completely invisible to URL scanners. Every browser user is affected.

## Solution + Demo (40s)
Veritas Vision reads the page the way a human sees it — with Gemini's multimodal vision.
- Demo 1: paypa1.com → lexical fast-tier blocks in milliseconds, 0 Gemini calls
- Demo 2: localhost Microsoft canvas mock → Gemini extracts text hidden in <canvas>
- Demo 3: legit portal → ALLOW 0.1 — it judges the MISMATCH, not the logo

## Close (15s)
Three layers: fast lexical check, multimodal vision, structured verdict —
dashboard + Chrome extension. Before the event we built the MVP core; today
we built the two-stage engine, tests, and new simulations.
We stopped looking at URLs and started looking at screens. Veritas Vision.
