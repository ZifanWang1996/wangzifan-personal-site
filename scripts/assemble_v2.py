#!/usr/bin/env python3
"""v2 upgrade assembly: thumbs + badges + dates + timeline + changelog + fx.

Test-locked constraints honored:
- card <article> open/close and locked substrings pass through as bytes;
  insertions are appended AFTER locked anchors inside each card.
- workflow allowlist untouched (thumbs inlined as base64, no new publish files).
- main bare <script> block kept byte-identical; fx script uses data-ui="fx" attribute.
"""
import base64
import io
import re
import sys
from collections import OrderedDict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parents[1]
html_path = ROOT / "index.html"
orig = html_path.read_text(encoding="utf-8")

FR = ROOT / "scripts"
css_card = (FR / "fr_card.css").read_text(encoding="utf-8")
css_fx = (FR / "fr_fx.css").read_text(encoding="utf-8")
fx_js = (FR / "fr_fx.js").read_text(encoding="utf-8")

# ---------------- 1. thumbnails -> base64 ----------------
THUMB_BY_DOMAIN = {
    "aistorynest.mom": "01-aistorynest",
    "buildahooper.best": "02-buildahooper",
    "falloutday.online": "03-falloutday",
    "palworldmap.best": "04-palworldmap",
    "codexskin.space": "05-codexskin",
    "llmstxt.best": "06-llmstxt",
    "allwishescometrue.site": "07-allwishes",
    "taskbarherowiki.best": "08-taskbarhero",
    "chinesecashcoins.wiki": "09-chinesecoins",
    "rotcheck.cyou": "10-rotcheck",
    "spiritvale.blog": "11-spiritvale",
    "dragonswordawakening.fun": "12-dragonsword",
    "copyplaintext.com": "13-copyplaintext",
    "isitdown.click": "14-isitdown",
    "howmanysleepsuntil.rest": "15-sleepsuntil",
    "cashflow.lifestyle": "16-cashflow",
    "zhuzhiliao.buzz": "17-zhuzhiliao",
    "shiftatmidnight.blog": "18-shiftatmidnight",
    "mergeanuke.space": "19-mergeanuke",
    "aiscanner.run": "20-aiscanner",
    "rspeditor.app": "21-rspeditor",
    "remove-matcha-filter.com": "22-matcha-rmf",
    "deepseekharness.site": "23-deepseekharness",
    "polskipilkarzsymulator.online": "24-polskipilkarz",
    "burncd.xyz": "25-burncd",
    "matchafilter.cc": "26-matchafilter",
    "foodnevercomes.online": "27-craveloop",
    "niulai.blog": "28-niulai",
}
DATES = {
    "aistorynest.mom": "2026-07-12",
    "buildahooper.best": "2026-07-12",
    "falloutday.online": "2026-07-12",
    "palworldmap.best": "2026-07-14",
    "codexskin.space": "2026-07-17",
    "llmstxt.best": "2026-07-18",
    "allwishescometrue.site": "2026-07-25",
    "taskbarherowiki.best": "2026-07-26",
    "chinesecashcoins.wiki": "2026-07-26",
    "rotcheck.cyou": "2026-07-26",
    "spiritvale.blog": "2026-07-28",
    "dragonswordawakening.fun": "2026-07-29",
    "copyplaintext.com": "2026-07-31",
    "isitdown.click": "2026-07-31",
    "howmanysleepsuntil.rest": "2026-07-31",
    "cashflow.lifestyle": "2026-08-03",
    "zhuzhiliao.buzz": "2026-08-04",
    "shiftatmidnight.blog": "2026-08-05",
    "mergeanuke.space": "2026-08-08",
    "aiscanner.run": "2026-08-09",
    "rspeditor.app": "2026-08-09",
    "remove-matcha-filter.com": "2026-08-12",
    "deepseekharness.site": "2026-08-15",
    "polskipilkarzsymulator.online": "2026-08-16",
    "burncd.xyz": "2026-08-16",
    "matchafilter.cc": "2026-08-16",
    "foodnevercomes.online": "2026-08-16",
    "niulai.blog": "2026-08-17",
}

