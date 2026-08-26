#!/usr/bin/env python3
"""Variant D: DEPARTURE BOARD — 站点=单人航运公司的实时出发大屏。"""
from datetime import date
import os

TODAY = date(2026, 8, 23)
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

def dom(u): return u.replace("https://","").rstrip("/")

CSS = """
:root{--bg:#F5F1E6;--ink:#121212;--or:#FF4D00;--green:#0E7C3D;--amber:#F5B800;--dim:#6E6858;--line:rgba(18,18,18,.18);
--mono:ui-monospace,"SF Mono",Menlo,Consolas,"Courier New",monospace;
--sans:"Helvetica Neue",Helvetica,Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1160px;margin:0 auto;padding:0 28px}
/* strip */
.strip{background:var(--ink);color:#EDE9DA;font:600 10.5px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase}
.strip .wrap{display:flex;justify-content:space-between;gap:14px;padding-top:11px;padding-bottom:11px}
.strip b{color:var(--amber);font-weight:700}
/* hero */
.hero{padding:64px 0 46px;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:48px;align-items:center}
.eyebrow{font:700 11px var(--mono);letter-spacing:.26em;color:var(--or);text-transform:uppercase;margin-bottom:20px}
.eyebrow i{display:inline-block;width:8px;height:8px;background:var(--or);margin-right:10px;animation:blink 1.5s ease-in-out infinite}
h1{font-size:clamp(42px,6.4vw,84px);line-height:1.04;font-weight:900;letter-spacing:-.025em}
h1 em{font-style:normal;color:var(--or)}
.hero p{margin-top:22px;font-size:16px;line-height:1.95;color:#3E3A30;max-width:56ch}
.hero p strong{color:var(--ink)}
.counter{border:3px solid var(--ink);background:#fff;padding:26px 30px;box-shadow:10px 10px 0 var(--ink)}
.counter b{display:block;font:900 clamp(88px,10vw,132px)/.9 var(--mono);letter-spacing:-.04em}
.counter small{display:block;margin-top:10px;font:700 10.5px var(--mono);letter-spacing:.3em;color:var(--dim);text-transform:uppercase}
.counter .next{margin-top:16px;padding-top:14px;border-top:2px solid var(--ink);font:700 12px var(--mono);letter-spacing:.14em;display:flex;justify-content:space-between}
.counter .next b{font-size:12px;color:var(--or);display:inline}
/* board */
.board-head{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin:8px 0 18px}
.board-head h2{font-size:clamp(26px,3vw,38px);font-weight:900;letter-spacing:-.02em}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{border:2px solid var(--ink);background:transparent;color:var(--ink);font:700 11px var(--mono);letter-spacing:.1em;padding:8px 13px;cursor:pointer;border-radius:3px;transition:.18s}
.chip:hover{background:rgba(18,18,18,.08)}
.chip.on{background:var(--ink);color:var(--bg)}
.vis{font:600 10.5px var(--mono);letter-spacing:.14em;color:var(--dim);margin-left:6px}
.board{background:#101010;border:3px solid var(--ink);border-radius:6px;overflow:hidden}
.thead,.row{display:grid;grid-template-columns:72px 106px minmax(0,1.35fr) minmax(0,1.15fr) 76px 78px;grid-template-areas:"num date name dest gate st";gap:0 16px;align-items:center;padding:0 24px}
.thead{font:700 9.5px var(--mono);letter-spacing:.24em;color:#8B8778;text-transform:uppercase;padding-top:15px;padding-bottom:15px;border-bottom:1px solid rgba(245,241,230,.16)}
.row{font:500 13.5px/1.35 var(--mono);color:#EDE9DA;padding-top:14px;padding-bottom:14px;border-bottom:1px solid rgba(245,241,230,.08);transition:background .18s}
.row:last-child{border-bottom:0}
.row:hover{background:rgba(245,241,230,.07)}
.c-num{grid-area:num;color:#8B8778;font-size:12px}
.c-date{grid-area:date;color:#B9B4A2;font-size:12px}
.c-name{grid-area:name;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.c-dest{grid-area:dest;color:#9A9583;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.c-dest i{font-style:normal;color:var(--or);opacity:0;margin-left:6px;transition:opacity .18s}
.row:hover .c-dest i{opacity:1}
.c-gate{grid-area:gate;font-size:11px;color:#B9B4A2;border:1px solid rgba(245,241,230,.22);border-radius:3px;padding:3px 0;text-align:center}
.c-st{grid-area:st;text-align:right}
.st{display:inline-block;font:700 9.5px/1 var(--mono);letter-spacing:.14em;color:#7BE3A0;border:1px solid rgba(123,227,160,.45);padding:5px 7px;border-radius:3px}
.row.latest{background:rgba(255,77,0,.13);box-shadow:inset 4px 0 0 var(--or)}
.row.latest .c-num:after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--amber);margin-left:7px;vertical-align:1px;animation:blink 1.4s ease-in-out infinite}
.row.latest .c-name{color:var(--amber)}
.st-blink{animation:blink 1.4s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.35}}
/* stats band */
.stats{background:var(--ink);color:var(--bg);margin-top:64px}
.stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);padding-top:34px;padding-bottom:34px}
.stats div{padding:0 22px;border-left:1px solid rgba(245,241,230,.18)}
.stats div:first-child{border-left:0}
.stats b{display:block;font:900 clamp(34px,3.6vw,52px)/1 var(--mono)}
.stats b em{font-style:normal;color:var(--amber)}
.stats small{display:block;margin-top:9px;font:600 10px var(--mono);letter-spacing:.22em;color:#9A9583;text-transform:uppercase}
/* system subway */
.system{padding:78px 0 66px}
.kicker{font:700 11px var(--mono);letter-spacing:.26em;color:var(--or);text-transform:uppercase;margin-bottom:16px}
.system h2{font-size:clamp(28px,3.6vw,44px);font-weight:900;letter-spacing:-.02em;max-width:22ch;line-height:1.2}
.line-map{position:relative;margin-top:54px;display:grid;grid-template-columns:repeat(4,1fr)}
.line-map:before{content:"";position:absolute;left:4%;right:4%;top:9px;height:4px;background:var(--ink)}
.station{position:relative;padding-top:38px;text-align:left}
.station:before{content:"";position:absolute;top:0;left:0;width:22px;height:22px;border-radius:50%;background:var(--bg);border:4px solid var(--ink)}
.station.hot:before{background:var(--or);border-color:var(--or)}
.station b{display:block;font-size:20px;font-weight:900;letter-spacing:-.01em}
.station small{display:block;margin-top:7px;font:600 10px var(--mono);letter-spacing:.18em;color:var(--dim);text-transform:uppercase}
.station p{margin-top:9px;font-size:12.5px;line-height:1.75;color:#55503F;max-width:24ch}
/* manifesto */
.quote{border-top:3px solid var(--ink);border-bottom:3px solid var(--ink);padding:58px 0;text-align:center}
.quote p{font-size:clamp(26px,4vw,48px);font-weight:900;letter-spacing:-.02em;line-height:1.3}
.quote p em{font-style:normal;color:var(--or)}
.quote small{display:block;margin-top:18px;font:600 10.5px var(--mono);letter-spacing:.3em;color:var(--dim)}
/* contact */
.contact{background:var(--ink);color:var(--bg);padding:74px 0 60px}
.contact h2{font-size:clamp(34px,5vw,64px);font-weight:900;letter-spacing:-.02em;line-height:1.15}
.contact h2 em{font-style:normal;color:var(--amber)}
.contact-grid{display:flex;justify-content:space-between;align-items:flex-end;gap:34px;flex-wrap:wrap;margin-top:34px}
.wx{font:600 13px var(--mono);letter-spacing:.1em;color:#B9B4A2}
.wx b{display:block;font-size:24px;color:var(--bg);margin-top:7px;letter-spacing:.04em}
.copy{border:0;background:var(--or);color:#fff;font:700 13px var(--mono);letter-spacing:.12em;padding:16px 26px;border-radius:4px;cursor:pointer;transition:.18s}
.copy:hover{background:#ff6a26;transform:translate(-1px,-1px);box-shadow:4px 4px 0 rgba(245,241,230,.25)}
.fine{margin-top:44px;padding-top:18px;border-top:1px solid rgba(245,241,230,.16);display:flex;justify-content:space-between;gap:12px;font:500 10.5px var(--mono);letter-spacing:.14em;color:#8B8778}
@media(max-width:900px){
 .hero{grid-template-columns:1fr;gap:34px;padding-top:44px}
 .thead{display:none}
 .row{grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:"num name st" "date dest dest";gap:3px 12px;padding:12px 16px}
 .c-gate{display:none}
 .c-dest{font-size:12px}
 .stats .wrap{grid-template-columns:1fr 1fr;gap:22px 0}
 .stats div:nth-child(3){border-left:0}
 .line-map{grid-template-columns:1fr;gap:30px}
 .line-map:before{left:9px;right:auto;top:2%;bottom:2%;width:4px;height:auto}
 .station{padding-top:0;padding-left:44px}
 .station:before{top:-2px}
 .contact-grid{align-items:flex-start;flex-direction:column}
}
"""

