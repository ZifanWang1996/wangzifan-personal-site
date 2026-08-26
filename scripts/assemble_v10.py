#!/usr/bin/env python3
"""v10: EDITORIAL TIMELINE skin (pure CSS layer + unlocked copy, zero DOM/JS change).

Approved direction C (Editorial / magazine annual review) by ZF Wang, 2026-08-26.
- Replaces the v9 design-token layer + v8 skin remnants (lines 631-866 of index.html,
  the final CSS block before </style>) with scripts/_v10.css. DOM anchors, inline scripts,
  workflow and the 44-test contract are untouched.
- Repaints the site as a magazine annual review: paper-white field, serif display headlines,
  single-column ledger-as-chapters, editorial red accent, zero "board" chrome.
- Unlocked copy refresh: topline -> "WZF PRESS · 一人出版 · ONE-PERSON PRESS".
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
orig_len = len(html)

def rep(old, new, n=1):
    global html
    c = html.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    html = html.replace(old, new)

CSS = (ROOT / "scripts" / "_v10.css").read_text(encoding="utf-8").rstrip("\n") + "\n"

# ---------------- 1. swap the skin block -------------------------------------
START = "/* ---- v8: DEPARTURE BOARD — one-person freight line skin (layered over the v6 console) ----"
i = html.find(START)
assert i >= 0, "v8 skin start marker not found"
j = html.find("</style>", i)
assert j > i, "style close not found after v8 block"
html = html[:i] + CSS + html[j:]
print(f"[1] v8+v9 block ({j - i} chars) replaced with v10 skin ({len(CSS)} chars)")

# ---------------- 2. unlocked copy refresh ------------------------------------
rep(
    '<div class="topline shell" aria-hidden="true"><span>WZF LINES · 一人航运 · ONE-PERSON FREIGHT</span><span>33 SHIPS LIVE · EVERY RELEASE IS A DEPARTURE</span><span>北京 · BEIJING</span></div>',
    '<div class="topline shell" aria-hidden="true"><span>WZF PRESS · 一人出版 · ONE-PERSON PRESS</span><span>33 ISSUES LIVE · EVERY RELEASE IS A CHAPTER</span><span>北京 · BEIJING</span></div>',
)
rep('<meta name="theme-color" content="#f5f1e6">', '<meta name="theme-color" content="#faf9f5">')
print("[2] topline + theme-color refreshed")

# ---------------- self-checks -------------------------------------------------
ok = True
def ck(n, c):
    global ok
    if not c: print("FAIL:", n); ok = False

ck('v8 gone', '--db-or:#ff4d00' not in html)
ck('v10 present', '--ed-red:#c41e3a' in html)
ck('topline new', 'WZF PRESS · 一人出版 · ONE-PERSON PRESS' in html)
ck('theme-color', 'content="#faf9f5"' in html)
ck('33 live', html.count('data-status="live"') == 33)
ck('33 article anchor', html.count('<article class="site" data-status="live">') == 33)
ck('33 visit', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 33)
ck('33 matrix px', html.count('class="px"') == 33)
ck('5 telemetry', html.count('<div class="tele-line">') == 5)
ck('canvas', 'orbit-canvas' in html)
ck('bridge div', '<div class="launch-bridge" aria-hidden="true"></div>' in html)
ck('intro-title', 'id="intro-title"' in html)
ck('5 chips', html.count('data-count="') == 5)
ck('ledger 33', '<span class="ledger-count">33</span>' in html)
ck('timeline title', '45 天，33 次真实上线' in html)
ck('wbr h3', '<h3>HowManySleeps<wbr>Until</h3>' in html)
ck('plausible', 'plausible.shipsolo.io/js/script.js' in html)
ck('no base64', 'data:image/webp;base64' not in html)
ck('single style', html.count('<style>') == 1 and html.count('</style>') == 1)
ck('scripts intact', html.count('<script data-ui="launch">') == 1 and html.count('<script data-ui="motion">') == 1 and html.count('<script data-ui="fx">') == 1)

# v9 contract tokens still present (tests lock these)
for tok in ("--r-0:0", "--r-sm:3px", "--r-md:6px", "--r-lg:12px", "--r-pill:999px",
            "--sec-breath:120px", "--sec-breath-sm:80px",
            "h1{font-weight:900;font-stretch:105%}", "--lime:var(--db-amber)"):
    ck(f'token {tok}', tok in html)

# no stale hues
for stale in ("#c6ff3f", "#6b8f00", "#0e7f9d", "#e8401a", "rgba(92,107,18"):
    ck(f'no stale {stale}', stale not in html)

if not ok:
    sys.exit(1)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[3] written {orig_len} -> {len(html)} ({len(html) - orig_len:+d})")
