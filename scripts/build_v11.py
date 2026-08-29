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


def render_hero_latest(projects: list[dict]) -> str:
    project = latest_live_project(projects)
    return f'''<aside class="hero-latest" data-hero-latest="{project["id"]}" aria-label="工作台最近状态">
        <div class="hero-latest-copy">
          <p><span>工作台最近</span><time datetime="{text(project["launched_at"])}">{text(project["launched_at"])}</time></p>
          <span class="hero-latest-state">刚上线</span>
          <h2>{text(project["name"])}</h2>
          <p>{text(project["subtitle"])} · {text(domain(project["url"]))}</p>
          <a href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">打开这次上线 <span aria-hidden="true">↗</span></a>
          <p class="hero-latest-note">不叫“最佳作品”，这里只按上线时间排。</p>
        </div>
      </aside>'''


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
            <span class="live-pill"><i aria-hidden="true"></i> 在线</span>
          </a>
          <div class="card-body">
            <div class="card-kicker"><span>{text(project["launched_at"])}</span><span>{text(CATEGORY_LABELS[project["category"]])}</span></div>
            <h3>{text(project["name"])}</h3>
            <p>{text(project["subtitle"])}</p>
            <a class="text-link" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">访问 {text(domain(project["url"]))} <span aria-hidden="true">↗</span></a>
          </div>
        </article>'''
        )
    return f'''<section class="section recent" id="recent" aria-labelledby="recent-title">
      <div class="section-heading">
        <p class="section-no">最近做的</p>
        <div><h2 id="recent-title">最近三次上线</h2><p>先看成品。想知道我怎么想、删了什么，再往下。</p></div>
      </div>
      <div class="latest-grid">{"".join(cards)}</div>
    </section>'''


def render_featured(projects: list[dict]) -> str:
    featured = sorted(
        (project for project in projects if project["featured"]),
        key=lambda project: project["featured_order"],
    )
    stories = {
        20: (
            ("为什么做", "AI 文本检测如果只给一个百分比，很容易被当成判决。"),
            ("我做的取舍", "把置信度、逐句理由和误判提示一起交给用户，而不是只留一个结果。"),
        ),
        22: (
            ("最重要的边界", "图片和视频不上传服务器，校色在浏览器本地完成。"),
            ("使用路径", "导入、对比、调整、导出。除此之外的功能，第一版先不做。"),
        ),
        9: (
            ("从哪里开始", "不先堆朝代百科，先把钱型、年代和铸造背景串成一条入门路径。"),
            ("我坚持的事", "双语内容、来源说明和本地识别工具放在一起。"),
        ),
    }
    cards = []
    for project in featured:
        notes = stories[project["id"]]
        cards.append(
            f'''<article class="case-card" data-featured-card="{project["id"]}">
          <div class="case-media">
            <img src="{text(project["image"])}" width="400" height="250" alt="{text(project["name"])} 项目页面截图" loading="lazy" decoding="async">
            <span>{text(CATEGORY_LABELS[project["category"]])}</span>
          </div>
          <div class="case-content">
            <div class="case-title"><span>我选这个项目</span><div><h3>{text(project["name"])}</h3><p>{text(project["subtitle"])}</p></div></div>
            <dl class="case-proof">
              <div><dt><span>{text(notes[0][0])}</span></dt><dd>{text(notes[0][1])}</dd></div>
              <div><dt><span>{text(notes[1][0])}</span></dt><dd>{text(notes[1][1])}</dd></div>
              <div><dt><span>现在能验证</span></dt><dd>{text(project["evidence"])}</dd></div>
            </dl>
            <a class="text-link" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">打开这个产品 <span aria-hidden="true">↗</span></a>
          </div>
        </article>'''
        )
    return f'''<section class="section selected" id="selected" aria-labelledby="selected-title">
      <div class="section-heading">
        <p class="section-no">愿意细讲的</p>
        <div><h2 id="selected-title">三个我愿意<span class="no-break">细讲的项目</span></h2><p>它们不是最大或最贵的，只是最能说明我怎么判断问题、删功能，再把东西发出去。</p></div>
      </div>
      <div class="case-grid">{"".join(cards)}</div>
    </section>'''


def render_collaboration() -> str:
    return '''<section class="collaboration" id="collaboration" aria-labelledby="collaboration-title">
      <div>
        <p class="section-no">可以一起做</p>
        <h2 id="collaboration-title">手上有个小问题，<br>一直没人愿意认真做？</h2>
      </div>
      <div class="collaboration-copy">
        <p>把谁遇到什么麻烦、你已经试过什么发给我。先判断值不值得做，不急着列功能表。</p>
        <div class="hero-actions">
          <a class="button button-primary" href="#contact">微信聊聊 <span aria-hidden="true">↓</span></a>
        </div>
      </div>
    </section>'''


def render_method() -> str:
    notes = (
        ("01", "先找最短的一条路", "我不会先把 PRD 写满。先找一个用户能从头走到尾、最后拿到结果的路径。"),
        ("02", "第一版要完整走通", "页面少一点没关系；入口、核心动作、结果和失败提示不能断。"),
        ("03", "发出去再决定加什么", "有真实网址之后，再看使用、搜索和反馈。没人需要的功能，不因为“完整”就补上。"),
    )
    items = "".join(
        f'''<li data-method-note="{number}"><span>{number}</span><h3>{title}</h3><p>{description}</p></li>'''
        for number, title, description in notes
    )
    return f'''<section class="section method" id="method" aria-labelledby="method-title">
      <div class="section-heading">
        <p class="section-no">做事习惯</p>
        <div><h2 id="method-title">我通常怎么开始</h2><p>不是方法论，只是我连续做过这些项目后，留下来的三个习惯。</p></div>
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
        status_label = "在线记录" if project["status"] == "live" else "离线记录"
        content = f'''<span class="ledger-date">{text(project["launched_at"])}</span>
            <span class="ledger-name"><strong>{text(project["name"])}</strong><small>{text(project["subtitle"])}</small></span>
            <span class="ledger-domain">{text(domain(project["url"]))}</span>
            <span class="ledger-category">{text(CATEGORY_LABELS[project["category"]])}</span>
            <span class="ledger-state is-{text(project["status"])}"><i aria-hidden="true"></i>{status_label}</span>'''
        if project["status"] == "live":
            main = f'''<a class="ledger-main" href="{text(project["url"])}" target="_blank" rel="noopener noreferrer">{content}</a>'''
        else:
            main = f'''<div class="ledger-main" aria-label="{text(project["name"])}，离线记录">{content}</div>'''
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
        <p class="section-no">全部记录</p>
        <div><h2 id="ledger-title">完整发布档案</h2><p>这里不只留“代表作”。{total} 条历史记录里，{live} 条标记在线，{offline} 条标记离线；都按原样保留。</p></div>
      </div>
      <div class="ledger-tools" hidden aria-label="筛选发布档案">
        <div class="ledger-filters" role="group" aria-label="按产品类型筛选">{filter_buttons}</div>
        <label class="search-field" for="ledger-search"><span>搜索</span><input id="ledger-search" type="search" placeholder="名称、用途或域名" autocomplete="off"></label>
        <label class="status-field" for="ledger-status"><span>状态</span><select id="ledger-status"><option value="all">全部状态</option><option value="live">在线记录</option><option value="offline">离线记录</option></select></label>
      </div>
      <div class="ledger-summary"><strong id="ledger-count" aria-live="polite">{total} / {total}</strong><span>匹配记录</span></div>
      <div class="ledger-head" aria-hidden="true"><span>日期</span><span>产品</span><span>域名</span><span>类型</span><span>状态</span></div>
      <div class="ledger-list" id="ledger-list">{"".join(rows)}</div>
      <p class="ledger-empty" id="ledger-empty" role="status" hidden>没有匹配记录，试试别的关键词或筛选。</p>
      <button class="button ledger-more" type="button" id="ledger-more" hidden aria-expanded="false" aria-controls="ledger-list">查看全部 {total} 条记录</button>
    </section>'''


def render_about() -> str:
    return '''<section class="section about" id="about" aria-labelledby="about-title">
      <div class="section-heading">
        <p class="section-no">关于我</p>
        <div><h2 id="about-title">我把上线过的，也把后来下线的留在这里</h2><p>我叫王子凡，习惯把一个具体问题做成能打开的网址。这个页面收着 33 次公开上线，不只挑最好看的。</p></div>
      </div>
      <div class="about-grid">
        <blockquote>上线不是收尾。域名、登录、隐私、故障和后来下线的记录，都算产品的一部分。</blockquote>
        <div><h3>合作前先对齐</h3><p>适合讨论一人产品、AI 工具、内容型网站、垂直数据库和小而完整的联合实验。开始前会先把问题、边界和能验证的结果写清楚。</p><a class="text-link" href="#contact">直接联系我 →</a></div>
      </div>
    </section>'''


def render_contact() -> str:
    return '''<section class="contact" id="contact" aria-labelledby="contact-title">
      <div class="contact-copy">
        <p class="section-no">直接联系</p>
        <h2 id="contact-title">有事直接说。</h2>
        <p>加微信时备注“合作”，再写一句：谁遇到了什么问题。背景不用整理得很完整，先把事情说清楚。</p>
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
                "description": "独立产品作者，持续制作 AI 产品、垂直工具、游戏资料站和内容型网站。",
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
        "LATEST_DATE": latest_live_project(projects)["launched_at"],
        "HERO_LATEST": render_hero_latest(projects),
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
    draw.text((155, 235), "SMALL, COMPLETE PRODUCTS", font=load_social_font(30), fill="#a82f1d")
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
