#!/usr/bin/env python3
"""Variant A: 出版誌 GAZETTE — editorial print ledger."""
P = [
 ("OxAlpha","tool","2026-08-22","32","https://oxalpha.site/"),
 ("The Sinking City 2 Field Guide","game","2026-08-20","31","https://thesinkingcity2.top/"),
 ("Chinamaxxing Online","creative","2026-08-20","30","https://chinamaxxing.site/"),
 ("HLLV Field Manual","game","2026-08-18","29","https://hellletloosevietnam.blog/"),
 ("牛来","creative","2026-08-17","28","https://niulai.blog/"),
 ("CraveLoop","creative","2026-08-16","27","https://foodnevercomes.online/"),
 ("MatchaFilter","tool","2026-08-16","26","https://matchafilter.cc/"),
 ("burnt for you","creative","2026-08-16","25","https://burncd.xyz/"),
 ("Polski Piłkarz Simulator","game","2026-08-16","24","https://polskipilkarzsymulator.online/"),
 ("DSH Field Guide","tool","2026-08-15","23","https://deepseekharness.site/"),
 ("Remove Matcha Filter","tool","2026-08-12","22","https://remove-matcha-filter.com/"),
 ("RSP Editor","ai","2026-08-09","21","https://rspeditor.app/"),
 ("AI Scanner","ai","2026-08-09","20","https://aiscanner.run/"),
 ("Merge a Nuke! Guide","game","2026-08-08","19","https://mergeanuke.space/"),
 ("Shift at Midnight Guide","game","2026-08-05","18","https://shiftatmidnight.blog/"),
 ("竹知了","tool","2026-08-04","17","https://zhuzhiliao.buzz/"),
 ("Cash Flow Lifestyle","creative","2026-08-03","16","https://cashflow.lifestyle/"),
 ("HowManySleepsUntil","tool","2026-07-31","15","https://howmanysleepsuntil.rest/"),
 ("IsItDown","tool","2026-07-31","14","https://isitdown.click/"),
 ("CopyPlaintext","tool","2026-07-31","13","https://copyplaintext.com/"),
 ("DragonSword Wiki","game","2026-07-29","12","https://dragonswordawakening.fun/"),
 ("SpiritVale Wiki","game","2026-07-28","11","https://spiritvale.blog/"),
 ("Rot Check","creative","2026-07-26","10","https://rotcheck.cyou/"),
 ("Chinese Coins Atlas","creative","2026-07-26","09","https://chinesecashcoins.wiki/"),
 ("TaskbarHeroWiki","game","2026-07-26","08","https://taskbarherowiki.best/"),
 ("All Wishes Come True","creative","2026-07-25","07","https://allwishescometrue.site/"),
 ("llmstxt","tool","2026-07-18","06","https://llmstxt.best/"),
 ("CodexSkin.space","tool","2026-07-17","05","https://codexskin.space/"),
 ("PalworldMap","game","2026-07-14","04","https://palworldmap.best/"),
 ("FalloutDay","game","2026-07-12","03","https://falloutday.online/"),
 ("Build a Hooper","game","2026-07-12","02","https://buildahooper.best/"),
 ("AIStoryNest","ai","2026-07-12","01","https://aistorynest.mom/"),
]
CAT = {"game":"游戏","tool":"工具","creative":"创意","ai":"AI"}

CSS = """
:root{--paper:#f5f0e4;--paper2:#efe8d6;--ink:#191510;--accent:#c8401a;--hair:rgba(25,21,16,.18);--dim:#6f6858;
--serif:Georgia,"Times New Roman","Songti SC","STSong","SimSun",serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:var(--serif);-webkit-font-smoothing:antialiased;
background-image:radial-gradient(rgba(25,21,16,.028) 1px,transparent 1px);background-size:5px 5px}
a{color:inherit;text-decoration:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 26px}
/* masthead */
.masthead{padding-top:30px}
.mast-top{display:flex;justify-content:space-between;gap:12px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);padding-bottom:14px;border-bottom:1px solid var(--ink)}
.mast-title{text-align:center;font-size:clamp(46px,8.4vw,96px);font-weight:700;letter-spacing:.04em;padding:20px 0 4px;line-height:1.05}
.mast-title em{font-style:normal;color:var(--accent)}
.mast-sub{text-align:center;font-size:13px;letter-spacing:.42em;color:var(--dim);padding-bottom:16px}
.rule-double{border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);height:6px}
/* front page */
.front{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;padding:40px 0 44px;align-items:start}
.front h2{font-size:clamp(30px,4vw,46px);line-height:1.28;font-weight:700;margin-bottom:22px}
.front h2 span{border-bottom:4px solid var(--accent)}
.front p{font-size:16.5px;line-height:1.9;color:#3c362c;max-width:52ch}
.stats{display:flex;gap:0;margin-top:30px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.stats div{flex:1;padding:14px 6px;text-align:center}
.stats div+div{border-left:1px solid var(--hair)}
.stats b{display:block;font-size:34px;font-weight:700;font-family:var(--serif)}
.stats small{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.feature{border:1px solid var(--ink);background:var(--paper)}
.feature figcaption{padding:14px 16px 16px;border-top:1px solid var(--ink)}
.feature .kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;color:var(--accent);text-transform:uppercase;margin-bottom:6px}
.feature h3{font-size:21px;font-weight:700;margin-bottom:4px}
.feature small{font-family:var(--mono);font-size:11px;color:var(--dim)}
.feature img{width:100%;display:block;aspect-ratio:16/10;object-fit:cover;filter:saturate(.92)}
/* section tabs */
.tabs-bar{position:sticky;top:0;z-index:9;background:var(--paper);border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.tabs{display:flex;gap:26px;padding:12px 0;overflow-x:auto}
.tab{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;background:none;border:none;cursor:pointer;color:var(--dim);padding:2px 0;border-bottom:2px solid transparent;white-space:nowrap}
.tab.active{color:var(--ink);border-color:var(--accent)}
.tab sup{color:var(--accent);margin-left:3px}
/* ledger rows */
.row{display:grid;grid-template-columns:64px 168px 1fr 86px 104px;gap:20px;align-items:center;padding:16px 8px;border-bottom:1px solid var(--hair);cursor:pointer;transition:background .18s,color .18s}
.row .no{font-family:var(--serif);font-size:22px;font-weight:700;color:var(--dim);font-style:italic}
.row img{width:168px;height:100px;object-fit:cover;border:1px solid var(--ink);filter:saturate(.92);transition:filter .18s}
.row h3{font-size:19px;font-weight:700;line-height:1.3;margin-bottom:3px}
.row .meta{font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--dim)}
.row .cat{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--ink);padding:4px 0;text-align:center}
.row .date{font-family:var(--mono);font-size:12px;text-align:right;color:var(--dim)}
.row:hover{background:var(--ink);color:var(--paper)}
.row:hover .no{color:var(--accent)}
.row:hover .meta,.row:hover .date{color:rgba(245,240,228,.62)}
.row:hover .cat{border-color:rgba(245,240,228,.5)}
.row:hover img{filter:saturate(1.05)}
.row.off{display:none}
/* footer */
.colophon{margin-top:56px;border-top:3px double var(--ink);padding:22px 0 40px;display:flex;justify-content:space-between;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
@media(max-width:860px){
.front{grid-template-columns:1fr}
.row{grid-template-columns:44px 1fr 90px;grid-template-areas:"no title date" "no img cat";row-gap:10px}
.row .no{grid-area:no;font-size:17px}
.row .tt{grid-area:title}
.row img{grid-area:img;width:100%;height:88px}
.row .cat{grid-area:cat}
.row .date{grid-area:date}
}
"""

