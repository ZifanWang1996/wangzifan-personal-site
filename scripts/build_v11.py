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


def render_latest(projects: list[dict]) -> str:
    latest = sorted(
        (project for project in projects if project["status"] == "live"),
        key=lambda project: (project["launched_at"], project["id"]),
        reverse=True,
    )[:3]
    cards = []
    for project in latest:
        cards.append(
            f'''<article class="latest-card" data-latest-card="{project["id"]}">
          <a class="card-image" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer" aria-label="访问 {text(project["name"])}">
            <img src="{text(project["image"])}" width="400" height="250" alt="{text(project["name"])} 项目页面截图" loading="lazy" decoding="async">
            <span class="live-pill"><i aria-hidden="true"></i> ONLINE</span>
          </a>
          <div class="card-body">
            <div class="card-kicker"><span>{text(project["launched_at"])}</span><span>{text(CATEGORY_LABELS[project["category"]])}</span></div>
            <h3>{text(project["name"])}</h3>
            <p>{text(project["subtitle"])}</p>
            <a class="text-link" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">访问 {text(domain(project["url"]))} <span aria-hidden="true">↗</span></a>
          </div>
        </article>'''
        )
    return f'''<section class="section recent" aria-labelledby="recent-title">
      <div class="section-heading">
        <p class="section-no">01 / RECENT RELEASES</p>
        <div><h2 id="recent-title">最近发布</h2><p>先看最近做成的三件事。每个项目都有可访问网址，而不是概念图。</p></div>
      </div>
      <div class="latest-grid">{"".join(cards)}</div>
    </section>'''


def render_featured(projects: list[dict]) -> str:
    featured = sorted(
        (project for project in projects if project["featured"]),
        key=lambda project: project["featured_order"],
    )
    cards = []
    for project in featured:
        cards.append(
            f'''<article class="case-card" data-featured-card="{project["id"]}">
          <div class="case-media">
            <img src="{text(project["image"])}" width="400" height="250" alt="{text(project["name"])} 项目页面截图" loading="lazy" decoding="async">
            <span>{text(CATEGORY_LABELS[project["category"]])}</span>
          </div>
          <div class="case-content">
            <div class="case-title"><span>{project["featured_order"]:02d}</span><div><h3>{text(project["name"])}</h3><p>{text(project["subtitle"])}</p></div></div>
            <dl class="case-proof">
              <div><dt><span>问题</span></dt><dd>{text(project["problem"])}</dd></div>
              <div><dt><span>解法</span></dt><dd>{text(project["solution"])}</dd></div>
              <div><dt><span>证据</span></dt><dd>{text(project["evidence"])}</dd></div>
            </dl>
            <a class="text-link" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">查看公开产品 <span aria-hidden="true">↗</span></a>
          </div>
        </article>'''
        )
    return f'''<section class="section selected" id="selected" aria-labelledby="selected-title">
      <div class="section-heading">
        <p class="section-no">02 / SELECTED WORK</p>
        <div><h2 id="selected-title">六个代表案例</h2><p>不按技术栈罗列能力。每个案例只回答三件事：问题是什么、如何解决、什么可以验证。</p></div>
      </div>
      <div class="case-grid">{"".join(cards)}</div>
    </section>'''


def render_collaboration() -> str:
    return '''<section class="collaboration" id="collaboration" aria-labelledby="collaboration-title">
      <div>
        <p class="section-no">03 / COLLABORATION</p>
        <h2 id="collaboration-title">有一个具体问题，<br>想把它做成产品？</h2>
      </div>
      <div class="collaboration-copy">
        <p>适合讨论：一人产品、AI 工具、内容型网站、垂直数据库与小而完整的联合实验。先讲清问题、用户和验证方式，再谈怎么做。</p>
        <div class="hero-actions">
          <a class="button button-primary" href="#contact">联系合作 <span aria-hidden="true">↓</span></a>
          <a class="button button-quiet" href="#contact">查看联系方式</a>
        </div>
      </div>
    </section>'''


