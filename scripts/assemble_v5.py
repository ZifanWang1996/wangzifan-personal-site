#!/usr/bin/env python3
"""v5 assemble: newest-first card grid + spotlight + living motion.

Design decision (approved by ZF Wang, plan A, 2026-08-22):
- project cards reorder to ship-date DESCENDING (latest first; same-day keeps
  publication order, i.e. higher card number first)
- latest release becomes a full-width SPOTLIGHT card; the rest flow into a
  responsive card grid (3 cols -> 2 cols -> 1 col)
- NEW badges for releases within 7 days of build; LATEST badge on spotlight
- hover lift + gradient top accent + image zoom; scroll-in reveal (the motion
  script now observes '.reveal,.site'); prefers-reduced-motion safe
- timeline rail flips to newest-first too (contract: timeline name sequence
  must equal card order); changelog stays newest-on-top
- card DOM structure is UNCHANGED (article.site anchor strings preserved for
  the 30+ test assertions); only order, badges and CSS change

Pure incremental transform on the current index.html (post-v4 state).
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DATE = date(2026, 8, 22)
NEW_CUTOFF = BUILD_DATE - timedelta(days=7)  # shipped >= 2026-08-15 -> NEW

html = (ROOT / "index.html").read_text(encoding="utf-8")
orig_len = len(html)


def rep(old, new, n=1):
    global html
    c = html.count(old)
    assert c == n, f"expected {n} occurrence(s), found {c}: {old[:70]!r}"
    html = html.replace(old, new)


# ---------------- 1. extract + reorder cards (date desc, num desc) ----------
cards = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
assert len(cards) == 31, f"expected 31 cards, found {len(cards)}"

def card_key(card):
    num = int(re.search(r'<span>(\d+)\s*·', card).group(1))
    shipped = re.search(r'<span class="site-date">(\d{4}-\d{2}-\d{2})</span>', card).group(1)
    return shipped, num

ordered = sorted(cards, key=card_key, reverse=True)
top = ordered[0]
assert '<h3>The Sinking City 2 Field Guide</h3>' in top, "newest card must be Sinking City 2"

# ---------------- 2. badges: NEW (7-day window) / LATEST (spotlight) --------
BADGE_ANCHOR = '<span class="site-badge"><i></i>LIVE</span>'
new_count = 0
badged = []
for i, card in enumerate(ordered):
    shipped = date.fromisoformat(card_key(card)[0])
    if i == 0:
        card = card.replace(BADGE_ANCHOR, BADGE_ANCHOR + '<span class="site-latest">★ 最新上线</span>')
    elif shipped >= NEW_CUTOFF:
        card = card.replace(BADGE_ANCHOR, BADGE_ANCHOR + '<span class="site-new">NEW</span>')
        new_count += 1
    badged.append(card)
print(f"[1] reordered desc; top=Sinking City 2; NEW badges={new_count}, LATEST=1")

first_pos = html.index(cards[0])
last_pos = html.index(cards[-1]) + len(cards[-1])
html = html[:first_pos] + '\n'.join(badged) + html[last_pos:]

# ---------------- 3. timeline rail: flip to newest-first --------------------
items = list(re.finditer(r'<div class="tl-item(?: latest)?">.*?</div></div>', html, re.S))
assert len(items) == 20, f"expected 20 timeline items, found {len(items)}"
blocks = []
for it in items:
    block = it.group(0).replace(' latest', '')
    names = re.search(r'<div class="tl-names">(.*?)</div>', block, re.S)
    spans = re.findall(r'<span>[^<]*</span>', names.group(1))
    flipped = ''.join(reversed(spans))
    block = block.replace(names.group(1), flipped)
    blocks.append(block)
blocks.reverse()
blocks[0] = blocks[0].replace('<div class="tl-item">', '<div class="tl-item latest">', 1)
html = html[:items[0].start()] + ''.join(blocks) + html[items[-1].end():]
print("[2] timeline flipped newest-first; latest marker moved to head")

# ---------------- 4. motion script: observe cards for scroll-in -------------
rep("var nodes=document.querySelectorAll('.reveal');",
    "var nodes=document.querySelectorAll('.reveal,.site');")

# ---------------- 5. subhead copy: newest-first hint -------------------------
rep('<p>Every release leaves a trail</p>',
    '<p>Every release leaves a trail · 最新在前</p>')

# ---------------- 6. v5 CSS: card grid + spotlight + motion ------------------
css_v5 = """
/* ---- v5: newest-first card grid + spotlight + living motion ---- */
.sites{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;padding:22px}
.site{display:flex;flex-direction:column;align-items:stretch;min-height:0;gap:0;padding:0;border:1px solid rgba(23,19,16,.12);border-radius:16px;background:#fffef8;overflow:hidden;transition:opacity .7s ease,transform .7s cubic-bezier(.19,.7,.22,1),translate .35s cubic-bezier(.19,.7,.22,1),box-shadow .35s,border-color .35s,background .3s}
.site:before{display:none}
.site:after{content:"";position:absolute;left:0;right:0;top:0;height:3px;z-index:2;background:linear-gradient(90deg,var(--flame),var(--lime) 55%,var(--electric));opacity:0;transition:opacity .35s}
.site:hover{background:#fffef8;border-color:rgba(92,107,18,.55);translate:0 -5px;box-shadow:0 20px 44px rgba(23,19,16,.13)}
.site:hover:after{opacity:1}
.site>div{display:flex;flex-direction:column;flex:1;min-width:0}
.site-category{order:1;margin:16px 18px 0}
.site h3{order:2;margin:9px 18px 0;font-size:20px;line-height:1.22}
.site p{order:3;margin:9px 18px 0;font-size:12.5px;line-height:1.7}
.site-meta{order:4;display:grid;grid-template-columns:1fr auto;gap:4px 12px;margin:auto 18px 0;padding-top:12px;border-top:1px dashed rgba(23,19,16,.14)}
.site-meta span:first-child,.site-date{white-space:nowrap}
.site-meta span:nth-child(2){grid-column:1/-1;grid-row:2}
.site-date{grid-column:2;grid-row:1}
.site-link{margin:16px 18px 18px;justify-content:center}
.site-shot{border-radius:0;border:0;border-bottom:1px solid rgba(23,19,16,.08);aspect-ratio:8/5}
.site-shot img{transition:filter .4s,transform .7s cubic-bezier(.19,.7,.22,1)}
.site:hover .site-shot img{transform:scale(1.05)}
/* spotlight: the latest release */
.site:first-child{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,1.18fr) minmax(0,1fr);background:linear-gradient(150deg,rgba(232,64,26,.06),rgba(255,253,244,.65) 42%),#fffef8}
.site:first-child>div{display:contents}
.site:first-child .site-shot{grid-column:1;grid-row:1/7;aspect-ratio:auto;height:100%;min-height:370px;border-bottom:0;border-right:1px solid rgba(23,19,16,.1)}
.site:first-child .site-category{grid-column:2;grid-row:1;margin:32px 34px 0}
.site:first-child h3{grid-column:2;grid-row:2;margin:12px 34px 0;font-size:clamp(27px,3vw,38px);line-height:1.08}
.site:first-child p{grid-column:2;grid-row:3;margin:16px 34px 0;font-size:14px;line-height:1.85}
.site:first-child .site-meta{grid-column:2;grid-row:4;display:flex;flex-direction:row;flex-wrap:wrap;gap:8px 18px;margin:20px 34px 0;padding-top:14px}
.site:first-child .site-link{grid-column:2;grid-row:5;margin:24px 34px 34px;justify-self:start}
.site:first-child:hover{translate:0 -3px}
/* badges */
.site-new{position:absolute;right:10px;top:10px;z-index:2;padding:4px 9px;border-radius:999px;background:var(--lime);color:#14140a;font:700 8.5px var(--mono);letter-spacing:.14em;box-shadow:0 6px 16px rgba(92,107,18,.35)}
.site-latest{position:absolute;right:10px;top:10px;z-index:2;padding:4px 10px;border-radius:999px;background:var(--flame);color:#fff7ee;font:700 8.5px var(--mono);letter-spacing:.14em;box-shadow:0 6px 18px rgba(232,64,26,.4)}
/* scroll-in motion (cards join the .reveal observer) + cascade stagger */
html.js .site{opacity:0;transform:translateY(30px)}
html.js .site.in{opacity:1;transform:none}
.sites>.site:nth-child(3n+2){transition-delay:.09s,.09s,0s,0s,0s,0s}
.sites>.site:nth-child(3n){transition-delay:.18s,.18s,0s,0s,0s,0s}
/* timeline rail reads newest -> oldest now; flip the gradient to match */
.tl-rail:before{background:linear-gradient(270deg,var(--flame),var(--lime) 52%,var(--electric))}
@media(max-width:1040px){
  .sites{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:700px){
  .sites{grid-template-columns:1fr;gap:16px;padding:16px}
  .site{padding:0}
  .site>div{display:flex;flex-direction:column}
  .site-category{margin:16px 18px 0}
  .site-meta{display:grid;grid-template-columns:1fr auto;gap:4px 12px}
  .site h3{margin:9px 18px 0}
  .site:first-child{display:flex;flex-direction:column}
  .site:first-child>div{display:flex;flex-direction:column;flex:1}
  .site:first-child .site-shot{aspect-ratio:16/9;min-height:0;height:auto;border-right:0;border-bottom:1px solid rgba(23,19,16,.08)}
  .site:first-child .site-category{margin:20px 20px 0}
  .site:first-child h3{margin:10px 20px 0;font-size:26px}
  .site:first-child p{margin:10px 20px 0;font-size:13px}
  .site:first-child .site-meta{margin:16px 20px 0}
  .site:first-child .site-link{margin:18px 20px 20px;align-self:stretch}
}
@media(prefers-reduced-motion:reduce){
  html.js .site{opacity:1;transform:none}
  .site:hover{translate:none}
  .site:hover .site-shot img{transform:none}
}
"""
rep('</style>', css_v5 + '</style>')

# ---------------- 7. self-checks ---------------------------------------------
checks = []
def ck(name, cond): checks.append((name, bool(cond)))

ck('cards live == 31', html.count('data-status="live"') == 31)
ck('article.site == 31', html.count('<article class="site" data-status="live">') == 31)
ck('visit links == 31', html.count('target="_blank" rel="noopener noreferrer">访问项目 ↗</a>') == 31)
ck('img refs == 31', len(re.findall(r'src="assets/projects/project-\d{2}\.webp"', html)) == 31)

desc = re.findall(r'<article class="site" data-status="live">.*?</article>', html, re.S)
keys = [card_key(c) for c in desc]
ck('order descending', keys == sorted(keys, reverse=True))
ck('top card spotlight', '<h3>The Sinking City 2 Field Guide</h3>' in desc[0])
ck('bottom card oldest', '<h3>AIStoryNest</h3>' in desc[-1])
ck(f'NEW badges == {new_count}', html.count('<span class="site-new">NEW</span>') == new_count)
ck('LATEST badge == 1', html.count('<span class="site-latest">★ 最新上线</span>') == 1)
ck('NEW+LATEST in top-9 only', all(('<span class="site-new">' in c or '<span class="site-latest">' in c) for c in desc[:9]) and not any('<span class="site-new">' in c for c in desc[9:]))

ck('timeline newest first', '<div class="tl-item latest"><div class="tl-date">2026-08-20</div>' in html)
ck('tl latest spans flipped', '<span>The Sinking City 2 Field Guide</span><span>Chinamaxxing Online</span>' in html)
ck('tl oldest last', html.rstrip().count('<div class="tl-date">2026-07-12</div>') == 1)
ck('tl latest marker == 1', html.count('tl-item latest') == 1)

ck('motion observes sites', "querySelectorAll('.reveal,.site')" in html)
ck('subhead hint', 'Every release leaves a trail · 最新在前' in html)
ck('grid css', '.sites{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))' in html)
ck('spotlight css', '.site:first-child{grid-column:1/-1;display:grid' in html)
ck('reveal css', 'html.js .site{opacity:0;transform:translateY(30px)}' in html)
ck('reduced-motion guard', 'html.js .site{opacity:1;transform:none}' in html)

# untouched contracts
ck('main script kept', "filters.forEach(button=>button.addEventListener('click'" in html)
ck('button text clean', '全部</button>' in html and 'AI 产品</button>' in html)
ck('data-count chips == 5', html.count('data-count="') == 5)
ck('ledger chip', '<span class="ledger-count">31</span>' in html)
ck('visibleCount kept', 'id="visibleCount" aria-live="polite">ALL RELEASES' in html)
ck('timeline title kept', '40 天，31 次真实上线。' in html)
ck('changelog kept newest-first', '[2026-08-20]</span><span class="log-ok">SHIP</span><span class="log-n">The Sinking City 2 Field Guide</span>' in html)
ck('no base64 imgs', 'data:image/webp;base64' not in html)
ck('plausible kept', 'plausible.shipsolo.io/js/script.js' in html)
ck('h3 wbr kept', '<h3>HowManySleeps<wbr>Until</h3>' in html)
wf = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
ck('workflow allowlist untouched', 'install -m 0644 index.html _site/index.html' in wf)

failed = [n for n, c in checks if not c]
if failed:
    print("SELF-CHECK FAILURES:", failed)
    sys.exit(1)
print(f"[3] self-checks: {len(checks)}/{len(checks)} OK")

(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"[4] written: {orig_len} -> {len(html)} chars (+{len(html)-orig_len})")
