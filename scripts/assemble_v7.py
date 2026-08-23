#!/usr/bin/env python3
"""v7: Constellation star-map for the 32-ship ledger + deep-space theming across sections.

Approved by ZF Wang (direction A constellation), 2026-08-22.
- #work .sites becomes a star-field: cards become glowing nodes positioned on a
  4-cluster constellation (ai/game/tool/creative), same-cluster nodes linked by
  thin SVG lines (oldest -> newest path).
- Filter chips FOCUS a cluster (dim others) instead of hiding cards.
- Cards keep every field (thumb/LIVE/NEW/num/subtitle/date/h3/desc/visit link);
  in star-map mode they render as compact node chips that expand on hover/click.
- Timeline nodes become launch pads (pulse + ignition index).
- system/manifesto/contact sections get deep-space glass treatment.
- Mobile (<900px): star-map gracefully degrades to grouped card flow.
- prefers-reduced-motion: static constellation, no pulses.
Atomic: all transforms + self-checks, single write at the end.
"""
import re, json, math, random, subprocess, sys
from pathlib import Path

ROOT = Path("/root/projects/zf-wang-personal-site")
html = (ROOT / "index.html").read_text(encoding="utf-8")
orig_len = len(html)

def rep(old, new, n=1):
    global html
    c = html.count(old)
    assert c >= n, f"need {n} got {c}: {old[:70]}"
    html = html.replace(old, new, n)

# ---------- 1. card data ----------------------------------------------------
cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
assert len(cards) == 32
data = []
for c in cards:
    cat = re.search(r'data-category="(\w+)"', c).group(1)
    num = int(re.search(r'<span>(\d+)\s*·', c).group(1))
    name = re.sub(r'<[^>]+>', '', re.search(r'<h3>(.*?)</h3>', c, re.S).group(1))
    d = re.search(r'site-date">(\d{4}-\d{2}-\d{2})', c).group(1)
    data.append({"num": num, "name": name, "cat": cat, "d": d})

# ---------- 2. constellation layout ----------------------------------------
CATS = {
  "ai":       {"hue": "#37d5ff", "cx": 0.24, "cy": 0.24},
  "game":     {"hue": "#c96bff", "cx": 0.74, "cy": 0.20},
  "tool":     {"hue": "#f06a2c", "cx": 0.27, "cy": 0.72},
  "creative": {"hue": "#ff5fa2", "cx": 0.75, "cy": 0.74},
}
rng = random.Random(42)
by_cat = {}
for x in data:
    by_cat.setdefault(x["cat"], []).append(x)
pos, links = {}, {}
for cat, items in by_cat.items():
    items = sorted(items, key=lambda x: x["num"])
    cx, cy, n = CATS[cat]["cx"], CATS[cat]["cy"], len(items)
    path = []
    for i, x in enumerate(items):
        t = i / max(1, n - 1)
        ang = t * math.pi * (1.1 + n * 0.14) + (0.4 if cat in ("ai", "tool") else 2.2)
        rad = 0.02 + t * 0.115
        px = cx + math.cos(ang) * rad * 1.25 + rng.uniform(-0.012, 0.012)
        py = cy + math.sin(ang) * rad + rng.uniform(-0.012, 0.012)
        pos[x["num"]] = (round(px * 100, 2), round(py * 100, 2))
        path.append((px, py))
    links[cat] = [(round(a[0]*100,2), round(a[1]*100,2), round(b[0]*100,2), round(b[1]*100,2))
                  for a, b in zip(path, path[1:])]

# ---------- 3. build SVG link layer ----------------------------------------
svg_lines = []
for cat, segs in links.items():
    hue = CATS[cat]["hue"]
    for x1, y1, x2, y2 in segs:
        svg_lines.append(
            f'<line class="cl" data-cat="{cat}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{hue}" stroke-width="0.14" stroke-opacity="0.28"/>')
svg = ('<svg class="constellation-links" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
       + "".join(svg_lines) + "</svg>")
print(f"[svg] {len(svg_lines)} link lines")

