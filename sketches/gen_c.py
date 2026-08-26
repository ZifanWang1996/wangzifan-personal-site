#!/usr/bin/env python3
"""Variant C: 唱片行 CRATE DIGGING — sleeves in record-store bins, pull-out reveal."""
import os

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
CAT_CN = {"game":"游戏区","tool":"工具区","creative":"创意区","ai":"AI 区"}
CAT_TAG = {"game":"GAME","tool":"TOOL","creative":"CREA","ai":"A.I."}
ORDER = ["game","tool","creative","ai"]

CSS = """
:root{--wall:#efe6d2;--wall2:#e6dabf;--wood:#7a5636;--wood2:#5d4028;--card:#fbf6ea;--ink:#241c12;--stamp:#b23a1a;--dim:#7d715a;
--sans:"Futura","Trebuchet MS","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--wall);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
/* storefront sign */
.sign{padding:34px 0 8px;text-align:center}
.sign .neon{display:inline-block;font-size:clamp(38px,6vw,68px);font-weight:800;letter-spacing:.12em;color:var(--ink);
border:3px solid var(--ink);padding:10px 34px;background:var(--card);box-shadow:5px 5px 0 var(--ink);transform:rotate(-.6deg)}
.sign .neon b{color:var(--stamp)}
.sign .sub{font-family:var(--mono);font-size:12px;letter-spacing:.34em;color:var(--dim);margin-top:16px}
.sign .intro{max-width:56ch;margin:20px auto 0;font-size:15.5px;line-height:1.85;color:#4c4232}
.sign .intro b{color:var(--ink)}
/* crate shelf */
.aisle{margin-top:46px}
.aisle-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;border-bottom:3px solid var(--ink);padding-bottom:8px;margin-bottom:20px}
.aisle-head h2{font-size:24px;font-weight:800;letter-spacing:.06em}
.aisle-head small{font-family:var(--mono);font-size:11px;letter-spacing:.18em;color:var(--dim)}
.crate{display:grid;grid-template-columns:repeat(auto-fill,minmax(218px,1fr));gap:18px;padding-bottom:36px}
.sleeve{position:relative;background:var(--card);border:2px solid var(--ink);cursor:pointer;
transition:transform .22s cubic-bezier(.2,.9,.3,1.25),box-shadow .22s;transform:rotate(var(--tilt,0deg))}
.sleeve .art{position:relative;border-bottom:2px solid var(--ink);overflow:hidden}
.sleeve img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.sleeve .sticker{position:absolute;top:8px;left:-6px;background:var(--stamp);color:#fff8ee;font-family:var(--mono);font-size:10px;letter-spacing:.14em;padding:4px 10px;transform:rotate(-3deg);box-shadow:2px 2px 0 rgba(36,28,18,.35)}
.sleeve .label{padding:11px 13px 13px;display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.sleeve .label b{font-size:15.5px;font-weight:750;letter-spacing:.01em;line-height:1.3}
.sleeve .label span{font-family:var(--mono);font-size:10.5px;color:var(--dim);white-space:nowrap}
.sleeve:hover{transform:rotate(0deg) translateY(-8px);box-shadow:7px 10px 0 rgba(36,28,18,.22);z-index:2}
/* pull-out card (flip liner notes) */
.flip{position:fixed;inset:0;z-index:60;background:rgba(36,28,18,.45);display:none;align-items:center;justify-content:center;padding:24px}
.flip.open{display:flex}
.flip-card{width:min(760px,100%);background:var(--card);border:3px solid var(--ink);box-shadow:10px 12px 0 rgba(36,28,18,.4);transform:rotate(-.8deg)}
.flip-card img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-bottom:3px solid var(--ink)}
.flip-body{padding:20px 24px 24px}
.flip-top{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}
.flip-body h3{font-size:26px;font-weight:800}
.flip-stamp{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--stamp);border:2px solid var(--stamp);padding:5px 10px;transform:rotate(2deg)}
.flip-notes{margin:14px 0 18px;font-size:15px;line-height:1.8;color:#4c4232}
.flip-notes b{color:var(--ink)}
.flip-meta{display:flex;gap:0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);margin-bottom:18px}
.flip-meta div{flex:1;text-align:center;padding:10px 4px}
.flip-meta div+div{border-left:1px solid rgba(36,28,18,.25)}
.flip-meta b{display:block;font-size:19px;font-weight:800}
.flip-meta small{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--dim)}
.flip-actions{display:flex;gap:12px;flex-wrap:wrap}
.btn{font-family:var(--mono);font-size:12px;letter-spacing:.12em;padding:12px 20px;border:2px solid var(--ink);background:none;color:var(--ink);cursor:pointer;box-shadow:3px 3px 0 var(--ink);transition:.15s}
.btn:hover{transform:translate(-1px,-1px);box-shadow:5px 5px 0 var(--ink)}
.btn.hot{background:var(--stamp);border-color:var(--stamp);color:#fff8ee;box-shadow:3px 3px 0 var(--ink)}
.flip-close{margin-left:auto}
/* footer */
footer{border-top:3px solid var(--ink);margin-top:20px;padding:22px 0 44px;display:flex;justify-content:space-between;gap:12px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--dim);flex-wrap:wrap}
@media(max-width:640px){.flip-meta small{font-size:9px}.flip-body h3{font-size:21px}}
"""

