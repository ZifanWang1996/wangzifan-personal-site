#!/usr/bin/env python3
"""v3 recolor: cream editorial light theme with dark terminal anchors.

Pure color-layer transformation of the v2 page:
- :root palette flipped to warm cream paper + ink text (variable-driven rules auto-follow)
- one override CSS block appended at the end of the stylesheet for hardcoded colors
- dark "terminal anchors" kept: shipping-engine, system-log, changelog, command palette
- zero markup changes -> all locked substrings/counts/scripts survive as bytes

Locked-rule safety:
- original body{}/.filter{}/.site h3{} first-match rules untouched (overrides come later)
- media-window blocks untouched; no new '.filters{grid-template-columns:1fr}' string
- main bare <script> and card articles byte-identical
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")

# ---------------- 1. :root palette flip ----------------
root_swaps = [
    ("--ink:#0a0a0d;--ink2:#0f0f14;--ink3:#14141a;",
     "--ink:#f7f3e8;--ink2:#f0ebdb;--ink3:#e9e3d0;"),
    ("--paper:#f1ede2;--paper2:#e6e1d2;",
     "--paper:#fbf7ec;--paper2:#f3eede;"),
    ("--text:#f4f2ec;--muted:#a09e96;--dim:#6d6c66;",
     "--text:#191510;--muted:#57534a;--dim:#7a766b;"),
    ("--line:rgba(244,242,236,.13);--line2:rgba(244,242,236,.06);",
     "--line:rgba(23,19,16,.16);--line2:rgba(23,19,16,.08);"),
    ("--flame:#ff4b1f;--flame2:#ff7a3c;--flame-tint:rgba(255,75,31,.07);",
     "--flame:#e8401a;--flame2:#f06a2c;--flame-tint:rgba(232,64,26,.08);"),
    # lime stays vivid for fills (CTA/active filter/badge/selection); text uses overridden below
    ("--lime-soft:rgba(198,255,63,.85);--lime-tint:rgba(198,255,63,.08);",
     "--lime-soft:rgba(92,107,18,.9);--lime-tint:rgba(92,107,18,.09);"),
    ("--electric:#3fd8ff;", "--electric:#0e7f9d;"),
    ("--green:#5fe3a1;--cyan:#5ad8ff;", "--green:#1f8a5a;--cyan:#0e7f9d;"),
]
for old, new in root_swaps:
    assert html.count(old) == 1, f":root target missing: {old[:50]}"
    html = html.replace(old, new, 1)
print("[1] :root palette flipped to cream/ink")

# ---------------- 2. theme-color meta ----------------
old_meta = '<meta name="theme-color" content="#0a0a0d">'
assert html.count(old_meta) == 1
html = html.replace(old_meta, '<meta name="theme-color" content="#f7f3e8">', 1)
print("[2] theme-color meta updated")

# ---------------- 3. light-theme override block ----------------
override_css = """
/* ---- v3: cream editorial light theme (dark terminal anchors kept) ---- */
html{color-scheme:light}
body:before{background:radial-gradient(680px circle at var(--mx) var(--my),rgba(232,64,26,.075),transparent 62%),radial-gradient(760px circle at 4% 106%,rgba(92,107,18,.06),transparent 60%),radial-gradient(560px circle at 96% 88%,rgba(14,127,157,.05),transparent 62%)}
.grain{opacity:.035}
:focus-visible{outline:2px solid var(--flame);outline-offset:3px}

