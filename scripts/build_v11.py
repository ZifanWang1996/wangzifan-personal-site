#!/usr/bin/env python3
"""Build the deterministic V11 static homepage from the canonical project registry."""

import argparse
import json
import re
import shutil
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CATEGORY_LABELS = {
    "ai": "AI 产品",
    "game": "游戏与内容",
    "tool": "实用工具",
    "creative": "创意实验",
}


def text(value) -> str:
    return escape(str(value), quote=True)


def domain(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.")


def latest_live_project(projects: list[dict]) -> dict:
    return max(
        (project for project in projects if project["status"] == "live"),
        key=lambda project: (project["launched_at"], project["id"]),
    )


def render_method() -> str:
    notes = json.loads((ROOT / "data" / "journal.json").read_text(encoding="utf-8"))
    items = "".join(
        f'''<li data-method-note="{number}"><div class="journal-meta"><span>手记 / {number}</span><span>{tag}</span></div><h3>{title}</h3><p>{description}</p><a class="text-link" href="#project-{project_id}">查看相关作品 <span aria-hidden="true">↗</span></a></li>'''
        for note in notes
        for number, title, description, tag, project_id in [tuple(text(note[key]) for key in ("number", "title", "body", "tag", "project_id"))]
    )
    return f'''<section class="section method" id="method" aria-labelledby="method-title">
      <div class="section-heading"><p class="section-no">02 / 构建手记</p><div><h2 id="method-title">做过，才有话可说。</h2><p>从已有作品里，记下三个正在实践的产品选择。</p></div></div>
      <ol class="method-grid">{items}</ol>
      <div class="journal-colophon"><span>保持好奇，也保持具体。</span><span>NOTES FROM THE WORKBENCH ↗</span></div>
    </section>'''


def render_ledger(projects: list[dict]) -> str:
    total = len(projects)
    live = sum(project["status"] == "live" for project in projects)
    offline = sum(project["status"] == "offline" for project in projects)
    rows = []
    ordered = sorted(projects, key=lambda project: project["id"], reverse=True)
    for project in ordered:
        status_label = "在线记录" if project["status"] == "live" else "离线记录"
        content = f'''<span class="project-window">
              <span class="window-bar"><span class="ledger-domain">{text(domain(project["url"]))}</span><span class="card-read">访问网站 ↗</span></span>
              <img src="{text(project["image"])}" width="800" height="500" alt="{text(project["name"])} 项目截图" loading="lazy" decoding="async">
            </span>
            <span class="project-info">
              <span class="project-kicker"><span class="project-number">/{project["id"]:02d}</span><span class="ledger-category">{text(CATEGORY_LABELS[project["category"]])}</span></span>
              <span class="ledger-name"><strong>{text(project["name"])}</strong><small>{text(project["subtitle"])}</small></span>
              <span class="project-footer"><span class="ledger-date">{text(project["launched_at"])}</span><span class="ledger-state is-{text(project["status"])}"><i aria-hidden="true"></i>{status_label}</span></span>
            </span>'''
        if project["status"] == "live":
            main = f'''<a class="ledger-main" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">{content}</a>'''
        else:
            main = f'''<div class="ledger-main" aria-label="{text(project["name"])}，离线记录">{content}</div>'''
        rows.append(
            f'''<article class="ledger-row" data-ledger-id="{project["id"]}" id="project-{project["id"]}" data-ledger-period="{text(project["launched_at"][:7])}" data-ledger-category="{text(project["category"])}" data-ledger-status="{text(project["status"])}" data-ledger-search="{text((project["name"] + " " + project["subtitle"] + " " + domain(project["url"])).lower())}">{main}</article>'''
        )

    filters = (
        ("all", "全部"),
        ("ai", "AI 产品"),
        ("game", "游戏与内容"),
        ("tool", "实用工具"),
        ("creative", "创意实验"),
    )
    filter_buttons = "".join(
        f'''<button type="button" class="ledger-filter{' is-active' if value == 'all' else ''}" data-ledger-filter="{value}" aria-pressed="{'true' if value == 'all' else 'false'}">{label}<span>{total if value == "all" else sum(p["category"] == value for p in projects):02d}</span></button>'''
        for value, label in filters
    )
    periods = sorted({p["launched_at"][:7] for p in projects}, reverse=True)
    years = sorted({p["launched_at"][:4] for p in projects}, reverse=True)
    period_options = "".join(f'<option value="{v}">{v} 年</option>' for v in years)
    period_options += "".join(f'<option value="{v}">{v[:4]} 年 {int(v[5:])} 月</option>' for v in periods)
    return f'''<section class="section ledger" id="ledger" aria-labelledby="ledger-title">
      <div class="section-heading">
        <p class="section-no">01 / 作品索引</p>
        <div><h2 id="ledger-title">一张不断生长的产品地图。</h2><p>{total} 个产品与实验，从游戏、AI 到日常工具。按兴趣探索，也可以切换清单快速查找。</p></div>
      </div>
      <div class="ledger-tools" hidden aria-label="筛选发布档案">
        <div class="ledger-filters" role="group" aria-label="按产品类型筛选">{filter_buttons}</div>
        <label class="search-field" for="ledger-search"><span>搜索</span><input id="ledger-search" type="search" placeholder="名称、用途或域名" autocomplete="off"></label>
        <label class="period-field" for="ledger-period"><span>时间</span><select id="ledger-period"><option value="all">全部时间</option>{period_options}</select></label>
        <label class="status-field" for="ledger-status"><span>状态</span><select id="ledger-status"><option value="all">全部状态</option><option value="live">在线记录</option><option value="offline">离线记录</option></select></label>
      </div>
      <div class="ledger-summary"><div><strong id="ledger-count" aria-live="polite">{total} / {total}</strong><span>个项目</span></div><div class="view-switch" role="group" aria-label="作品展示方式" hidden><button type="button" data-view="wall" aria-pressed="true">杂志</button><button type="button" data-view="list" aria-pressed="false">清单</button></div></div>
      <div class="ledger-list" id="ledger-list">{"".join(rows)}</div>
      <p class="ledger-empty" id="ledger-empty" role="status" hidden>没有匹配记录，试试别的关键词或筛选。</p>
      <button class="button ledger-more" type="button" id="ledger-more" hidden aria-expanded="false" aria-controls="ledger-list">查看全部 {total} 条记录</button>
    </section>'''


def render_about(projects: list[dict]) -> str:
    return f'''<section class="section about" id="about" aria-labelledby="about-title">
      <div class="about-identity"><p class="section-no">03 / 关于王子凡</p><div class="identity-letter" aria-hidden="true">ZF<span>↗</span></div><div class="identity-caption"><strong>王子凡 / ZF WANG</strong><span>OPC 一人公司创业者</span></div></div>
      <div class="about-story"><p class="eyebrow">规模可以小，作品要认真。</p><h2 id="about-title">选择自己想解决的问题，<br>也对结果负责。</h2><p>我是王子凡，正在实践 OPC 一人公司创业。我想建立一家由自己掌舵、靠产品创造价值的小公司：从需求出发，用 AI 协作，把想法带到真实用户面前。</p><p>这个页面记录着 {len(projects)} 次公开上线。从游戏指南到实用工具，每一次尝试都让我更具体地理解：一个人能把什么做出来，又有哪些地方值得继续改进。</p><div class="about-invitation"><span>欢迎同路人</span><h3>带着一个具体问题来聊。</h3><p>如果你也在做一人公司、AI 产品或出海项目，欢迎交换构建经验；如果你有清晰的需求，也可以一起讨论产品原型、内容工具和网站体验。</p><a class="text-link" href="#contact">认识一下 →</a></div></div>
    </section>'''


def render_project_dialog(projects: list[dict]) -> str:
    fields = ("id", "name", "url", "category", "subtitle", "summary", "problem", "solution", "evidence", "launched_at", "status", "image")
    public = [{k: p[k] for k in fields} for p in projects]
    payload = json.dumps(public, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return '''<dialog id="project-dialog" aria-labelledby="detail-title">
      <div class="dialog-top"><span>作品档案 / <span id="detail-number"></span></span><button type="button" id="detail-close" aria-label="关闭项目详情">关闭 <span aria-hidden="true">×</span></button></div>
      <div class="detail-body"><p class="eyebrow" id="detail-category"></p><h2 id="detail-title"></h2><p id="detail-subtitle"></p><p class="detail-summary" id="detail-summary"></p>
      <dl class="detail-facts"><div><dt>收录日期</dt><dd id="detail-date"></dd></div><div><dt>档案状态</dt><dd id="detail-status"></dd></div></dl>
      <div class="detail-section" id="detail-problem-wrap"><h3>从什么问题出发</h3><p id="detail-problem"></p></div><div class="detail-section" id="detail-solution-wrap"><h3>怎么解决</h3><p id="detail-solution"></p></div><div class="detail-section"><h3>这份作品的记录</h3><p id="detail-evidence"></p></div>
      <div id="detail-visit"></div></div>
    </dialog><script type="application/json" id="project-data">''' + payload + '</script>'


def render_contact() -> str:
    return '''<section class="contact" id="contact" aria-labelledby="contact-title">
      <div class="contact-copy">
        <p class="section-no">下一次出发</p>
        <h2 id="contact-title">有个想法？<br>一起把它做出来。</h2>
        <p>聊产品，聊 AI，聊一人公司的机会和难题。加微信时备注“一人公司”，说说你正在做什么，或者想解决什么问题。</p>
      </div>
      <div class="contact-card">
        <figure>
          <img src="assets/wechat-qr.webp" width="560" height="560" alt="王子凡微信二维码，微信号 wang1227928718" loading="lazy" decoding="async">
          <figcaption>微信扫码联系</figcaption>
        </figure>
        <div class="contact-details">
          <span>微信号</span>
          <strong id="wechat-value">wang1227928718</strong>
          <button class="button copy-button" type="button" hidden data-copy-value="wang1227928718" aria-describedby="copy-status">复制微信号</button>
          <p id="copy-status" class="copy-status" role="status" aria-live="polite"></p>
          <label class="manual-copy" hidden>手动复制<input value="wang1227928718" readonly></label>
        </div>
      </div>
    </section>'''


def render_structured_data(projects: list[dict]) -> str:
    release_items = []
    ordered = sorted(projects, key=lambda project: project["id"], reverse=True)
    for position, project in enumerate(ordered, start=1):
        item = {
            "@type": "CreativeWork",
            "name": project["name"],
            "datePublished": project["launched_at"],
            "genre": CATEGORY_LABELS[project["category"]],
            "additionalProperty": {
                "@type": "PropertyValue",
                "name": "public status",
                "value": project["status"],
            },
        }
        if project["status"] == "live":
            item["url"] = project["url"]
        release_items.append(
            {"@type": "ListItem", "position": position, "item": item}
        )

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": "https://wangzifan.store/#person",
                "name": "王子凡",
                "alternateName": "ZF Wang",
                "url": "https://wangzifan.store/",
                "description": "OPC 一人公司创业者，以 AI、产品与持续发布探索独立创业。",
            },
            {
                "@type": "WebSite",
                "@id": "https://wangzifan.store/#website",
                "url": "https://wangzifan.store/",
                "name": "王子凡（ZF Wang）— 个人产品工作台",
                "inLanguage": "zh-CN",
                "publisher": {"@id": "https://wangzifan.store/#person"},
            },
            {
                "@type": "ItemList",
                "@id": "https://wangzifan.store/#release-ledger",
                "name": "ZF Wang 公开产品发布档案",
                "numberOfItems": len(projects),
                "itemListOrder": "https://schema.org/ItemListOrderDescending",
                "itemListElement": release_items,
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace(
        "<", "\\u003c"
    )


def render_homepage() -> str:
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    template = (ROOT / "src" / "index.template.html").read_text(encoding="utf-8")
    content = "\n\n    ".join(
        (
            render_ledger(projects),
            render_method(),
            render_about(projects),
            render_contact(),
        )
    )
    values = {
        "TOTAL": str(len(projects)),
        "LIVE": str(sum(project["status"] == "live" for project in projects)),
        "OFFLINE": str(sum(project["status"] == "offline" for project in projects)),
        "LATEST_DATE": latest_live_project(projects)["launched_at"],
        "STRUCTURED_DATA": render_structured_data(projects),
        "CONTENT": content,
        "PROJECT_DIALOG": render_project_dialog(projects),
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", template):
        raise ValueError("unresolved template placeholder")
    return template.rstrip() + "\n"


def render_privacy() -> str:
    return (ROOT / "src" / "privacy.template.html").read_text(encoding="utf-8").rstrip() + "\n"


def load_social_font(size: int):
    return ImageFont.truetype(
        ROOT / "src" / "fonts" / "DejaVuSans-Bold.ttf",
        size=size,
        layout_engine=ImageFont.Layout.BASIC,
    )


def write_social_card(path: Path, projects: list[dict]) -> None:
    total = len(projects)
    live = sum(project["status"] == "live" for project in projects)
    offline = sum(project["status"] == "offline" for project in projects)
    image = Image.new("RGB", (1200, 630), "#f5f3ee")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 78, 630), fill="#252822")
    draw.rectangle((78, 0, 98, 630), fill="#863d38")
    draw.rectangle((970, 0, 1200, 630), fill="#171816")
    draw.text((150, 115), "ZF WANG", font=load_social_font(98), fill="#171816")
    draw.text((155, 235), "THE INDEPENDENT PRODUCT JOURNAL", font=load_social_font(25), fill="#a82f1d")
    draw.line((155, 315, 900, 315), fill="#171816", width=3)
    draw.text((155, 355), f"{total} PUBLIC RELEASES", font=load_social_font(42), fill="#171816")
    draw.text((155, 425), f"{live} LIVE  /  {offline} OFFLINE", font=load_social_font(25), fill="#66675f")
    draw.text((155, 525), "wangzifan.store", font=load_social_font(25), fill="#171816")
    draw.text((1023, 483), "ZF", font=load_social_font(66), fill="#fcfbf7")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", lossless=True, method=6)


def write_shared_assets(parent: Path) -> None:
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    asset_dir = parent / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "src" / "styles.css", asset_dir / "site.css")
    shutil.copyfile(ROOT / "src" / "site.js", asset_dir / "site.js")
    write_social_card(asset_dir / "og-card.webp", projects)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "index.html")
    parser.add_argument("--privacy-output", type=Path)
    args = parser.parse_args()

    privacy_output = args.privacy_output
    if privacy_output is None and args.output.resolve() == (ROOT / "index.html").resolve():
        privacy_output = ROOT / "privacy.html"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_homepage(), encoding="utf-8")
    write_shared_assets(args.output.parent)

    if privacy_output is not None:
        privacy_output.parent.mkdir(parents=True, exist_ok=True)
        privacy_output.write_text(render_privacy(), encoding="utf-8")
        if privacy_output.parent.resolve() != args.output.parent.resolve():
            write_shared_assets(privacy_output.parent)


if __name__ == "__main__":
    main()