def render_method() -> str:
    steps = (
        ("01", "找问题", "从真实搜索、重复操作或信息缺口里，挑一个值得解决的具体问题。"),
        ("02", "做最小闭环", "先交付一条从进入、理解、使用到得到结果的完整路径。"),
        ("03", "公开发布", "让产品拥有真实网址、可访问页面和可复现的上线证据。"),
        ("04", "持续校正", "根据使用反馈、证据变化和运行状态，修正内容与产品边界。"),
    )
    items = "".join(
        f'''<li data-method-step="{number}"><span>{number}</span><h3>{title}</h3><p>{description}</p></li>'''
        for number, title, description in steps
    )
    return f'''<section class="section method" id="method" aria-labelledby="method-title">
      <div class="section-heading">
        <p class="section-no">04 / WORKING METHOD</p>
        <div><h2 id="method-title">工作方法</h2><p>技术是手段，闭环才是交付。四步反复执行，但每次都以具体问题为起点。</p></div>
      </div>
      <ol class="method-grid">{items}</ol>
    </section>'''


def render_ledger(projects: list[dict]) -> str:
    total = len(projects)
    live = sum(project["status"] == "live" for project in projects)
    offline = sum(project["status"] == "offline" for project in projects)
    rows = []
    ordered = sorted(projects, key=lambda project: project["id"], reverse=True)
    for project in ordered:
        status_label = "在线" if project["status"] == "live" else "当前离线"
        content = f'''<span class="ledger-date">{text(project["launched_at"])}</span>
            <span class="ledger-name"><strong>{text(project["name"])}</strong><small>{text(project["subtitle"])}</small></span>
            <span class="ledger-domain">{text(domain(project["url"]))}</span>
            <span class="ledger-category">{text(CATEGORY_LABELS[project["category"]])}</span>
            <span class="ledger-state is-{text(project["status"])}"><i aria-hidden="true"></i>{status_label}</span>'''
        if project["status"] == "live":
            main = f'''<a class="ledger-main" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">{content}</a>'''
        else:
            main = f'''<div class="ledger-main" aria-label="{text(project["name"])}，当前离线">{content}</div>'''
        rows.append(
            f'''<article class="ledger-row" data-ledger-id="{project["id"]}" data-ledger-category="{text(project["category"])}" data-ledger-status="{text(project["status"])}" data-ledger-search="{text((project["name"] + " " + project["subtitle"] + " " + domain(project["url"])).lower())}">{main}</article>'''
        )

    filters = (
        ("all", "全部"),
        ("ai", "AI 产品"),
        ("game", "游戏与内容"),
        ("tool", "实用工具"),
        ("creative", "创意实验"),
    )
    filter_buttons = "".join(
        f'''<button type="button" class="ledger-filter{' is-active' if value == 'all' else ''}" data-ledger-filter="{value}" aria-pressed="{'true' if value == 'all' else 'false'}">{label}</button>'''
        for value, label in filters
    )
    return f'''<section class="section ledger" id="ledger" aria-labelledby="ledger-title">
      <div class="section-heading">
        <p class="section-no">05 / RELEASE LEDGER</p>
        <div><h2 id="ledger-title">完整发布档案</h2><p>{total} 条历史发布记录，{live} 个当前在线，{offline} 个明确标记为离线。可以按类型、状态和关键词查找。</p></div>
      </div>
      <div class="ledger-tools" hidden aria-label="筛选发布档案">
        <div class="ledger-filters" role="group" aria-label="按产品类型筛选">{filter_buttons}</div>
        <label class="search-field" for="ledger-search"><span>搜索</span><input id="ledger-search" type="search" placeholder="名称、用途或域名" autocomplete="off"></label>
        <label class="status-field" for="ledger-status"><span>状态</span><select id="ledger-status"><option value="all">全部状态</option><option value="live">当前在线</option><option value="offline">当前离线</option></select></label>
      </div>
      <div class="ledger-summary"><strong id="ledger-count" aria-live="polite">{total} / {total}</strong><span>匹配记录</span></div>
      <div class="ledger-head" aria-hidden="true"><span>日期</span><span>产品</span><span>域名</span><span>类型</span><span>状态</span></div>
      <div class="ledger-list" id="ledger-list">{"".join(rows)}</div>
      <button class="button ledger-more" type="button" id="ledger-more" hidden aria-expanded="false" aria-controls="ledger-list">查看全部 {total} 条记录</button>
    </section>'''