/* nav */
.nav-links{color:#57534a}
.nav-links>a:hover{color:var(--flame)}
.nav-command{border-color:rgba(23,19,16,.2);background:rgba(23,19,16,.03);color:#3d3a33}
.nav-command:hover,.nav-command:focus-visible{border-color:rgba(92,107,18,.6);background:rgba(198,255,63,.3);color:#191510}

/* hero */
.hero-badge text{fill:#7a766b}
.eyebrow{color:#6b675e}
.gradient-word{background:linear-gradient(92deg,#e8401a 8%,#f59e0b 42%,#6b8f00 78%,#0e7f9d);-webkit-background-clip:text;background-clip:text;color:transparent}
.lede{color:#57534a}
.lede strong{color:#191510}
.btn-primary{box-shadow:0 10px 30px rgba(232,64,26,.2)}
.btn-ghost{color:#3d3a33}
.btn-ghost:hover{border-color:rgba(23,19,16,.4);background:rgba(23,19,16,.05)}
.hero-credo{color:#7a766b}

/* dark terminal anchors: re-scope border vars to light-on-dark */
.shipping-engine,.system-log,.changelog,.palette{--line:rgba(244,242,236,.13);--line2:rgba(244,242,236,.08)}
.shipping-engine{background:linear-gradient(160deg,#1a1a24,#12121a 52%,#1d1613);border-color:rgba(23,19,16,.4);color:#f4f2ec}
.engine-stage strong{color:#f4f2ec}

/* bands */
.band.ghost .band-set{color:transparent;-webkit-text-stroke:1px rgba(23,19,16,.38)}
.band.ghost .band-set i{color:var(--flame);-webkit-text-stroke:0}

/* sections */
.kicker{color:#6b675e}
.section-copy{color:#57534a}
.section-copy strong{color:#191510}

/* release rally */
.release-rally{border-color:rgba(92,107,18,.4);background:radial-gradient(460px circle at 90% 20%,rgba(232,64,26,.16),transparent 66%),linear-gradient(120deg,rgba(198,255,63,.22),rgba(255,253,244,.5))}
.release-rally:before{color:rgba(232,64,26,.1)}
.release-rally small{color:#7a766b}
.release-rally strong em{background:linear-gradient(92deg,var(--flame),#6b8f00);-webkit-background-clip:text;background-clip:text;color:transparent}
.release-rally span{color:#7a766b}

/* ledger */
.release-ledger{background:#fffdf4;box-shadow:0 24px 70px rgba(23,19,16,.09)}
.filters-wrap{background:rgba(247,243,232,.92)}
.filter{background:rgba(23,19,16,.03);color:#57534a}
.filter:hover{color:#191510;border-color:rgba(92,107,18,.55)}
.visible-count{color:#8a887f}
.site:hover{background:linear-gradient(90deg,rgba(92,107,18,.06),rgba(23,19,16,.015))}
.site-category{color:#d63d12}
.site-meta{color:#7a766b}
.site-meta span:first-child{color:#5c6b12}
.site p{color:#57534a}
.site-link{color:#191510}
.site-date{color:#8a887f}
.site-shot{background:#e9e3d3;border-color:rgba(23,19,16,.14)}
.site:hover .site-shot{border-color:rgba(92,107,18,.55)}

/* timeline */
.tl-item{background:#fffdf4}
.tl-item:hover{background:rgba(198,255,63,.18);border-color:rgba(92,107,18,.5)}
.tl-item:before{border-color:#6b8f00}
.tl-item.latest{border-color:rgba(92,107,18,.6);box-shadow:0 0 30px rgba(92,107,18,.12)}
.tl-item.latest:before{background:#6b8f00}
.tl-date{color:#5c6b12}
.tl-names span{color:#191510}
.tl-count{color:#6b675e}
.tl-rail{scrollbar-color:rgba(92,107,18,.4) transparent}

/* system */
.system-grid{background:#fffdf4}
.system-step p{color:#57534a}
.system-step:hover{background:rgba(198,255,63,.16)}
.system-log{box-shadow:0 18px 50px rgba(23,19,16,.12)}
.system-status{color:#5c6b12;border-color:rgba(92,107,18,.45)}

/* contact */
.contact-card{background:linear-gradient(150deg,rgba(232,64,26,.09),rgba(255,253,244,.4) 46%);box-shadow:0 24px 70px rgba(23,19,16,.08)}
.contact-main p{color:#57534a}
.contact-fire{color:#191510}
.contact-side{background:rgba(23,19,16,.035)}
.contact-note{color:#57534a}
.copy-status{color:#4a6b00}

/* footer */
.footer{color:#7a766b}
.footer a:hover{color:var(--flame)}

/* changelog stays dark; soften outer shadow for light page */
.changelog{box-shadow:0 22px 60px rgba(23,19,16,.16)}

/* cursor glow reads as warm sunlight on cream */
.glow-dot{background:radial-gradient(circle,rgba(232,64,26,.11),rgba(92,107,18,.07) 46%,transparent 70%);mix-blend-mode:multiply}
"""

anchor = "</style>"
assert html.count(anchor) == 1
html = html.replace(anchor, override_css + anchor, 1)
print("[3] light-theme override block injected")

# ---------------- 4. self-checks (full v2 trap set + v3 markers) ----------------
checks = []


def ck(name, cond):
    checks.append((name, cond))


ck("cards==28", html.count('<article class="site" data-status="live">') == 28)
ck("data-status==28", html.count('data-status="live"') == 28)
ck("data-category==28", html.count('data-category=') == 28)
ck("visit-link==28", html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 28)
ck("release-ledger attr", 'class="release-ledger"' in html)
ck("visibleCount", 'id="visibleCount" aria-live="polite">ALL RELEASES' in html)
for v in ("all", "ai", "game", "tool", "creative"):
    ck(f"filter {v}", f'data-filter="{v}"' in html)
ck("body first-match", "font-feature-settings:normal" in re.search(r"body\{([^}]*)\}", html).group(1))
ck("filter first-match", "border:1px solid var(--line2)" in re.search(r"\.filter\{([^}]*)\}", html).group(1))
h3_rule = re.search(r"\.site h3\{([^}]*)\}", html).group(1)
ck("site h3 wrap", "overflow-wrap:anywhere" in h3_rule and "font-size:clamp(25px,8vw,28px)" in h3_rule)
m_start = html.index("@media(max-width:700px){")
m_end = html.index("@media(max-width:360px){", m_start)
mcss = html[m_start:m_end]
ck("mobile meta 11px", "font-size:11px" in re.search(r"\.site-category,\.site-meta\{([^}]*)\}", mcss).group(1))
ck("mobile link 12px", "font-size:12px" in re.search(r"\.site-link\{([^}]*)\}", mcss).group(1))
ck("filters 1fr 1fr", ".filters{display:grid;grid-template-columns:1fr 1fr}" in html)
ck("no filters 1fr only", ".filters{grid-template-columns:1fr}" not in html)
plausible = '<script defer data-domain="wangzifan.store" src="https://plausible.shipsolo.io/js/script.js"></script>'
ck("plausible==1", html.count(plausible) == 1)
ck("modal focus", "modal.querySelector('a').focus()" in html)
ck("howmanysleeps wbr", "<h3>HowManySleeps<wbr>Until</h3>" in html)
ck("favicon link", '<link rel="icon" href="favicon.svg" type="image/svg+xml">' in html)
for phrase in ("先把想法做出来", "再让世界给答案。", "SHIPPING ENGINE", "不把灵感收藏起来",
               "少一点等待", "多一次真实发布", "上线就是时机", "下一件值得上线的事",
               "现在就开始", "Founder Manifesto", "全部上线记录", "把想法做成网址",
               "wang1227928718", "复制微信号", 'aria-live="polite"'):
    ck(f"phrase {phrase[:8]}", phrase in html)
for step in ("判断", "构建", "上线", "反馈"):
    ck(f"step {step}", f'data-step="{step}"' in html)
order = ['id="top"', 'id="work"', 'id="system"', 'id="manifesto"', 'id="contact"']
pos = [html.index(s) for s in order]
ck("section order", pos == sorted(pos))
for banned in ("主业", "项目经理", "项目管理", "Project Management", "个人履历", "Resume",
               "工作经历", "26 个产品", "6 项证书", "六个重点产品", "Selected Deployments",
               'id="proof"', 'data-featured="true"', "全部 28", "AI 产品 3",
               "游戏与内容 9", "实用工具 9", "创意实验 7"):
    ck(f"banned {banned[:8]}", banned not in html)
ck("craveloop href==1", html.count('href="https://foodnevercomes.online/"') == 1)
ck("niulai href==1", html.count('href="https://niulai.blog/"') == 1)
first_script = re.search(r"<script>\s*([\s\S]*?)</script>", html)
ck("first bare script is interactions",
   "const filters=[...document.querySelectorAll('.filter')]" in first_script.group(1))
ck("timeline present", 'id="timeline"' in html and len(re.findall(r'class="tl-item[ "]', html)) == 18)
ck("changelog present", html.count('class="log-line"') == 28)
_open = len(re.findall(r"<script[\s>]", html))
_close = html.count("</script>")
ck("script tags balanced", _open == _close)
# v3 markers
ck("cream ink", "--ink:#f7f3e8" in html)
ck("ink text", "--text:#191510" in html)
ck("color-scheme light", "html{color-scheme:light}" in html)
ck("dark engine kept", "#1a1a24" in html)
ck("dark changelog kept", "background:#0b0b0f" in html)
ck("dark palette kept", "background:#121218" in html)
ck("no old ink root", "--ink:#0a0a0d" not in html)
ck("theme-color cream", '<meta name="theme-color" content="#f7f3e8">' in html)

failed = [n for n, c in checks if not c]
if failed:
    print("SELF-CHECK FAILURES:", failed)
    sys.exit(1)
print(f"[4] self-checks: {len(checks)}/{len(checks)} OK")

html_path.write_text(html, encoding="utf-8")
print(f"written: {html_path} ({len(html) // 1024}KB)")