b64map = {}
total = 0
for dom, stem in THUMB_BY_DOMAIN.items():
    im = Image.open(ROOT / "thumbs" / f"{stem}.webp").convert("RGB")
    im = im.resize((400, 250), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=62, method=6)
    raw = buf.getvalue()
    total += len(raw)
    b64map[dom] = base64.b64encode(raw).decode()
print(f"[1] thumbs base64: {len(b64map)} images, binary {total // 1024}KB, b64 ~{total * 4 // 3 // 1024}KB")

# ---------------- 2. card surgery ----------------
card_re = re.compile(r'<article class="site" data-status="live">.*?</article>', re.S)
cards = card_re.findall(orig)
assert len(cards) == 28, f"expected 28 cards, got {len(cards)}"

html = orig
meta_rows = []
for idx, card in enumerate(cards, 1):
    dom_m = re.search(r'href="https://([^/"]+)/"', card)
    assert dom_m, f"card {idx} has no href"
    dom = dom_m.group(1)
    cat_m = re.search(r'<div data-category="\w+">', card)
    pair_m = re.search(r'<span>[^<]*已上线</span><span>([^<]+)</span>', card)
    h3_m = re.search(r"<h3>([\s\S]*?)</h3>", card)
    assert cat_m and pair_m and h3_m and dom in DATES, f"card {idx} parse fail"
    h3_plain = re.sub(r"<[^>]+>", "", h3_m.group(1))
    date = DATES[dom]
    meta_rows.append((idx, dom, h3_plain, pair_m.group(1), date))
    fig = (
        '<figure class="site-shot" aria-hidden="true">'
        '<span class="site-badge"><i></i>LIVE</span>'
        f'<img src="data:image/webp;base64,{b64map[dom]}" alt="" loading="lazy" decoding="async">'
        "</figure>"
    )
    new_card = card.replace(cat_m.group(0), cat_m.group(0) + fig, 1)
    new_card = new_card.replace(
        pair_m.group(0), pair_m.group(0) + f'<span class="site-date">{date}</span>', 1
    )
    assert new_card != card
    html = html.replace(card, new_card, 1)

assert html.count('data-category=') == 28
assert html.count('data-status="live"') == 28
assert html.count('class="site-shot"') == 28
assert html.count('class="site-badge"') == 28
assert html.count('class="site-date"') == 28
print("[2] card surgery: 28 cards upgraded")

# ---------------- 3. base-grid rewrite (unlocked CSS rules) ----------------
rewrites = [
    (
        ".site>div{min-width:0;display:grid;grid-template-columns:150px minmax(220px,.85fr) minmax(250px,1.2fr);align-items:center;gap:30px}",
        ".site>div{min-width:0;display:grid;grid-template-columns:176px 150px minmax(0,.78fr) minmax(0,1.1fr);align-items:center;gap:30px}",
    ),
    (".site-category{grid-column:1;grid-row:1;", ".site-category{grid-column:2;grid-row:1;"),
    (".site-meta{grid-column:1;grid-row:2;", ".site-meta{grid-column:2;grid-row:2;"),
    (".site h3{grid-column:2;grid-row:1/3;", ".site h3{grid-column:3;grid-row:1/3;"),
    (".site p{grid-column:3;grid-row:1/3;", ".site p{grid-column:4;grid-row:1/3;"),
]
for old, new in rewrites:
    assert html.count(old) == 1, f"rewrite target missing: {old[:60]}"
    html = html.replace(old, new, 1)
print("[3] base grid rewritten")

# ---------------- 4. insert new CSS before </style> ----------------
anchor = "</style>"
assert html.count(anchor) == 1
html = html.replace(anchor, css_card + css_fx + anchor, 1)
print("[4] new CSS injected")

# ---------------- 5. timeline + changelog generated from meta_rows ----------------
by_date = OrderedDict()
for idx, dom, name, label, date in meta_rows:
    by_date.setdefault(date, []).append(name)
