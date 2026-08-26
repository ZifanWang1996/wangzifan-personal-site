#!/usr/bin/env python3
"""Variant B: 暗房冲印室 DARKROOM — photographic index cards, lightbox reveal."""
import json, os

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
CAT = {"game":"GAME","tool":"TOOL","creative":"CREATIVE","ai":"AI"}

CSS = """
:root{--bg:#12100c;--bg2:#1a1712;--fg:#ece5d3;--dim:#8f8776;--edge:#2e2a20;--red:#ff4b1f;--tape:rgba(236,229,211,.07);
--sans:"Helvetica Neue",Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--fg);font-family:var(--sans);-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.05;
background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><filter id="n"><feTurbulence baseFrequency="0.9" numOctaves="2"/></filter><rect width="120" height="120" filter="url(%23n)" opacity="0.6"/></svg>')}
a{color:inherit;text-decoration:none}
.wrap{max-width:1220px;margin:0 auto;padding:0 26px}
/* header */
header{padding:38px 0 10px;display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap}
.brand{font-family:var(--mono);font-size:13px;letter-spacing:.18em;color:var(--dim)}
.brand b{color:var(--fg)}
h1{font-size:clamp(34px,5.4vw,62px);font-weight:800;line-height:1.06;letter-spacing:-.015em;max-width:16ch;padding:18px 0 12px}
h1 em{font-style:normal;color:var(--red)}
.lede{color:var(--dim);font-size:15px;line-height:1.75;max-width:58ch}
.lede b{color:var(--fg);font-weight:600}
.counter{font-family:var(--mono);font-size:12px;letter-spacing:.12em;color:var(--dim);margin-top:18px}
.counter b{color:var(--red);font-size:22px;letter-spacing:0}
/* contact sheet */
.sheet{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;margin:44px 0 70px}
.cell{position:relative;background:var(--bg2);border:1px solid var(--edge);padding:8px;cursor:pointer;
transition:transform .25s cubic-bezier(.2,.9,.3,1.3),border-color .25s,box-shadow .25s}
.cell img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;filter:grayscale(.25) contrast(1.06);transition:filter .25s}
.cell .cap{display:flex;justify-content:space-between;gap:8px;font-family:var(--mono);font-size:10.5px;color:var(--dim);padding-top:7px;letter-spacing:.04em}
.cell .cap b{color:var(--fg);font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cell .frame-no{position:absolute;top:2px;right:10px;font-family:var(--mono);font-size:10px;color:rgba(236,229,211,.4)}
.cell:hover{transform:translateY(-5px) rotate(-.5deg);border-color:var(--red);box-shadow:0 14px 30px rgba(0,0,0,.5)}
.cell:hover img{filter:grayscale(0) contrast(1.02)}
.cell.off{display:none}
/* lightbox */
.lb{position:fixed;inset:0;z-index:50;background:rgba(10,9,7,.88);backdrop-filter:blur(6px);display:none;align-items:center;justify-content:center;padding:26px}
.lb.open{display:flex}
.lb-card{width:min(880px,100%);background:var(--bg2);border:1px solid var(--edge);box-shadow:0 30px 80px rgba(0,0,0,.6)}
.lb-card img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.lb-body{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:18px 20px;flex-wrap:wrap}
.lb-body h3{font-size:22px;font-weight:750;letter-spacing:-.01em}
.lb-meta{font-family:var(--mono);font-size:11.5px;color:var(--dim);margin-top:4px;letter-spacing:.06em}
.lb-actions{display:flex;gap:10px}
.btn{font-family:var(--mono);font-size:12px;letter-spacing:.1em;padding:11px 18px;border:1px solid var(--edge);color:var(--fg);background:none;cursor:pointer;transition:.2s}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn.hot{background:var(--red);border-color:var(--red);color:#140c08;font-weight:700}
.btn.hot:hover{filter:brightness(1.12);color:#140c08}
.lb-close{position:absolute;top:22px;right:26px;font-family:var(--mono);color:var(--dim);background:none;border:none;font-size:13px;cursor:pointer;letter-spacing:.1em}
.lb-close:hover{color:var(--fg)}
/* filters */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-top:26px}
.f{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;padding:8px 14px;border:1px solid var(--edge);background:none;color:var(--dim);cursor:pointer;transition:.2s}
.f:hover{color:var(--fg);border-color:var(--dim)}
.f.on{color:#140c08;background:var(--fg);border-color:var(--fg)}
/* footer */
footer{border-top:1px solid var(--edge);margin-top:10px;padding:24px 0 46px;display:flex;justify-content:space-between;gap:14px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--dim);flex-wrap:wrap}
@media(max-width:980px){.sheet{grid-template-columns:repeat(3,1fr)}}
@media(max-width:620px){.sheet{grid-template-columns:repeat(2,1fr)} .lb-body{padding:14px}}
"""

