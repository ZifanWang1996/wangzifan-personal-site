#!/usr/bin/env python3
"""Variant E: MANIFEST — 站点=一张货运提单，每个产品是一件已发出的货。"""
import os

P = [
 ("OxAlpha","tool","2026-08-22","32","https://oxalpha.site/","AI 模型证据站"),
 ("The Sinking City 2 Field Guide","game","2026-08-20","31","https://thesinkingcity2.top/","克苏鲁侦探攻略站"),
 ("Chinamaxxing Online","creative","2026-08-20","30","https://chinamaxxing.site/","多语文化指南"),
 ("HLLV Field Manual","game","2026-08-18","29","https://hellletloosevietnam.blog/","HLLV 越南战场手册"),
 ("牛来","creative","2026-08-17","28","https://niulai.blog/","牛来电影资料站"),
 ("CraveLoop","creative","2026-08-16","27","https://foodnevercomes.online/","全球美食点单模拟器"),
 ("MatchaFilter","tool","2026-08-16","26","https://matchafilter.cc/","照片抹茶滤镜校色"),
 ("burnt for you","creative","2026-08-16","25","https://burncd.xyz/","数字 mixtape 礼物站"),
 ("Polski Piłkarz Simulator","game","2026-08-16","24","https://polskipilkarzsymulator.online/","PPS 粉丝站"),
 ("DSH Field Guide","tool","2026-08-15","23","https://deepseekharness.site/","DeepSeek 评测站"),
 ("Remove Matcha Filter","tool","2026-08-12","22","https://remove-matcha-filter.com/","抹茶偏色修正"),
 ("RSP Editor","ai","2026-08-09","21","https://rspeditor.app/","RSP 编辑器"),
 ("AI Scanner","ai","2026-08-09","20","https://aiscanner.run/","AI 扫描器"),
 ("Merge a Nuke! Guide","game","2026-08-08","19","https://mergeanuke.space/","合成核弹攻略"),
 ("Shift at Midnight Guide","game","2026-08-05","18","https://shiftatmidnight.blog/","午夜轮班攻略"),
 ("竹知了","tool","2026-08-04","17","https://zhuzhiliao.buzz/","竹蝉玩具模拟器"),
 ("Cash Flow Lifestyle","creative","2026-08-03","16","https://cashflow.lifestyle/","现金流桌游"),
 ("HowManySleepsUntil","tool","2026-07-31","15","https://howmanysleepsuntil.rest/","还要睡几觉"),
 ("IsItDown","tool","2026-07-31","14","https://isitdown.click/","网站在线检测"),
 ("CopyPlaintext","tool","2026-07-31","13","https://copyplaintext.com/","纯文本复制"),
 ("DragonSword Wiki","game","2026-07-29","12","https://dragonswordawakening.fun/","龙剑维基"),
 ("SpiritVale Wiki","game","2026-07-28","11","https://spiritvale.blog/","灵谷维基"),
 ("Rot Check","creative","2026-07-26","10","https://rotcheck.cyou/","腐烂检测器"),
 ("Chinese Coins Atlas","creative","2026-07-26","09","https://chinesecashcoins.wiki/","古泉馆双语图鉴"),
 ("TaskbarHeroWiki","game","2026-07-26","08","https://taskbarherowiki.best/","任务栏英雄维基"),
 ("All Wishes Come True","creative","2026-07-25","07","https://allwishescometrue.site/","愿望成真"),
 ("llmstxt","tool","2026-07-18","06","https://llmstxt.best/","llms.txt 工具"),
 ("CodexSkin.space","tool","2026-07-17","05","https://codexskin.space/","Codex 皮肤站"),
 ("PalworldMap","game","2026-07-14","04","https://palworldmap.best/","帕鲁地图"),
 ("FalloutDay","game","2026-07-12","03","https://falloutday.online/","辐射日"),
 ("Build a Hooper","game","2026-07-12","02","https://buildahooper.best/","组装篮球架"),
 ("AIStoryNest","ai","2026-07-12","01","https://aistorynest.mom/","AI 故事巢"),
]
CAT = {"game":"游戏与内容","tool":"实用工具","creative":"创意实验","ai":"AI 产品"}