def render_about() -> str:
    return '''<section class="section about" id="about" aria-labelledby="about-title">
      <div class="section-heading">
        <p class="section-no">06 / FOUNDER NOTE</p>
        <div><h2 id="about-title">关于王子凡</h2><p>ZF Wang，一人产品工作室创作者。关注 AI 产品、垂直工具、内容型网站和能被真实使用的小型互联网产品。</p></div>
      </div>
      <div class="about-grid">
        <blockquote>“我更愿意用一个能打开、能使用、能继续修正的网址，来说明自己能做什么。”</blockquote>
        <div><h3>合作边界</h3><p>适合从一个明确问题出发，讨论产品定义、原型、内容系统、开发与公开发布。不承诺虚构增长、不包装未经验证的结果，也不把功能堆叠当成交付。</p></div>
      </div>
    </section>'''


def render_contact() -> str:
    return '''<section class="contact" id="contact" aria-labelledby="contact-title">
      <div class="contact-copy">
        <p class="section-no">07 / CONTACT</p>
        <h2 id="contact-title">把问题说清楚，<br>我们从第一步开始。</h2>
        <p>添加微信时，请备注“合作”并附上一句话：你想解决什么问题、主要给谁用。</p>
      </div>
      <div class="contact-card">
        <figure>
          <img src="assets/wechat-qr.webp" width="560" height="560" alt="王子凡微信二维码，微信号 wang1227928718" loading="lazy" decoding="async">
          <figcaption>微信扫码联系</figcaption>
        </figure>
        <div class="contact-details">
          <span>WECHAT / DIRECT CONTACT</span>
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
                "description": "一人产品工作室创作者，关注 AI 产品、垂直工具与内容型网站。",
            },
            {
                "@type": "WebSite",
                "@id": "https://wangzifan.store/#website",
                "url": "https://wangzifan.store/",
                "name": "ZF Wang — 一人产品工作室",
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
            render_latest(projects),
            render_featured(projects),
            render_collaboration(),
            render_method(),
            render_ledger(projects),
            render_about(),
            render_contact(),
        )
    )
    values = {
        "TOTAL": str(len(projects)),
        "LIVE": str(sum(project["status"] == "live" for project in projects)),
        "OFFLINE": str(sum(project["status"] == "offline" for project in projects)),
        "CATEGORY_COUNT": str(len({project["category"] for project in projects})),
        "STRUCTURED_DATA": render_structured_data(projects),
        "CONTENT": content,
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
    )


def write_social_card(path: Path, projects: list[dict]) -> None:
    total = len(projects)
    live = sum(project["status"] == "live" for project in projects)
    offline = sum(project["status"] == "offline" for project in projects)
    image = Image.new("RGB", (1200, 630), "#f2f0ea")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 78, 630), fill="#16283a")
    draw.rectangle((78, 0, 98, 630), fill="#e34a2f")
    draw.rectangle((970, 0, 1200, 630), fill="#171816")
    draw.text((150, 115), "ZF WANG", font=load_social_font(98), fill="#171816")
    draw.text((155, 235), "ONE-PERSON PRODUCT STUDIO", font=load_social_font(30), fill="#a82f1d")
    draw.line((155, 315, 900, 315), fill="#171816", width=3)
    draw.text((155, 355), f"{total} RELEASE RECORDS", font=load_social_font(42), fill="#171816")
    draw.text((155, 425), f"{live} ONLINE  /  {offline} OFFLINE", font=load_social_font(25), fill="#66675f")
    draw.text((155, 525), "wangzifan.store", font=load_social_font(25), fill="#171816")
    draw.text((1023, 483), "WZ", font=load_social_font(66), fill="#fcfbf7")
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