JS = r"""
const DATA=__DATA__;
const sheet=document.getElementById('sheet');
const lb=document.getElementById('lb');
const cells=[...document.querySelectorAll('.cell')];
let cur=-1;
cells.forEach((c,i)=>{
 c.addEventListener('click',()=>open(i));
 c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(i);}});
});
function render(i){
 cur=i;
 const d=DATA[i];
 document.getElementById('lbImg').src='../../assets/projects/project-'+d.n+'.webp';
 document.getElementById('lbTitle').textContent=d.t;
 document.getElementById('lbMeta').textContent=d.c.toUpperCase()+' · '+d.d+' · FRAME '+d.n+'/32';
 document.getElementById('lbVisit').href=d.u;
}
function open(i){render(i);lb.classList.add('open');document.body.style.overflow='hidden';}
function close(){lb.classList.remove('open');document.body.style.overflow='';cur=-1;}
document.getElementById('lbClose').addEventListener('click',close);
document.getElementById('lbNext').addEventListener('click',()=>{if(cur>=0)render((cur+1)%DATA.length);});
lb.addEventListener('click',e=>{if(e.target===lb)close()});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape')close();
 if(e.key==='ArrowRight'&&cur>=0)render((cur+1)%DATA.length);
 if(e.key==='ArrowLeft'&&cur>=0)render((cur-1+DATA.length)%DATA.length);
});
document.querySelectorAll('.f').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('.f').forEach(x=>x.classList.toggle('on',x===b));
 const f=b.dataset.f;
 cells.forEach((c,i)=>c.classList.toggle('off',f!=='all'&&DATA[i].c!==f));
}));
"""

DATA = [{"t":n,"c":c,"d":d,"n":num,"u":u} for n,c,d,num,u in P]

cells_html = []
for i, (name, cat, date, num, url) in enumerate(P):
    cells_html.append(
        f'<div class="cell" role="button" tabindex="0" aria-label="{name}">'
        f'<span class="frame-no">{num}</span>'
        f'<img src="../../assets/projects/project-{num}.webp" alt="{name}" loading="lazy">'
        f'<div class="cap"><b>{name}</b><span>{CAT[cat]}</span></div></div>'
    )

html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>暗房 · 王子凡的 32 次上线</title><style>__CSS__</style></head>
<body>
<div class="wrap">
<header><span class="brand"><b>WZF</b> / DARKROOM INDEX</span><span class="brand">2026.07.12 — 08.22 · 北京</span></header>
<h1>四十二天，我在暗房里<em>冲印了三十二张</em>。</h1>
<p class="lede">我是王子凡。每张底片是一个真实上线的产品：域名是真的，流量是真的，用户也是真的。点击任意一格，<b>放大查看原片</b>。</p>
<div class="filters">
<button class="f on" data-f="all">ALL · 32</button>
<button class="f" data-f="game">GAME · 11</button>
<button class="f" data-f="tool">TOOL · 10</button>
<button class="f" data-f="creative">CREATIVE · 8</button>
<button class="f" data-f="ai">AI · 3</button>
</div>
<div class="counter">CONTACT SHEET · <b>32</b> FRAMES · 1.3 天 / 张</div>
<div class="sheet" id="sheet">
__CELLS__
</div>
<footer><span>WANG ZIFAN — ONE-PERSON STUDIO</span><span>不设完美时机，只设上线日期</span><span>© 2026</span></footer>
</div>

<div class="lb" id="lb" role="dialog" aria-modal="true">
<button class="lb-close" id="lbClose">ESC / 关闭 ✕</button>
<div class="lb-card">
<img id="lbImg" alt="">
<div class="lb-body">
<div><h3 id="lbTitle"></h3><div class="lb-meta" id="lbMeta"></div></div>
<div class="lb-actions"><a class="btn hot" id="lbVisit" target="_blank" rel="noopener">访问线上 ↗</a><button class="btn" id="lbNext">下一张 →</button></div>
</div>
</div>
</div>
<script>__JS__</script>
</body></html>"""

html = html.replace("__CSS__", CSS).replace("__CELLS__", "\n".join(cells_html)).replace("__JS__", JS).replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
os.makedirs("002-darkroom-contact-sheet", exist_ok=True)
open("002-darkroom-contact-sheet/index.html", "w", encoding="utf-8").write(html)
print("B written:", len(html), "chars")