JS = """
const tabs=[...document.querySelectorAll('.tab')];
const rows=[...document.querySelectorAll('.row')];
tabs.forEach(t=>t.addEventListener('click',()=>{
 tabs.forEach(x=>x.classList.toggle('active',x===t));
 const f=t.dataset.f;
 rows.forEach(r=>r.classList.toggle('off',f!=='all'&&r.dataset.cat!==f));
}));
"""

rows_html = []
for name, cat, date, num, url in P[1:]:  # front page takes #32
    rows_html.append(
        f'<a class="row" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">'
        f'<span class="no">No.{num}</span>'
        f'<img src="../../assets/projects/project-{num}.webp" alt="{name}" loading="lazy">'
        f'<span class="tt"><h3>{name}</h3><span class="meta">{CAT[cat]} · 已上线 · 点击访问 ↗</span></span>'
        f'<span class="cat">{CAT[cat]}</span>'
        f'<span class="date">{date}</span></a>'
    )

html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>出版誌 · 王子凡的 32 次上线</title><style>__CSS__</style></head>
<body>
<div class="wrap">
  <header class="masthead">
    <div class="mast-top"><span>第 32 期 · 独立出版</span><span>WANG ZIFAN · ONE PERSON PRESS</span><span>2026 年 8 月 · 北京</span></div>
    <div class="mast-title">出版<em>誌</em></div>
    <div class="mast-sub">一个人 · 四十二天 · 三十二次真实上线</div>
    <div class="rule-double"></div>
  </header>

  <section class="front">
    <div>
      <h2>先把想法做出来，<br><span>再让世界给答案。</span></h2>
      <p>我是王子凡。不等完美时机，不写商业计划书，直接把产品上线，让真实用户投票。每一期出版誌收录一次完整发布——域名、代码、流量，全部可查证。</p>
      <div class="stats">
        <div><b>32</b><small>已上线产品</small></div>
        <div><b>42</b><small>天 · 连续发布</small></div>
        <div><b>1.3</b><small>天 / 次 · 节奏</small></div>
      </div>
    </div>
    <figure class="feature">
      <img src="../../assets/projects/project-32.webp" alt="OxAlpha">
      <figcaption>
        <div class="kicker">本期头条 · No.32 · 2026-08-22</div>
        <h3>OxAlpha</h3>
        <small>oxalpha.site · 工具 · 最新一期</small>
      </figcaption>
    </figure>
  </section>

  <div class="tabs-bar"><div class="tabs">
    <button class="tab active" data-f="all">全部目录<sup>32</sup></button>
    <button class="tab" data-f="game">游戏<sup>11</sup></button>
    <button class="tab" data-f="tool">工具<sup>10</sup></button>
    <button class="tab" data-f="creative">创意<sup>8</sup></button>
    <button class="tab" data-f="ai">AI<sup>3</sup></button>
  </div></div>

  <section>
__ROWS__
  </section>

  <footer class="colophon"><span>王子凡 · 独立出版人</span><span>不设完美时机，只设上线日期</span><span>WZF / 2026</span></footer>
</div>
<script>__JS__</script>
</body></html>"""

html = html.replace("__CSS__", CSS).replace("__ROWS__", "\n".join(rows_html)).replace("__JS__", JS)
import os
os.makedirs("001-gazette-editorial", exist_ok=True)
open("001-gazette-editorial/index.html", "w", encoding="utf-8").write(html)
print("A written:", len(html), "chars")
