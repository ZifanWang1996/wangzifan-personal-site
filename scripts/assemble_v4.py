#!/usr/bin/env python3
"""v4 assemble: filter count chips + subhead count chip + card #29 (HLLV Field Manual).

Pure incremental transform on the v3 cream theme:
- 5 filter buttons get data-count chips rendered via CSS ::after
  (button.textContent stays clean -> live status bar contract unchanged)
- subhead h3 gets <span class="ledger-count">29</span>
- timeline title 28 -> 29; HLLV joins the 2026-08-17 latest item (first public
  Pages deployment = 08-17, verified via `wrangler pages deployment list`;
  08-16 was first code commit only)
- changelog 28 -> 29 entries/releases + new HLLV log line at top (08-17)
- new card #29 (game) with base64-inlined thumb (workflow allowlist untouched)
- main inline script untouched (Node interaction contract preserved)
"""
import base64, io, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
orig_len = len(html)

def rep(old, new, n=1):
    global html
    c = html.count(old)
    assert c == n, f"expected {n} occurrence(s), found {c}: {old[:70]!r}"
    html = html.replace(old, new)

# ---------------- 1. HLLV thumb -> base64 (400x250, same pipeline as v2) ----
im = Image.open(ROOT / "thumbs" / "29-hllv.webp").convert("RGB")
im = im.resize((400, 250), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "WEBP", quality=82)
b64 = base64.b64encode(buf.getvalue()).decode()
print(f"[1] hllv thumb: 400x250, {len(buf.getvalue())//1024}KB, b64 {len(b64)//1024}KB")

# ---------------- 2. filter buttons: data-count chips (CSS ::after) ----------
# button.textContent must remain exactly the label — live status bar uses it.
rep('<button class="filter active" data-filter="all" aria-pressed="true">全部</button>',
    '<button class="filter active" data-filter="all" data-count="29" aria-pressed="true">全部</button>')
rep('<button class="filter" data-filter="ai" aria-pressed="false">AI 产品</button>',
    '<button class="filter" data-filter="ai" data-count="3" aria-pressed="false">AI 产品</button>')
rep('<button class="filter" data-filter="game" aria-pressed="false">游戏与内容</button>',
    '<button class="filter" data-filter="game" data-count="10" aria-pressed="false">游戏与内容</button>')
rep('<button class="filter" data-filter="tool" aria-pressed="false">实用工具</button>',
    '<button class="filter" data-filter="tool" data-count="9" aria-pressed="false">实用工具</button>')
rep('<button class="filter" data-filter="creative" aria-pressed="false">创意实验</button>',
    '<button class="filter" data-filter="creative" data-count="7" aria-pressed="false">创意实验</button>')

# ---------------- 3. subhead count chip --------------------------------------
rep('<h3>全部上线记录</h3>',
    '<h3>全部上线记录<span class="ledger-count">29</span></h3>')

# ---------------- 4. timeline: 29 launches, HLLV joins 2026-08-17 latest -----
rep('<h2 id="timeline-title">37 天，28 次真实上线。</h2>',
    '<h2 id="timeline-title">37 天，29 次真实上线。</h2>')
rep('从第一个产品到第 28 个，每一次上线都在同一条时间轴上留下坐标。',
    '从第一个产品到第 29 个，每一次上线都在同一条时间轴上留下坐标。')
rep('<div class="tl-names"><span>牛来</span></div><div class="tl-count">1 SHIPPED</div></div></div>',
    '<div class="tl-names"><span>牛来</span><span>HLLV Field Manual</span></div><div class="tl-count">2 SHIPPED</div></div></div>')

# ---------------- 5. changelog: 29 entries + HLLV log line -------------------
rep('~/venture-os — release.log — 28 entries',
    '~/venture-os — release.log — 29 entries')
rep('<b>28 releases</b>', '<b>29 releases</b>')
rep('<div class="log-line"><span class="log-d">[2026-08-17]</span><span class="log-ok">SHIP</span><span class="log-n">牛来</span>',
    '<div class="log-line"><span class="log-d">[2026-08-17]</span><span class="log-ok">SHIP</span><span class="log-n">HLLV Field Manual</span><span class="log-u">→ https://hellletloosevietnam.blog/</span></div><div class="log-line"><span class="log-d">[2026-08-17]</span><span class="log-ok">SHIP</span><span class="log-n">牛来</span>')

# ---------------- 6. new card #29 after the 牛来 card -------------------------
hllv_card = (
    '<article class="site" data-status="live"><div data-category="game">'
    '<figure class="site-shot" aria-hidden="true"><span class="site-badge"><i></i>LIVE</span>'
    f'<img src="data:image/webp;base64,{b64}" alt="" loading="lazy" decoding="async"></figure>'
    '<div class="site-category">游戏与内容</div>'
    '<div class="site-meta"><span>29 · 已上线</span><span>HLLV 越南战场手册</span><span class="site-date">2026-08-17</span></div>'
    '<h3>HLLV Field Manual</h3>'
    '<p>面向《Hell Let Loose: Vietnam》玩家的非官方野战手册，提供经来源核验的已知问题、新手指南、地图、兵种与模式情报，每条结论均标注日期与依据。</p>'
    '</div><a class="site-link" href="https://hellletloosevietnam.blog/" target="_blank" rel="noopener noreferrer">访问项目 ↗</a></article>'
)
m = re.search(r'<article class="site" data-status="live"><div data-category="creative">(?:(?!<article).)*?<h3>牛来</h3>.*?</article>', html, re.S)
assert m, "niulai card not found"
html = html[:m.end()] + hllv_card + html[m.end():]

