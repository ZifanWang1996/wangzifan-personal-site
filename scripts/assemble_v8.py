#!/usr/bin/env python3
"""v8: DEPARTURE BOARD skin (pure CSS layer, zero DOM/JS change).

Approved direction D (Departure Board / one-person freight line) by ZF Wang, 2026-08-24.
- Replaces the v7 GAZETTE skin block (lines 628-762 of index.html, the final CSS layer
  before </style>) with scripts/_v8.css. DOM anchors, inline scripts, workflow and the
  42-test contract are untouched.
- Repaints the site as a departure board: cream field + black board strips, square
  ink-framed tickets, amber/orange signals, mono-forward, zero serif.
- Unlocked copy refresh: topline -> "WZF LINES · ONE-PERSON FREIGHT", theme-color #f5f1e6.
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

CSS = (ROOT / "scripts" / "_v8.css").read_text(encoding="utf-8").rstrip("\n") + "\n"

# ---------------- 1. swap the skin block -------------------------------------
START = "/* ---- v7: GAZETTE — one-person press editorial skin (layered over the v6 console) ---- */"
i = html.find(START)
assert i >= 0, "v7 skin start marker not found"
j = html.find("</style>", i)
assert j > i, "style close not found after v7 block"
html = html[:i] + CSS + html[j:]
print(f"[1] v7 block ({j - i} chars) replaced with v8 skin ({len(CSS)} chars)")

# ---------------- 2. unlocked copy refresh ------------------------------------
rep(
    '<div class="topline shell" aria-hidden="true"><span>WANG ZIFAN · ONE PERSON PRESS</span><span>把想法做出来 · 再让世界给答案</span><span>北京 · BEIJING</span></div>',
    '<div class="topline shell" aria-hidden="true"><span>WZF LINES · 一人航运 · ONE-PERSON FREIGHT</span><span>32 SHIPS LIVE · EVERY RELEASE IS A DEPARTURE</span><span>北京 · BEIJING</span></div>',
)
rep('<meta name="theme-color" content="#f5f0e4">', '<meta name="theme-color" content="#f5f1e6">')
print("[2] topline + theme-color refreshed")

# ---------------- self-checks -------------------------------------------------
ok = True
def ck(n, c):
    global ok
    if not c: print("FAIL:", n); ok = False

ck('v7 gone', 'gz-' not in html)
ck('v8 present', '--db-or:#ff4d00' in html)
ck('topline new', 'WZF LINES · 一人航运 · ONE-PERSON FREIGHT' in html)
ck('theme-color', 'content="#f5f1e6"' in html)
ck('32 live', html.count('data-status="live"') == 32)
ck('32 article anchor', html.count('<article class="site" data-status="live">') == 32)
ck('32 visit', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 32)
ck('32 matrix px', html.count('class="px"') == 32)
ck('5 telemetry', html.count('<div class="tele-line">') == 5)
ck('canvas', 'orbit-canvas' in html)
ck('bridge div', '<div class="launch-bridge" aria-hidden="true"></div>' in html)
ck('intro-title', 'id="intro-title"' in html)
ck('5 chips', html.count('data-count="') == 5)
ck('ledger 32', '<span class="ledger-count">32</span>' in html)
ck('timeline title', '42 天，32 次真实上线' in html)
ck('wbr h3', '<h3>HowManySleeps<wbr>Until</h3>' in html)
ck('plausible', 'plausible.shipsolo.io/js/script.js' in html)
ck('no base64', 'data:image/webp;base64' not in html)
ck('single style', html.count('<style>') == 1 and html.count('</style>') == 1)
ck('scripts intact', html.count('<script data-ui="launch">') == 1 and html.count('<script data-ui="motion">') == 1 and html.count('<script data-ui="fx">') == 1)

if not ok:
    sys.exit(1)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[3] written {orig_len} -> {len(html)} ({len(html) - orig_len:+d})")