rows = []
for i,(name,cat,dt,num,url) in enumerate(P):
    latest = " latest" if i==0 else ""
    st = '<span class="st">LIVE</span>'
    rows.append('<a class="row{lt}" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">'
        '<span class="c-num">№{num}</span><span class="c-date">{dt}</span>'
        '<span class="c-name">{name}</span><span class="c-dest">{dom}<i>↗</i></span>'
        '<span class="c-gate">{g}</span><span class="c-st">{st}</span></a>'.format(
        lt=latest,cat=cat,url=url,num=num,dt=dt,name=name,dom=dom(url),g=CAT[cat],st=st))

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>王子凡 — 出发大屏（方案 D）</title>
<style>__CSS__</style>
</head>
<body>
<div class="strip"><div class="wrap"><span>WZF LINES · 一人航运 · ONE-PERSON FREIGHT</span><span><b id="clock">BEIJING --:--:--</b> · 2026-08-23</span></div></div>
<section class="wrap hero">
  <div>
    <div class="eyebrow"><i></i>DEPARTURE BOARD / 出发大屏</div>
    <h1>42 天，32 班。<br>每一班都<em>真的起飞</em>。</h1>
    <p>我是<strong>王子凡</strong>，一个人的航运公司：判断是机票，构建是装配，上线是起飞。这里没有草稿和预告——<strong>只有已经出发的航班</strong>，每一班都有真实目的地。</p>
  </div>
  <div class="counter"><b>32</b><small>DEPARTURES SINCE 2026-07-12</small>
    <div class="next"><span>NEXT SHIP</span><b>TODAY</b></div>
  </div>