# ---------------- 7. CSS: data-count chips (light-theme tuned) ---------------
css_v4 = """
/* v4: filter count chips via ::after (button text stays clean) + ledger chip */
.filter:after{content:attr(data-count);display:inline-block;margin-left:7px;padding:2px 7px;border-radius:999px;border:1px solid rgba(23,19,16,.18);color:#8a887f;font:700 9px var(--mono);letter-spacing:.04em;transition:inherit}
.filter:hover:after{border-color:rgba(92,107,18,.55);color:#57534a}
.filter.active:after,.filter[aria-pressed="true"]:after{background:rgba(20,20,10,.14);border-color:transparent;color:#14140a}
.ledger-count{display:inline-block;margin-left:12px;padding:5px 11px;border-radius:999px;background:#dff0a8;border:1px solid rgba(92,107,18,.5);color:#2a330c;font:700 11px var(--mono);letter-spacing:.08em;vertical-align:5px}
"""
rep('</style>', css_v4 + '</style>')

# ---------------- 8. self-checks ---------------------------------------------
checks = []
def ck(name, cond): checks.append((name, bool(cond)))

ck('cards live == 29', html.count('data-status="live"') == 29)
ck('article.site == 29', html.count('<article class="site" data-status="live">') == 29)
ck('data-category == 29', html.count('data-category=') == 29)
ck('visit links == 29', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 29)
ck('base64 imgs == 29', html.count('data:image/webp;base64,') == 29)
ck('data-count chips == 5', html.count('data-count="') == 5)
for v in ('29', '3', '10', '9', '7'):
    ck(f'data-count {v}', f'data-count="{v}"' in html)
ck('no i.filter-num', 'filter-num' not in html)
ck('ledger-count chip', '<span class="ledger-count">29</span>' in html)
ck('hllv card h3', '<h3>HLLV Field Manual</h3>' in html)
ck('hllv card href once', html.count('href="https://hellletloosevietnam.blog/"') == 1)
ck('hllv url text twice', html.count('https://hellletloosevietnam.blog/') == 2)
ck('hllv meta', '<span>29 · 已上线</span><span>HLLV 越南战场手册</span>' in html)
ck('hllv date 08-17', '<span class="site-date">2026-08-17</span>' in html)
ck('timeline title 37d 29', '37 天，29 次真实上线。' in html)
ck('timeline copy 29th', '从第一个产品到第 29 个' in html)
ck('tl 08-17 two shipped', '<div class="tl-count">2 SHIPPED</div>' in html)
ck('tl hllv name', '<span>HLLV Field Manual</span>' in html)
ck('tl latest has both', '<span>牛来</span><span>HLLV Field Manual</span>' in html)
ck('changelog 29 entries', 'release.log — 29 entries' in html)
ck('changelog 29 releases', '<b>29 releases</b>' in html)
ck('changelog hllv line top', '[2026-08-17]</span><span class="log-ok">SHIP</span><span class="log-n">HLLV Field Manual</span><span class="log-u">→ https://hellletloosevietnam.blog/</span>' in html)
ck('ledger heading kept', '全部上线记录' in html)
ck('modal link kept', '浏览全部上线记录' in html)
ck('visibleCount initial kept', 'id="visibleCount" aria-live="polite">ALL RELEASES' in html)
ck('main script kept', "filters.forEach(button=>button.addEventListener('click'" in html)
ck('button text clean', '全部</button>' in html and 'AI 产品</button>' in html and '游戏与内容</button>' in html)
ck('no stale 28 次', '28 次真实上线' not in html)
ck('no stale 28 entries', '28 entries' not in html)
ck('no stale 28 releases', '28 releases' not in html)
ck('no stale 第 28 个', '第 28 个' not in html)
ck('plausible kept', 'plausible.shipsolo.io/js/script.js' in html)
wf = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
ck('workflow allowlist untouched', 'install -m 0644 index.html _site/index.html' in wf and 'install -m 0644 privacy.html _site/privacy.html' in wf)
ck('cream theme kept', '.glow-dot{background:radial-gradient(circle,rgba(232,64,26,.11)' in html)

failed = [n for n, c in checks if not c]
if failed:
    print("SELF-CHECK FAILURES:", failed)
    sys.exit(1)
print(f"[8] self-checks: {len(checks)}/{len(checks)} OK")

(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[9] written: {orig_len} -> {len(html)} chars (+{len(html)-orig_len})")