def dom(u): return u.replace("https://","").rstrip("/")

CSS = """
:root{--paper:#F2EEE3;--card:#FBF8EF;--ink:#191512;--dim:#6E675A;--line:rgba(25,21,18,.22);--red:#C43E1C;
--serif:Georgia,"Times New Roman","Songti SC","STSong","SimSun",serif;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:var(--serif);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 28px}
/* bill header */
.bill{border-bottom:3px double var(--ink);padding:34px 0 22px}
.bill-top{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;font:600 10px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--dim)}
.bill-title{display:flex;align-items:baseline;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:14px}
.bill-title h1{font-size:clamp(34px,5vw,58px);font-weight:700;letter-spacing:.01em}
.bill-title h1 em{font-style:normal;color:var(--red)}
.stamp{border:2px solid var(--red);color:var(--red);font:700 11px var(--mono);letter-spacing:.2em;padding:8px 14px;transform:rotate(-4deg);border-radius:2px}
.bill-meta{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:22px;border:1px solid var(--ink)}
.bill-meta div{padding:12px 16px;border-left:1px solid var(--line)}
.bill-meta div:first-child{border-left:0}
.bill-meta small{display:block;font:600 9px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--dim)}
.bill-meta b{display:block;margin-top:4px;font:700 15px var(--mono)}
/* intro */
.intro{padding:34px 0 10px;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:40px}
.intro h2{font-size:clamp(24px,3vw,34px);line-height:1.4;font-weight:700}
.intro h2 em{font-style:normal;color:var(--red)}
.intro p{font-size:14.5px;line-height:1.9;color:#3E3A30;margin-top:14px}
.shipper{border:1px solid var(--ink);background:var(--card);padding:20px 22px;font-size:13px;line-height:1.9}
.shipper small{display:block;font:600 9px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--dim);margin-bottom:8px}
/* cargo table */
.cargo-head{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin:44px 0 14px}
.cargo-head h2{font-size:clamp(24px,2.8vw,34px);font-weight:700}
.tabs{display:flex;gap:0;border:1px solid var(--ink);border-radius:3px;overflow:hidden}
.tab{border:0;border-left:1px solid var(--ink);background:transparent;color:var(--ink);font:600 11px var(--mono);letter-spacing:.08em;padding:9px 14px;cursor:pointer;transition:.15s}
.tab:first-child{border-left:0}
.tab:hover{background:rgba(25,21,18,.07)}
.tab.on{background:var(--ink);color:var(--paper)}
.cargo{border:1px solid var(--ink);background:var(--card)}
.thead,.item{display:grid;grid-template-columns:64px minmax(0,1.3fr) minmax(0,1fr) 118px 92px;gap:0 18px;align-items:center;padding:0 22px}
.thead{font:600 9px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:var(--dim);padding-top:13px;padding-bottom:13px;border-bottom:1px solid var(--ink)}
.item{padding-top:15px;padding-bottom:15px;border-bottom:1px solid var(--line);transition:background .15s}
.item:last-child{border-bottom:0}
.item:hover{background:rgba(196,62,28,.05)}
.lot{font:700 12px var(--mono);color:var(--dim)}
.what b{display:block;font-size:17px;font-weight:700;line-height:1.3}
.what small{font-size:12px;color:var(--dim)}
.dest{font:500 12.5px var(--mono);color:#55503F;word-break:break-all}
.dest i{font-style:normal;color:var(--red);opacity:0;margin-left:5px;transition:.15s}
.item:hover .dest i{opacity:1}
.duty{font:600 10.5px var(--mono);letter-spacing:.08em;color:var(--ink);border:1px solid var(--line);border-radius:2px;padding:4px 8px;text-align:center;width:fit-content}
.item:hover .duty{border-color:var(--red);color:var(--red)}
.status{font:700 10px var(--mono);letter-spacing:.16em;color:var(--red);text-align:right}
.item:first-child .status{color:var(--red)}
/* terms */
.terms{border-top:3px double var(--ink);margin-top:64px;padding:44px 0}
.terms h2{font-size:clamp(24px,3vw,36px);font-weight:700;max-width:24ch;line-height:1.35}
.terms h2 em{font-style:normal;color:var(--red)}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--ink);border:1px solid var(--ink);margin-top:30px}
.grid4 div{background:var(--card);padding:22px 20px;min-height:150px}
.grid4 b{display:block;font-size:16px;font-weight:700}
.grid4 small{display:block;font:600 9px var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--red);margin-bottom:10px}
.grid4 p{margin-top:9px;font-size:12px;line-height:1.8;color:#55503F}
/* manifesto quote */
.quote{padding:54px 0;text-align:center}
.quote p{font-size:clamp(24px,3.4vw,40px);font-weight:700;line-height:1.4}
.quote p em{font-style:normal;color:var(--red)}
.quote small{display:block;margin-top:16px;font:600 10px var(--mono);letter-spacing:.3em;color:var(--dim)}
/* contact */
.contact{background:var(--ink);color:var(--paper);padding:64px 0 52px}
.contact h2{font-size:clamp(30px,4.4vw,54px);font-weight:700;line-height:1.2}
.contact h2 em{font-style:normal;color:#F5B800}
.crow{display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap;margin-top:30px}
.wx small{display:block;font:600 9px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#9A9583}
.wx b{display:block;font:700 22px var(--mono);margin-top:7px}
.copy{border:0;background:var(--red);color:#fff;font:700 12.5px var(--mono);letter-spacing:.1em;padding:15px 24px;border-radius:3px;cursor:pointer;transition:.15s}
.copy:hover{background:#d9502c}
.fine{margin-top:38px;padding-top:16px;border-top:1px solid rgba(242,238,227,.18);display:flex;justify-content:space-between;gap:12px;font:500 10px var(--mono);letter-spacing:.14em;color:#8B8778}
@media(max-width:860px){
 .bill-meta{grid-template-columns:1fr 1fr}
 .bill-meta div:nth-child(3){border-left:0}
 .bill-meta div:nth-child(n+3){border-top:1px solid var(--line)}
 .intro{grid-template-columns:1fr}
 .thead{display:none}
 .item{grid-template-columns:44px minmax(0,1fr);grid-template-areas:"lot what" "lot dest" "lot duty";gap:5px 12px;padding:13px 16px}
 .lot{grid-area:lot}
 .what{grid-area:what}
 .dest{grid-area:dest;font-size:11.5px}
 .duty{grid-area:duty}
 .status{display:none}
 .grid4{grid-template-columns:1fr 1fr}
}
"""