</section>
<section class="wrap" id="work">
  <div class="board-head">
    <h2>全部出发记录</h2>
    <div class="chips">
      <button class="chip on" data-f="all">全部 32</button>
      <button class="chip" data-f="ai">AI 3</button>
      <button class="chip" data-f="game">游戏 11</button>
      <button class="chip" data-f="tool">工具 10</button>
      <button class="chip" data-f="creative">创意 8</button>
      <span class="vis" id="vis">显示 32 / 32 班</span>
    </div>
  </div>
  <div class="board">
    <div class="thead"><span class="c-num">航班</span><span class="c-date">日期</span><span class="c-name">产品</span><span class="c-dest">目的地（真实域名）</span><span class="c-gate">类型</span><span class="c-st">状态</span></div>
    __ROWS__
  </div>
</section>
<section class="stats">
  <div class="wrap">
    <div><b>42<em>天</em></b><small>连续上线周期</small></div>
    <div><b>32<em>班</em></b><small>真实出发 · 0 取消</small></div>
    <div><b>1.3<em>天</em></b><small>平均发班间隔</small></div>
    <div><b>100<em>%</em></b><small>目的地可访问</small></div>
  </div>
</section>
<section class="wrap system" id="system">
  <div class="kicker">OPERATING ROUTINE / 运转规程</div>
  <h2>一个人怎么保持每天起飞：四条固定航线。</h2>
  <div class="line-map">
    <div class="station hot"><b>判断</b><small>STEP 01 · SIGNAL</small><p>不追所有机会，找到真实需求，选中值得立刻动手的那一个问题。</p></div>
    <div class="station"><b>构建</b><small>STEP 02 · BUILD</small><p>AI 放大单人产能，最短路径做出可用版本，不用筹备冒充进展。</p></div>
    <div class="station"><b>上线</b><small>STEP 03 · SHIP</small><p>产品上线才算回答。真实域名、真实用户、真实反馈。</p></div>
    <div class="station"><b>反馈</b><small>STEP 04 · LEARN</small><p>数据与用户反馈沉淀为下一次判断的燃料，循环复利。</p></div>
  </div>