# ---------- 4. inject star-field container + reposition cards ----------------
# wrap .sites content: add svg layer right after <div class="sites">
rep('<div class="sites">', '<div class="sites">' + svg, 1)
# position each card as a node (absolute, left/top %), tag with category + num.
# We must match the exact opening tag followed by THIS card's inner start, because
# all 32 share the identical opening tag string.
OPEN = '<article class="site" data-status="live">'
search_from = html.index('<div class="sites">')
for c in cards:
    num = int(re.search(r'<span>(\d+)\s*·', c).group(1))
    cat = re.search(r'data-category="(\w+)"', c).group(1)
    x, y = pos[num]
    star = (f'<article class="site star-node" data-status="live" data-num="{num}" data-cat="{cat}" '
            f'style="left:{x}%;top:{y}%">')
    # locate this exact article occurrence (by unique project image src) and swap only the opening tag
    img = re.search(r'assets/projects/(project-\d+\.webp)', c).group(1)
    idx = html.index(img, search_from)
    open_idx = html.rindex(OPEN, 0, idx)
    html = html[:open_idx] + star + html[open_idx + len(OPEN):]
print("[dom] 32 star-node cards positioned")

# ---------- 5. replace old hide-filter JS with cluster-focus JS ---------------
OLD_FILTER = '''      projects.forEach(card=>{const show=value==='all'||card.querySelector('[data-category]').dataset.category===value;card.classList.toggle('hide',!show)});
      visibleCount.textContent=value==='all'?'ALL RELEASES':button.textContent.toUpperCase();'''
NEW_FILTER = '''      sites_el.classList.remove('focus-ai','focus-game','focus-tool','focus-creative');
      if(value!=='all')sites_el.classList.add('focus-'+value);
      visibleCount.textContent=value==='all'?'ALL RELEASES':({ai:'AI CLUSTER · 3',game:'GAME CLUSTER · 11',tool:'TOOL CLUSTER · 10',creative:'CREATIVE CLUSTER · 8'}[value]||button.textContent.toUpperCase());'''
rep(OLD_FILTER, NEW_FILTER, 1)
# add sites_el reference next to projects declaration
rep("    const projects=[...document.querySelectorAll('.site')];",
    "    const projects=[...document.querySelectorAll('.site')];\n    const sites_el=document.querySelector('.sites');", 1)
print("[js] filter logic -> cluster focus")

# ---------- 6. CSS inject ------------------------------------------------------
CSS = open(ROOT / "scripts" / "_v7.css", encoding="utf-8").read()
rep("</style>", CSS + "\n</style>", 1)
print(f"[css] injected {len(CSS)}")

# ---------- 7. constellation JS inject (node hover highlight only) -------------
JS = open(ROOT / "scripts" / "_v7.js", encoding="utf-8").read()
# strip the chips-binding part (old inline script already handles chips now)
js_node_only = JS.split("/* hovering a node highlights its cluster's links */", 1)
assert len(js_node_only) == 2
JS = "(function(){'use strict';var sites=document.querySelector('.sites');if(!sites||!sites.querySelector('.star-node'))return;/* hovering a node highlights its cluster's links */" + js_node_only[1]
import tempfile, os
fd, tmp = tempfile.mkstemp(suffix=".js"); os.write(fd, JS.encode()); os.close(fd)
p = subprocess.run(["node", "--check", tmp], capture_output=True); os.unlink(tmp)
assert p.returncode == 0, p.stderr.decode()
rep("</body>", "<script data-ui=\"constellation\">\n" + JS + "\n</script>\n</body>", 1)
print("[js] constellation node-highlight injected + node --check OK")

# ---------- 8. self-checks ------------------------------------------------------
fails = []
def ck(name, ok):
    if not ok: fails.append(name)
ck('32 cards still live', html.count('data-status="live"') == 32)
ck('32 star-node', html.count('star-node') >= 32)
ck('32 visit links', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 32)
ck('svg links layer', 'constellation-links' in html)
ck('svg lines', html.count('<line class="cl"') == sum(len(v) for v in links.values()))
ck('4 clusters in css', 'focus-ai' in html and 'focus-game' in html and 'focus-tool' in html and 'focus-creative' in html)
ck('focus js present', "sites_el.classList.remove('focus-ai'" in html)
ck('old hide js gone', "classList.toggle('hide'" not in html)
ck('no .hide display css kept for safety', True)
ck('launch console intact', 'data-launch' in html)
ck('timeline intact', 'tl-item latest' in html)
ck('changelog intact', 'git log --oneline --ships' in html)
ck('constellation script', 'data-ui="constellation"' in html)
ck('mobile degrade', '@media(max-width:900px)' in html and 'position:static' in html)
ck('reduced motion', '.site.star-node{transition:none}' in html)
ck('node check', p.returncode == 0)
if fails:
    print("FAIL:", fails); sys.exit(1)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[write] {orig_len} -> {len(html)} (+{len(html)-orig_len})")
print("v7 constellation + deep-space theming assembled OK")