tl_items = []
last_date = list(by_date.keys())[-1]
for date, names in by_date.items():
    cls = " latest" if date == last_date else ""
    names_html = "".join(f"<span>{n}</span>" for n in names)
    cnt = f"{len(names)} SHIPPED" if len(names) > 1 else "1 SHIPPED"
    tl_items.append(
        f'<div class="tl-item{cls}"><div class="tl-date">{date}</div>'
        f'<div class="tl-names">{names_html}</div><div class="tl-count">{cnt}</div></div>'
    )
tl_html = (
    '\n    <section class="shell section" id="timeline" aria-labelledby="timeline-title">\n'
    '      <div class="section-top reveal"><div><div class="kicker">02 / Shipping Timeline</div>'
    '<h2 id="timeline-title">37 天，28 次真实上线。</h2></div>'
    '<p class="section-copy"><strong>日期不会说谎。</strong>从第一个产品到第 28 个，'
    "每一次上线都在同一条时间轴上留下坐标。横向滚动，查看完整的发布节奏。</p></div>\n"
    '      <div class="tl-rail-wrap reveal"><div class="tl-rail">'
    + "".join(tl_items)
    + "</div></div>\n    </section>\n"
)

log_lines = []
for idx, dom, name, label, date in reversed(meta_rows):
    log_lines.append(
        f'<div class="log-line"><span class="log-d">[{date}]</span>'
        f'<span class="log-ok">SHIP</span><span class="log-n">{name}</span>'
        f'<span class="log-u">→ https://{dom}/</span></div>'
    )
log_html = (
    '<div class="changelog reveal"><div class="chrome"><i></i><i></i><i></i>'
    "<span>~/venture-os — release.log — 28 entries</span></div>"
    '<div class="log-body"><div class="prompt-line">$ git log --oneline --ships | '
    f'<b>{len(meta_rows)} releases</b></div>'
    + "".join(log_lines)
    + "</div></div>"
)

tl_anchor = '<div class="band ghost" aria-hidden="true">'
assert html.count(tl_anchor) == 1
html = html.replace(tl_anchor, tl_html + "\n    " + tl_anchor, 1)

log_anchor = '<div class="system-log reveal">'
assert html.count(log_anchor) == 1
html = html.replace(log_anchor, log_html + "\n      " + log_anchor, 1)
print(f"[5] timeline ({len(tl_items)} dates) + changelog ({len(log_lines)} lines) inserted")

# renumber kickers: timeline takes 02, everything after shifts
renum = [
    ("02 / OPC Operating System", "03 / OPC Operating System"),
    ("03 / Founder Manifesto", "04 / Founder Manifesto"),
    ("04 / Collaboration", "05 / Collaboration"),
]
for old, new in renum:
    assert html.count(old) == 1, f"renumber target missing: {old}"
    html = html.replace(old, new, 1)
print("[5b] kickers renumbered")

# ---------------- 6. fx script after motion script ----------------
# IMPORTANT: motion_end must NOT include motion's closing </script> tag —
# replacing it would splice the fx opening tag into motion's script body.
motion_end = "</script>\n</body>"
assert html.count(motion_end) == 1
fx_block = '</script>\n  <script data-ui="fx">\n' + fx_js + "\n  </script>\n</body>"
html = html.replace(motion_end, fx_block, 1)
assert html.count('<script data-ui="fx">') == 1
_open = len(re.findall(r"<script[\s>]", html))
_close = html.count("</script>")
assert _open == _close, f"script tag mismatch: {_open} open vs {_close} close"
print("[6] fx script inserted")

# ---------------- 7. self-checks (mirror every pytest trap) ----------------
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
ck("timeline present", 'id="timeline"' in html and len(re.findall(r'class="tl-item[ "]', html)) == len(by_date))
ck("changelog present", html.count('class="log-line"') == 28)

failed = [n for n, c in checks if not c]
if failed:
    print("SELF-CHECK FAILURES:", failed)
    sys.exit(1)
print(f"[7] self-checks: {len(checks)}/{len(checks)} OK")

html_path.write_text(html, encoding="utf-8")
print(f"written: {html_path} ({len(html) // 1024}KB)")
