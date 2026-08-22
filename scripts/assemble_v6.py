#!/usr/bin/env python3
"""v6: Launch Console hero (deep-instrument theme) + site-wide upgrades.

Approved direction A (Launch Console) by ZF Wang, 2026-08-22.
- Hero becomes a full-viewport launch console: canvas starfield + 32 orbital
  ship pixels (mouse parallax + cursor attraction), T-minus countdown to the
  next ship (cadence-derived), telemetry feed of the 5 latest launches, and a
  32-cell status matrix (hover = tooltip, click = scroll to card).
- Scoped entirely under [data-launch] so the existing editorial (paper) zone
  keeps its identity; a gradient bridge eases the dark->paper transition.
- Card DOM untouched: all 32 <article class="site" data-status="live"> anchors
  and downstream assertions preserved.
- prefers-reduced-motion: static starfield, telemetry visible, no orbit/ticker.
"""
import re, json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
orig_len = len(html)

def rep(old, new, n=1):
    global html
    c = html.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    html = html.replace(old, new)

cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
assert len(cards) == 32, len(cards)
names = [re.sub(r'<[^>]+>', '', re.search(r'<h3>(.*?)</h3>', c, re.S).group(1)) for c in cards]
dates = [re.search(r'site-date">(\d{4}-\d{2}-\d{2})', c).group(1) for c in cards]
nums = [int(re.search(r'<span>(\d+)\s*·', c).group(1)) for c in cards]
ships = [{"n": nums[i], "name": names[i], "d": dates[i]} for i in range(31, -1, -1)]  # oldest..newest by real ship number
ship_js = json.dumps(ships, ensure_ascii=False)
tele = [{"name": names[i], "d": dates[i]} for i in range(5)]

# ---------------- hero DOM ---------------------------------------------------
tele_html = "".join(
    '<div class="tele-line"><span class="tele-dot"></span>'
    f'<span class="tele-date">[{t["d"]}]</span><span class="tele-verb">SHIP</span>'
    f'<span class="tele-name">{t["name"]}</span></div>' for t in tele)
dots = "".join(
    f'<button class="px" data-i="{i}" title="{m["name"]} · {m["d"]}" '
    f'aria-label="{m["name"]}, {m["d"]}"><i></i></button>'
    for i, m in enumerate(ships))

hero_new = (
    '<section class="shell hero" aria-labelledby="intro-title" data-launch>\n'
    '      <canvas class="orbit-canvas" aria-hidden="true"></canvas>\n'
    '      <div class="launch-head">\n'
    '        <div class="eyebrow"><span class="pulse"></span>LAUNCH CONSOLE · WZF-OS · ONLINE</div>\n'
    '        <div class="engine-status"><i></i>32 SHIPS LIVE</div>\n'
    '      </div>\n'
    '      <div class="launch-grid">\n'
    '        <div class="launch-copy reveal">\n'
    '          <h1 id="intro-title"><span>先把想法做出来，</span><span class="gradient-word">再让世界给答案。</span></h1>\n'
    '          <p class="lede">我是王子凡，一名持续构建、上线和迭代产品的 OPC 创业者。<strong>不等完美时机，用 AI 放大单人产能，把每一次真实发布变成下一次增长的起点。</strong></p>\n'
    '          <div class="hero-actions"><a class="btn btn-primary" href="#work">进入发布现场 <span>↘</span></a><a class="btn btn-ghost" href="#system">查看我的创业系统</a></div>\n'
    '          <div class="hero-credo"><span>不等万事俱备</span><i></i><span>只做真实上线</span><i></i><span>让每次发布产生复利</span></div>\n'
    '        </div>\n'
    '        <div class="launch-panel reveal">\n'
    '          <div class="tminus"><span class="tminus-label">T-MINUS NEXT SHIP</span><span class="tminus-val" id="tminus">--:--:--</span><span class="tminus-sub">avg cadence 1.3d / ship</span></div>\n'
    f'          <div class="telemetry" aria-label="最近发射遥测">{tele_html}</div>\n'
    '        </div>\n'
    '      </div>\n'
    f'      <div class="launch-matrix" role="list" aria-label="32 次发布状态矩阵">{dots}</div>\n'
    '    </section>')

hs = html.index('<section class="shell hero" aria-labelledby="intro-title">')
he = html.index('</section>', hs) + len('</section>')
html = html[:hs] + hero_new + html[he:]
print("[1] hero DOM replaced", he - hs, "->", len(hero_new))

# ---------------- bridge ------------------------------------------------------
rep('    </section>\n\n    <div class="band" aria-hidden="true">',
    '    </section>\n\n    <div class="launch-bridge" aria-hidden="true"></div>\n\n    <div class="band" aria-hidden="true">')
print("[2] bridge inserted")

# ---------------- CSS ---------------------------------------------------------
CSS = open(ROOT / "scripts" / "_v6.css", encoding="utf-8").read()
rep('</style>', CSS + '</style>')
print("[3] CSS injected:", len(CSS))

# ---------------- JS ----------------------------------------------------------
JS_TPL = open(ROOT / "scripts" / "_v6.js", encoding="utf-8").read()
JS = JS_TPL.replace('/*__SHIPS__*/', ship_js)
import tempfile, os
fd, tmp = tempfile.mkstemp(suffix=".js"); os.write(fd, JS.encode()); os.close(fd)
p = subprocess.run(["node", "--check", tmp], capture_output=True)
os.unlink(tmp)
assert p.returncode == 0, p.stderr.decode()
rep('</body>', '<script data-ui="launch">\n' + JS + '\n</script>\n</body>')
print("[4] JS injected + node --check OK; ships:", JS.count('"name"'))

# ---------------- self-checks -------------------------------------------------
ok = True
def ck(n, c):
    global ok
    if not c: print("FAIL:", n); ok = False

ck('32 live', html.count('data-status="live"') == 32)
ck('32 article anchor', html.count('<article class="site" data-status="live">') == 32)
ck('32 visit', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 32)
ck('32 matrix px', html.count('class="px"') == 32)
ck('5 telemetry', html.count('<div class="tele-line">') == 5)
ck('canvas', 'orbit-canvas' in html)
ck('data-launch', '[data-launch]{position:relative;min-height:calc(100vh - 78px)' in html)
ck('bridge css', '.launch-bridge{height:clamp(48px,9vh,120px)' in html)
ck('bridge div', '<div class="launch-bridge" aria-hidden="true"></div>' in html)
ck('intro-title', 'id="intro-title"' in html)
ck('5 chips', html.count('data-count="') == 5)
ck('ledger 32', '<span class="ledger-count">32</span>' in html)
ck('timeline title', '42 天，32 次真实上线' in html)
ck('wbr h3', '<h3>HowManySleeps<wbr>Until</h3>' in html)
ck('plausible', 'plausible.shipsolo.io/js/script.js' in html)
ck('no base64', 'data:image/webp;base64' not in html)
ck('launch script tag', '<script data-ui="launch">' in html)
ck('reduced guard', '@media(prefers-reduced-motion:reduce){\n  .tele-line{opacity:1;transform:none}' in html)

if not ok:
    sys.exit(1)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[5] written {orig_len} -> {len(html)} (+{len(html) - orig_len})")