</section>
<section class="quote">
  <div class="wrap"><p>不等完美天气。<em>起飞，就是天气。</em></p><small>WZF LINES · MANIFESTO 001</small></div>
</section>
<footer class="contact" id="contact">
  <div class="wrap">
    <h2>下一班，<em>一起发</em>。</h2>
    <div class="contact-grid">
      <div class="wx">WECHAT / DIRECT CONTACT<b>wang1227928718</b></div>
      <button class="copy" id="copyBtn">复制微信号</button>
    </div>
    <div class="fine"><span>© 2026 王子凡 ZF WANG · ONE PERSON · ALWAYS SHIPPING</span><span>备注「合作」+ 你的方向</span></div>
  </div>
</footer>
<script>
(function(){
  var chips=document.querySelectorAll('.chip');
  var rows=document.querySelectorAll('.row');
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.classList.remove('on')});
    c.classList.add('on');
    var f=c.getAttribute('data-f');var n=0;
    rows.forEach(function(r){
      var show=(f==='all'||r.getAttribute('data-cat')===f);
      r.style.display=show?'':'none';
      if(show)n++;
    });
    document.getElementById('vis').textContent='显示 '+n+' / 32 班';
  })});
  var btn=document.getElementById('copyBtn');
  function done(){btn.textContent='已复制 ✓';setTimeout(function(){btn.textContent='复制微信号'},1600)}
  function fallback(){var i=document.createElement('input');i.value='wang1227928718';document.body.appendChild(i);i.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(i);done()}
  btn.addEventListener('click',function(){
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText('wang1227928718').then(done,fallback)}else{fallback()}
  });
  var clock=document.getElementById('clock');
  function tick(){var d=new Date();var p=function(x){return String(x).padStart(2,'0')};clock.textContent='BEIJING '+p(d.getHours())+':'+p(d.getMinutes())+':'+p(d.getSeconds())}
  tick();setInterval(tick,1000);
})();
</script>
</body>
</html>
"""

out = os.path.join(os.path.dirname(__file__), "004-departure-board")
os.makedirs(out, exist_ok=True)
html = HTML.replace("__CSS__", CSS).replace("__ROWS__", "\n    ".join(rows))
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(
"""## Variant D: 出发大屏 DEPARTURE BOARD

### Design stance
站点不是档案馆，是单人航运公司的实时出发大屏——节奏（42 天 32 班）就是品牌本身。

### Key choices
- Layout: 深黑信息板嵌在米白纸面上，32 班以航班行呈现（№/日期/产品/目的地域名/类型/状态）
- Typography: 重型无衬线标题 + 等宽航班信息，交通标识语言
- Color: 纸白 + 墨黑 + 信号橙，LIVE 绿、最新班次琥珀高亮
- Interaction: 分类筛选、行悬停显示 ↗、实时时钟、最新班闪烁

### Trade-offs
- Strong at: 节奏感/公共感/能量感，一眼看懂"这个人一直在发货"
- Weak at: 信息板密集，叙事性弱于文档式

### Best for
想传达"速度与真实上线密度"的第一印象，面向关注执行力的访客/合作方。
""")
print("wrote", os.path.join(out, "index.html"), len(html), "bytes,", len(rows), "rows")
