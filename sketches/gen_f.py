#!/usr/bin/env python3
"""Variant F: DAYLIGHT OS — Venture OS 做成白天精密仪表盘，冷静现代可信赖。"""
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
:root{--bg:#FAFBFC;--panel:#FFFFFF;--ink:#0B1220;--sub:#5B6472;--line:#E4E7EC;--line2:#EDF0F3;
--blue:#1D4ED8;--green:#047857;--orange:#B45309;--vio:#6D28D9;--red:#B91C1C;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1140px;margin:0 auto;padding:0 28px}
/* topbar */
.topbar{background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:40}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;height:58px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px;letter-spacing:-.01em}
.brand i{width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(4,120,87,.14)}
.nav a{font-size:13.5px;color:var(--sub);margin-left:26px;transition:.15s}
.nav a:hover{color:var(--ink)}
.nav a.cta{color:var(--panel);background:var(--ink);padding:8px 16px;border-radius:8px;font-weight:600}
.nav a.cta:hover{background:#1E293B}
/* hero */
.hero{padding:60px 0 40px}
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:7px 14px;font:600 12px var(--mono);color:var(--sub)}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--green)}
.hero h1{font-size:clamp(38px,5.4vw,66px);line-height:1.08;font-weight:800;letter-spacing:-.03em;margin-top:20px;max-width:16ch}
.hero h1 span{color:var(--blue)}
.hero p{margin-top:18px;font-size:16px;line-height:1.9;color:var(--sub);max-width:62ch}
.hero p b{color:var(--ink)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:38px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px}
.kpi small{font:600 11px var(--mono);letter-spacing:.08em;color:var(--sub);text-transform:uppercase}
.kpi b{display:block;margin-top:9px;font-size:34px;font-weight:800;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kpi b em{font-style:normal;font-size:16px;color:var(--sub);font-weight:600}
.kpi .bar{margin-top:13px;height:6px;border-radius:999px;background:var(--line2);overflow:hidden}
.kpi .bar i{display:block;height:100%;border-radius:999px}
/* section head */
.shead{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin:8px 0 18px}
.shead h2{font-size:clamp(24px,2.8vw,34px);font-weight:800;letter-spacing:-.02em}
.seg{display:flex;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:3px;gap:2px}
.seg button{border:0;background:transparent;color:var(--sub);font:600 12.5px var(--sans);padding:7px 13px;border-radius:8px;cursor:pointer;transition:.15s}
.seg button:hover{color:var(--ink)}
.seg button.on{background:var(--ink);color:#fff}
/* release table */
.table{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.thead,.rrow{display:grid;grid-template-columns:86px minmax(0,1.5fr) minmax(0,1fr) 118px 86px;gap:0 18px;align-items:center;padding:0 22px}
.thead{font:600 11px var(--sans);color:var(--sub);text-transform:uppercase;letter-spacing:.04em;padding-top:13px;padding-bottom:13px;border-bottom:1px solid var(--line);background:#F7F8FA}
.rrow{padding-top:14px;padding-bottom:14px;border-bottom:1px solid var(--line2);transition:background .13s}
.rrow:last-child{border-bottom:0}
.rrow:hover{background:#F7F9FC}
.rdate{font:500 12.5px var(--mono);color:var(--sub)}
.rname b{display:block;font-size:15px;font-weight:700;line-height:1.3;letter-spacing:-.01em}
.rname small{font-size:12.5px;color:var(--sub)}
.rurl{font:500 12.5px var(--mono);color:var(--sub);word-break:break-all}
.rurl i{font-style:normal;color:var(--blue);opacity:0;margin-left:4px;transition:.13s}
.rrow:hover .rurl i{opacity:1}
.tag{font:600 11px var(--sans);padding:4px 10px;border-radius:999px;width:fit-content}
.tag.ai{background:rgba(29,78,216,.09);color:var(--blue)}
.tag.game{background:rgba(109,40,217,.09);color:var(--vio)}
.tag.tool{background:rgba(4,120,87,.09);color:var(--green)}
.tag.creative{background:rgba(180,83,9,.1);color:var(--orange)}
.rst{font:600 11px var(--sans);color:var(--green);display:flex;align-items:center;gap:6px;justify-content:flex-end}
.rst i{width:6px;height:6px;border-radius:50%;background:var(--green)}
.rrow.latest{background:rgba(29,78,216,.03)}
.rrow.latest .rname b{color:var(--blue)}
/* system */
.system{padding:70px 0 30px}
.system h2{font-size:clamp(26px,3.2vw,40px);font-weight:800;letter-spacing:-.02em;max-width:20ch;line-height:1.25}
.sys{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}
.sys div{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px;position:relative;transition:.18s}
.sys div:hover{border-color:#C9D2DE;transform:translateY(-3px);box-shadow:0 12px 30px rgba(11,18,32,.07)}
.sys div b{display:block;font-size:17px;font-weight:700;letter-spacing:-.01em}
.sys div small{display:block;font:600 10.5px var(--mono);letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px}
.sys div:nth-child(1) small{color:var(--blue)}
.sys div:nth-child(2) small{color:var(--vio)}
.sys div:nth-child(3) small{color:var(--green)}
.sys div:nth-child(4) small{color:var(--orange)}
.sys div p{margin-top:9px;font-size:13px;line-height:1.8;color:var(--sub)}
.sys div:after{content:"→";position:absolute;top:50%;right:-12px;transform:translateY(-50%);color:#C1C8D2;font-size:14px;z-index:1}
.sys div:last-child:after{display:none}
/* credo */
.credo{background:var(--ink);color:#fff;border-radius:18px;padding:54px 44px;margin:64px 0;display:flex;justify-content:space-between;align-items:center;gap:34px;flex-wrap:wrap}
.credo p{font-size:clamp(22px,3vw,34px);font-weight:800;letter-spacing:-.02em;line-height:1.4;max-width:24ch}
.credo p span{color:#7DA2FF}
.credo small{font:600 11px var(--mono);letter-spacing:.24em;color:#8B94A6}
/* contact */
.contact{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:44px;margin-bottom:64px;display:flex;justify-content:space-between;align-items:center;gap:34px;flex-wrap:wrap}
.contact h2{font-size:clamp(24px,3vw,36px);font-weight:800;letter-spacing:-.02em;line-height:1.3}
.contact h2 span{color:var(--blue)}
.cright{text-align:right}
.cright small{display:block;font:600 10.5px var(--mono);letter-spacing:.2em;color:var(--sub);text-transform:uppercase}
.cright b{display:block;font:700 22px var(--mono);margin-top:8px;letter-spacing:.02em}
.copy{margin-top:16px;border:0;background:var(--ink);color:#fff;font:600 13px var(--sans);padding:13px 22px;border-radius:10px;cursor:pointer;transition:.15s}
.copy:hover{background:#1E293B}
footer{padding:26px 0 34px;display:flex;justify-content:space-between;gap:12px;font:500 11.5px var(--mono);color:var(--sub)}
@media(max-width:880px){
 .kpis{grid-template-columns:1fr 1fr}
 .thead{display:none}
 .rrow{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"name tag" "url url" "date rst";gap:6px 12px;padding:13px 16px}
 .rname{grid-area:name}
 .rurl{grid-area:url;font-size:11.5px}
 .tag{grid-area:tag}
 .rdate{grid-area:date}
 .rst{grid-area:rst}
 .sys{grid-template-columns:1fr}
 .sys div:after{display:none}
 .contact{flex-direction:column;align-items:flex-start}
 .cright{text-align:left}
}
"""

rows = []
for i,(name,cat,dt,num,url,desc) in enumerate(P):
    latest = " latest" if i==0 else ""
    rows.append('<a class="rrow{lt}" data-cat="{cat}" href="{url}" target="_blank" rel="noopener">'
        '<span class="rdate">{dt}</span>'
        '<span class="rname"><b>{name}</b><small>{desc}</small></span>'
        '<span class="rurl">{dom}<i>↗</i></span>'
        '<span class="tag {cat}">{duty}</span>'
        '<span class="rst"><i></i>LIVE</span></a>'.format(
        lt=latest,cat=cat,url=url,dt=dt,name=name,desc=desc,dom=dom(url),duty=CAT[cat]))

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>王子凡 — Venture OS（方案 F）</title>
<style>__CSS__</style>
</head>
<body>
<div class="topbar"><div class="wrap">
  <div class="brand"><i></i>王子凡 · Venture OS</div>
  <nav class="nav"><a href="#work">上线记录</a><a href="#system">系统</a><a href="#contact" class="cta">合作</a></nav>
</div></div>

<section class="wrap hero">
  <span class="pill"><i></i>SYSTEM ONLINE · 32 PRODUCTS SHIPPED</span>
  <h1>把想法变成产品，<br><span>一个人持续上线。</span></h1>
  <p>我是<b>王子凡</b>，一名 OPC 创业者。过去 42 天上线了 <b>32 个真实产品</b>，平均 1.3 天一个。这里每个条目都对应一个可访问的真实域名——不是演示，是已经在跑的东西。</p>
  <div class="kpis">
    <div class="kpi"><small>Ships / 上线</small><b>32</b><div class="bar"><i style="width:100%;background:var(--blue)"></i></div></div>
    <div class="kpi"><small>Days / 周期</small><b>42<em> 天</em></b><div class="bar"><i style="width:84%;background:var(--green)"></i></div></div>
    <div class="kpi"><small>Cadence / 节奏</small><b>1.3<em> 天/个</em></b><div class="bar"><i style="width:66%;background:var(--vio)"></i></div></div>
    <div class="kpi"><small>Live / 在线率</small><b>100<em>%</em></b><div class="bar"><i style="width:100%;background:var(--orange)"></i></div></div>
  </div>
</section>

<section class="wrap" id="work">
  <div class="shead">
    <h2>上线记录 <span style="color:var(--sub);font-weight:600;font-size:.6em">32 releases</span></h2>
    <div class="seg">
      <button class="on" data-f="all">全部</button>
      <button data-f="ai">AI</button>
      <button data-f="game">游戏</button>
      <button data-f="tool">工具</button>
      <button data-f="creative">创意</button>
    </div>
  </div>
  <div class="table">
    <div class="thead"><span>日期</span><span>产品</span><span>域名</span><span>品类</span><span style="text-align:right">状态</span></div>
    __ROWS__
  </div>
</section>

<section class="wrap system" id="system">
  <h2>一个人的操作系统：判断 → 构建 → 上线 → 反馈。</h2>
  <div class="sys">
    <div><small>STEP 01</small><b>判断</b><p>找到真实需求，选中值得立刻动手的问题，不追所有机会。</p></div>
    <div><small>STEP 02</small><b>构建</b><p>用 AI 放大单人产能，最短路径做出可用版本。</p></div>
    <div><small>STEP 03</small><b>上线</b><p>产品上线才算回答。真实域名，真实用户。</p></div>
    <div><small>STEP 04</small><b>反馈</b><p>用户反馈沉淀为下一次判断的燃料，循环复利。</p></div>
  </div>
</section>

<div class="wrap"><div class="credo">
  <p>不等万事俱备，<span>只做真实上线。</span></p>
  <small>WZF / VENTURE OS · MANIFESTO</small>
</div></div>

<section class="wrap" id="contact"><div class="contact">
  <h2>有个想法想一起做成产品？<br><span>现在就开始。</span></h2>
  <div class="cright">
    <small>WECHAT / DIRECT</small>
    <b>wang1227928718</b>
    <button class="copy" id="copyBtn">复制微信号</button>
  </div>
</div></section>

<footer class="wrap"><span>© 2026 王子凡 ZF Wang · One Person · Always Shipping</span><span>备注「合作」+ 你的方向</span></footer>

<script>
(function(){
  var segs=document.querySelectorAll('.seg button');
  var rows=document.querySelectorAll('.rrow');
  segs.forEach(function(s){s.addEventListener('click',function(){
    segs.forEach(function(x){x.classList.remove('on')});
    s.classList.add('on');
    var f=s.getAttribute('data-f');
    rows.forEach(function(r){r.style.display=(f==='all'||r.getAttribute('data-cat')===f)?'':'none'});
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

out = os.path.join(os.path.dirname(__file__), "006-daylight-os")
os.makedirs(out, exist_ok=True)
html = HTML.replace("__CSS__", CSS).replace("__ROWS__", "\n    ".join(rows))
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(
"""## Variant F: 白天控制室 DAYLIGHT OS

### Design stance
站点是 Venture OS 的白天仪表盘：冷静、现代、可信赖，用数据和状态传达"一个正在运转的系统"。

### Key choices
- Layout: sticky 顶栏 + KPI 卡 + 发布表格，信息密度高但呼吸感足
- Typography: 系统无衬线 + 等宽数字，tabular-nums，克制圆角
- Color: 冷白底 + 墨蓝主色，品类色（蓝/紫/绿/橙）仅用于标签
- Interaction: 分段筛选、行悬停、KPI 进度条、复制微信号

### Trade-offs
- Strong at: 专业感/可信度/可扩展性，像一个真正的产品而非海报
- Weak at: 个性记忆点弱于隐喻型方案（出发大屏/提单）

### Best for
想传达"专业、系统化、可持续"的创业者形象，最通用、最安全的一版。
""")
print("wrote", os.path.join(out, "index.html"), len(html), "bytes,", len(rows), "rows")