JS = r"""
const sleeves=[...document.querySelectorAll('.sleeve')];
const flip=document.getElementById('flip');
sleeves.forEach(s=>s.addEventListener('click',()=>{
 document.getElementById('fImg').src=s.querySelector('img').src;
 document.getElementById('fTitle').textContent=s.dataset.title;
 document.getElementById('fStamp').textContent=s.dataset.tag+' · NO.'+s.dataset.no;
 document.getElementById('fDate').textContent=s.dataset.date;
 document.getElementById('fCat').textContent=s.dataset.cat;
 document.getElementById('fVisit').href=s.dataset.url;
 document.getElementById('fNote').innerHTML='这张「'+s.dataset.title+'」于 <b>'+s.dataset.date+'</b> 上架。真货：线上可访问，随时可听。翻到 B 面，直接访问官网。';
 flip.classList.add('open');document.body.style.overflow='hidden';
}));
function close(){flip.classList.remove('open');document.body.style.overflow=''}
document.getElementById('fClose').addEventListener('click',close);
flip.addEventListener('click',e=>{if(e.target===flip)close()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
"""

sections = []
for cat in ORDER:
    items = [p for p in P if p[1] == cat]
    sleeves_html = []
    for name, _, date, num, url in items:
        tilt = ((int(num) * 7) % 5) - 2  # -2..2 deg deterministic tilt
        sleeves_html.append(
            f'<div class="sleeve" style="--tilt:{tilt}deg" role="button" tabindex="0" data-title="{name}" data-date="{date}" '
            f'data-cat="{CAT_CN[cat]}" data-tag="{CAT_TAG[cat]}" data-no="{num}" data-url="{url}" aria-label="{name}">'
            f'<div class="art"><img src="../../assets/projects/project-{num}.webp" alt="{name}" loading="lazy">'
            f'<span class="sticker">NO.{num}</span></div>'
            f'<div class="label"><b>{name}</b><span>{date[5:]}</span></div></div>'
        )
    sections.append(
        f'<section class="aisle"><div class="aisle-head"><h2>{CAT_CN[cat]}</h2>'
        f'<small>BIN {CAT_TAG[cat]} · {len(items)} SLEEVES · 按上架时间排</small></div>'
        f'<div class="crate">{"".join(sleeves_html)}</div></section>'
    )

html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>一人唱片行 · 王子凡的 32 张出品</title><style>__CSS__</style></head>
<body>
<div class="wrap">
<header class="sign">
<div class="neon">一人唱片行 <b>WZF</b> RECORDS</div>
<div class="sub">EST. 2026.07.12 · 42 天 · 32 张出品 · 全部在线</div>
<p class="intro">我是王子凡。这家店只卖一种东西：<b>真实上线的产品</b>。每张唱片都有现货——点开唱片套，翻到 B 面就能直接访问。不预购，不画饼。</p>
</header>
__SECTIONS__
<footer><span>WANG ZIFAN · ONE-PERSON RECORD SHOP</span><span>不设完美时机，只设上架日期</span><span>© 2026</span></footer>
</div>

<div class="flip" id="flip" role="dialog" aria-modal="true">
<div class="flip-card">
<img id="fImg" alt="">
<div class="flip-body">
<div class="flip-top"><h3 id="fTitle"></h3><span class="flip-stamp" id="fStamp"></span></div>
<p class="flip-notes" id="fNote"></p>
<div class="flip-meta">
<div><b id="fCat"></b><small>唱片分区</small></div>
<div><b id="fDate"></b><small>上架日期</small></div>
<div><b>LIVE</b><small>播放状态</small></div>
</div>
<div class="flip-actions"><a class="btn hot" id="fVisit" target="_blank" rel="noopener">▶ 现在播放（访问官网）</a><button class="btn flip-close" id="fClose">放回唱片架</button></div>
</div>
</div>
</div>
<script>__JS__</script>
</body></html>"""

html = html.replace("__CSS__", CSS).replace("__SECTIONS__", "\n".join(sections)).replace("__JS__", JS)
os.makedirs("003-record-shop-crate", exist_ok=True)
open("003-record-shop-crate/index.html", "w", encoding="utf-8").write(html)
print("C written:", len(html), "chars")