items = []
for i,(name,cat,dt,num,url,desc) in enumerate(P):
    items.append('<a class="item" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">'
        '<span class="lot">LOT {num}</span>'
        '<span class="what"><b>{name}</b><small>{desc} · {dt}</small></span>'
        '<span class="dest">{dom}<i>↗</i></span>'
        '<span class="duty">{duty}</span>'
        '<span class="status">DELIVERED</span></a>'.format(
        cat=cat,url=url,num=num,name=name,desc=desc,dt=dt,dom=dom(url),duty=CAT[cat]))

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>王子凡 — 货运提单（方案 E）</title>
<style>__CSS__</style>
</head>
<body>
<header class="wrap bill">
  <div class="bill-top"><span>BILL OF LADING / 货运提单</span><span>NO. WZF-2026-0712 / 北京签发</span></div>
  <div class="bill-title">
    <h1>王子凡的<em>发货记录</em></h1>
    <span class="stamp">32 LOTS DELIVERED</span>
  </div>
  <div class="bill-meta">
    <div><small>发货人 Shipper</small><b>王子凡 · ONE PERSON</b></div>
    <div><small>启运港 Origin</small><b>想法 · IDEA</b></div>
    <div><small>目的地 Destination</small><b>真实域名 · LIVE URL</b></div>
    <div><small>交付状态 Status</small><b>32/32 已上线</b></div>
  </div>
</header>
<section class="wrap intro">
  <div>
    <h2>每一件货，都<em>真的送达</em>。</h2>
    <p>我是王子凡，一名 OPC 创业者。这份提单记录 42 天里的 32 次真实交付：每一批货从「一个具体问题」启运，经「最短路径构建」，最终抵达「一个可访问的真实域名」。没有滞留在草稿港的集装箱。</p>
  </div>
  <div class="shipper"><small>SHIPPER'S DECLARATION / 发货人声明</small>不把灵感收藏起来，不用筹备冒充进展。今天能发的货，今天就发。</div>
</section>
<section class="wrap" id="work">
  <div class="cargo-head">
    <h2>货物清单 Manifest</h2>
    <div class="tabs">
      <button class="tab on" data-f="all">全部 32</button>
      <button class="tab" data-f="ai">AI 3</button>
      <button class="tab" data-f="game">游戏 11</button>
      <button class="tab" data-f="tool">工具 10</button>
      <button class="tab" data-f="creative">创意 8</button>
    </div>
  </div>
  <div class="cargo">
    <div class="thead"><span>批次</span><span>货品</span><span>目的地（真实域名）</span><span>品类</span><span>状态</span></div>
    __ITEMS__
  </div>
</section>
<section class="wrap terms" id="system">
  <h2>运输条款：判断 → 构建 → 上线 → 反馈。</h2>
  <div class="grid4">
    <div><small>CLAUSE 01</small><b>判断</b><p>找到真实需求，选中值得立刻动手的问题，不追所有机会。</p></div>
    <div><small>CLAUSE 02</small><b>构建</b><p>AI 放大单人产能，最短路径做出可用版本。</p></div>
    <div><small>CLAUSE 03</small><b>上线</b><p>产品上线才算交付。真实域名，真实用户。</p></div>
    <div><small>CLAUSE 04</small><b>反馈</b><p>用户反馈沉淀为下一次判断的燃料，循环复利。</p></div>
  </div>
</section>
<section class="quote">
  <div class="wrap"><p>船到了港，才算<em>真的出过海</em>。</p><small>WZF FREIGHT · MANIFESTO</small></div>
</section>
<footer class="contact" id="contact">
  <div class="wrap">
    <h2>有一批想法想一起发？<em>联系我。</em></h2>
    <div class="crow">
      <div class="wx"><small>WECHAT / DIRECT CONTACT</small><b>wang1227928718</b></div>
      <button class="copy" id="copyBtn">复制微信号</button>
    </div>
    <div class="fine"><span>© 2026 王子凡 ZF WANG · ONE PERSON · ALWAYS SHIPPING</span><span>备注「合作」+ 你的方向</span></div>
  </div>
</footer>
<script>
(function(){
  var tabs=document.querySelectorAll('.tab');
  var items=document.querySelectorAll('.item');
  tabs.forEach(function(t){t.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.remove('on')});
    t.classList.add('on');
    var f=t.getAttribute('data-f');
    items.forEach(function(r){r.style.display=(f==='all'||r.getAttribute('data-cat')===f)?'':'none'});
  })});
  var btn=document.getElementById('copyBtn');
  function done(){btn.textContent='已复制 ✓';setTimeout(function(){btn.textContent='复制微信号'},1600)}
  function fallback(){var i=document.createElement('input');i.value='wang1227928718';document.body.appendChild(i);i.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(i);done()}
  btn.addEventListener('click',function(){
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText('wang1227928718').then(done,fallback)}else{fallback()}
  });
})();
</script>
</body>
</html>
"""

out = os.path.join(os.path.dirname(__file__), "005-manifest")
os.makedirs(out, exist_ok=True)
html = HTML.replace("__CSS__", CSS).replace("__ITEMS__", "\n    ".join(items))
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(
"""## Variant E: 货运提单 MANIFEST

### Design stance
站点是一份货运提单：每个产品是一批已交付的货，真实域名是目的地——"可验证"是核心叙事。

### Key choices
- Layout: 单据版式（提单头/发货人/目的地/状态四格），货物清单表格
- Typography: 衬线正文 + 等宽单据字段，印章式红戳
- Color: 纸白 + 墨 + 单据红，克制三色
- Interaction: 品类筛选、行悬停显示 ↗、印章、复制微信号

### Trade-offs
- Strong at: 可验证性/可信度叙事，"每件货真的送达"的比喻完整
- Weak at: 隐喻较重，能量感低于出发大屏

### Best for
想强调"真实交付、可访问证据"的可信度，面向合作方/投资人视角。
""")
print("wrote", os.path.join(out, "index.html"), len(html), "bytes,", len(items), "items")
