import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


ROOT = Path(__file__).parents[1]
REGISTRY = ROOT / "data" / "projects.json"


def load_projects():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_v11_registry_has_complete_truthful_project_contract():
    projects = load_projects()

    required = {
        "id",
        "name",
        "url",
        "category",
        "subtitle",
        "summary",
        "problem",
        "solution",
        "evidence",
        "launched_at",
        "status",
        "image",
        "featured",
        "featured_order",
    }
    assert len(projects) == 33
    assert [project["id"] for project in projects] == list(range(1, 34))
    assert len({project["url"] for project in projects}) == 33
    assert sum(project["status"] == "live" for project in projects) == 32
    assert sum(project["status"] == "offline" for project in projects) == 1
    assert sum(project["featured"] for project in projects) == 3
    assert sorted(
        project["featured_order"] for project in projects if project["featured"]
    ) == list(range(1, 4))
    assert all(
        project["featured_order"] is None
        for project in projects
        if not project["featured"]
    )
    assert {
        project["id"] for project in projects if project["featured"]
    } == {9, 20, 22}

    for project in projects:
        assert required == set(project)
        assert project["category"] in {"ai", "game", "tool", "creative"}
        assert project["status"] in {"live", "offline", "archived"}
        assert urlparse(project["url"]).scheme == "https"
        assert urlparse(project["url"]).netloc
        assert date.fromisoformat(project["launched_at"])
        assert (ROOT / project["image"]).is_file()
        for field in ("name", "subtitle", "summary", "problem", "solution", "evidence"):
            assert project[field].strip()

    offline = next(project for project in projects if project["id"] == 24)
    assert offline["name"] == "Polski Piłkarz Simulator"
    assert offline["status"] == "offline"


def test_v11_registry_keeps_release_dates_monotonic():
    projects = load_projects()
    dates = [date.fromisoformat(project["launched_at"]) for project in projects]
    assert dates == sorted(dates)


def test_build_v11_generates_truthful_identity_and_counts(tmp_path):
    output = tmp_path / "index.html"
    command = [
        sys.executable,
        str(ROOT / "scripts" / "build_v11.py"),
        "--output",
        str(output),
    ]

    subprocess.run(command, cwd=ROOT, check=True)
    first = output.read_bytes()
    subprocess.run(command, cwd=ROOT, check=True)
    second = output.read_bytes()
    html = first.decode("utf-8")

    assert first == second
    assert "你好，我是王子凡。" in html
    assert "我做小而完整的互联网产品。" in html
    assert '<span class="title-line">我做小而完整的</span>' in html
    assert '<span class="title-line"><em>互联网产品。</em></span>' in html
    assert 'data-hero-latest="33"' in html
    assert 'class="hero-latest-image"' not in html
    assert "工作台最近" in html
    assert "不叫“最佳作品”，这里只按上线时间排。" in html
    assert "Mortal Shell II Wiki" in html
    assert "2026-08-25" in html
    assert '<main id="main-content" tabindex="-1">' in html
    assert 'data-status="releases">33 条公开记录' in html
    assert 'data-status="live">32 条在线记录' in html
    assert 'data-status="offline">1 条离线记录' in html
    for retired in (
        "WZF PRESS",
        "LAUNCH CONSOLE",
        "T-MINUS",
        "SHIPS LIVE",
        "WZF / ONE-PERSON PRODUCT STUDIO",
        "不是传统简历，也不是项目数量墙",
        "问题、解法、证据，三件事讲清楚",
        "一个人，把具体问题做成真正能用的产品",
    ):
        assert retired not in html


def test_build_v11_renders_latest_and_featured_case_studies(tmp_path):
    output = tmp_path / "index.html"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_v11.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    html = output.read_text(encoding="utf-8")
    projects = load_projects()

    assert html.count('data-latest-card="') == 3
    latest_positions = [html.index(f'data-latest-card="{project_id}"') for project_id in (33, 32, 31)]
    assert latest_positions == sorted(latest_positions)

    featured = sorted(
        (project for project in projects if project["featured"]),
        key=lambda project: project["featured_order"],
    )
    assert html.count('data-featured-card="') == 3
    positions = [html.index(f'data-featured-card="{project["id"]}"') for project in featured]
    assert positions == sorted(positions)
    for project in featured:
        assert project["name"] in html
        assert project["evidence"] in html
        assert f'href="{project["url"]}"' in html
        assert f'src="{project["image"]}"' in html

    assert html.count('target="_blank" rel="noopener noreferrer"') >= 6
    assert '<h2 id="selected-title">三个我愿意<span class="no-break">细讲的项目</span></h2>' in html
    for label in ("为什么做", "我做的取舍", "最重要的边界", "使用路径", "从哪里开始", "我坚持的事", "现在能验证"):
        assert f'>{label}</span>' in html
    for retired_label in (">问题</span>", ">解法</span>", ">证据</span>"):
        assert retired_label not in html


def test_build_v11_closes_collaboration_method_ledger_and_contact_flow(tmp_path):
    output = tmp_path / "index.html"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_v11.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    html = output.read_text(encoding="utf-8")

    ordered_ids = ("top", "selected", "collaboration", "method", "ledger", "about", "contact")
    positions = [html.index(f'id="{section_id}"') for section_id in ordered_ids]
    assert positions == sorted(positions)

    assert html.count('data-method-note="') == 3
    assert 'data-method-step="' not in html
    assert "我通常怎么开始" in html
    for habit in ("先找最短的一条路", "第一版要完整走通", "发出去再决定加什么"):
        assert habit in html
    assert html.count('data-ledger-id="') == 33
    ledger_positions = [html.index(f'data-ledger-id="{project_id}"') for project_id in range(33, 0, -1)]
    assert ledger_positions == sorted(ledger_positions)
    assert html.count('data-ledger-status="live"') == 32
    assert html.count('data-ledger-status="offline"') == 1

    offline_row = re.search(
        r'<article[^>]+data-ledger-id="24".*?</article>', html, re.S
    )
    assert offline_row is not None
    assert 'href="https://polskipilkarzsymulator.online/"' not in offline_row.group()
    assert "离线记录" in offline_row.group()

    for category in ("all", "ai", "game", "tool", "creative"):
        assert f'data-ledger-filter="{category}"' in html
    assert 'id="ledger-search"' in html
    assert 'id="ledger-status"' in html
    assert 'id="ledger-count" aria-live="polite">33 / 33' in html
    assert 'class="ledger-tools" hidden' in html
    assert 'class="ledger-empty" id="ledger-empty" role="status" hidden' in html
    assert '<h2 id="selected-title">三个我愿意<span class="no-break">细讲的项目</span></h2>' in html
    assert "没有匹配记录，试试别的关键词或筛选。" in html
    assert 'class="button ledger-more" type="button" id="ledger-more" hidden' in html

    assert html.count('href="#contact"') >= 3
    assert 'src="assets/wechat-qr.webp"' in html
    assert 'class="button copy-button" type="button" hidden' in html
    assert 'alt="王子凡微信二维码，微信号 wang1227928718"' in html
    assert 'data-copy-value="wang1227928718"' in html
    assert "适合讨论" in html and "开始前会先把问题、边界和能验证的结果写清楚" in html
    assert "不承诺虚构增长" not in html
    assert "<canvas" not in html
    assert "requestAnimationFrame" not in html
    for decorative_heading in (
        "RECENT RELEASES",
        "SELECTED WORK",
        "COLLABORATION",
        "WORKING METHOD",
        "RELEASE LEDGER",
        "FOUNDER NOTE",
        "WECHAT / DIRECT CONTACT",
    ):
        assert decorative_heading not in html


def test_build_v11_generates_shared_assets_seo_and_privacy_page(tmp_path):
    output = tmp_path / "index.html"
    privacy = tmp_path / "privacy.html"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_v11.py"),
            "--output",
            str(output),
            "--privacy-output",
            str(privacy),
        ],
        cwd=ROOT,
        check=True,
    )

    html = output.read_text(encoding="utf-8")
    privacy_html = privacy.read_text(encoding="utf-8")
    css = (tmp_path / "assets" / "site.css")
    javascript = (tmp_path / "assets" / "site.js")
    social_image = tmp_path / "assets" / "og-card.webp"

    assert css.read_bytes() == (ROOT / "src" / "styles.css").read_bytes()
    css_text = css.read_text(encoding="utf-8")
    assert 'src: url("archivo.woff2") format("woff2")' in css_text
    assert 'url("assets/archivo.woff2")' not in css_text
    assert "@media (max-width: 1100px)" in css_text
    desktop_transition_css = css_text.split("@media (max-width: 1100px)", 1)[1].split(
        "@media (max-width: 1000px)", 1
    )[0]
    assert ".contact-details { padding-inline: 14px; }" in desktop_transition_css
    assert ".contact h2 { margin: 0; font-size: clamp(45px, 5.4vw, 68px);" in css_text
    assert "@media (max-width: 1000px)" in css_text
    compact_tablet_css = css_text.split("@media (max-width: 1000px)", 1)[1].split(
        "@media (max-width: 900px)", 1
    )[0]
    assert (
        "grid-template-columns: 80px minmax(150px, 1fr) minmax(150px, .8fr) 85px 80px; gap: 10px;"
        in compact_tablet_css
    )
    assert "grid-template-columns: minmax(0, 1fr)" in css_text.split("@media (max-width: 1100px)", 1)[1]
    assert "@media (max-width: 900px)" in css_text
    tablet_css = css_text.split("@media (max-width: 900px)", 1)[1]
    assert ".method-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }" in tablet_css
    assert ".contact { grid-template-columns: minmax(0, 1fr);" in tablet_css
    assert "@media (max-width: 360px)" in css_text
    narrow_mobile_css = css_text.split("@media (max-width: 360px)", 1)[1].split(
        "@media (prefers-reduced-motion: reduce)", 1
    )[0]
    assert ".hero h1 { font-size: 12vw; }" in narrow_mobile_css
    assert ".hero h1 .title-line { white-space: nowrap; }" in narrow_mobile_css
    assert ".no-break { white-space: nowrap; }" in css_text
    assert "font-size: 17px; white-space: nowrap" in css_text
    assert javascript.read_bytes() == (ROOT / "src" / "site.js").read_bytes()
    assert "<style" not in html and "<style" not in privacy_html
    assert '<link rel="stylesheet" href="assets/site.css">' in html
    assert '<script defer src="assets/site.js"></script>' in html
    assert "requestAnimationFrame" not in javascript.read_text(encoding="utf-8")
    assert Image.open(social_image).size == (1200, 630)
    builder_source = (ROOT / "scripts" / "build_v11.py").read_text(encoding="utf-8")
    assert '"33 RELEASE RECORDS"' not in builder_source
    assert '"32 ONLINE  /  1 OFFLINE"' not in builder_source
    assert "33 条历史发布记录" not in builder_source
    assert ">33 / 33<" not in builder_source
    assert "查看全部 33 条记录" not in builder_source

    assert '<link rel="canonical" href="https://wangzifan.store/">' in html
    assert '<meta property="og:url" content="https://wangzifan.store/">' in html
    assert '<meta property="og:image" content="https://wangzifan.store/assets/og-card.webp">' in html
    assert '<meta property="og:image:type" content="image/webp">' in html
    assert '<meta property="og:image:alt" content="王子凡的个人产品工作台分享图">' in html
    assert 'data-domain="wangzifan.store" src="https://plausible.shipsolo.io/js/script.js"' in html
    graph_match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    assert graph_match is not None
    graph = json.loads(graph_match.group(1))["@graph"]
    assert {node["@type"] for node in graph} == {"Person", "WebSite", "ItemList"}
    release_list = next(node for node in graph if node["@type"] == "ItemList")
    assert release_list["numberOfItems"] == 33
    assert len(release_list["itemListElement"]) == 33
    structured_statuses = [
        item["item"]["additionalProperty"]["value"]
        for item in release_list["itemListElement"]
    ]
    assert structured_statuses.count("live") == 32
    assert structured_statuses.count("offline") == 1

    assert '<link rel="canonical" href="https://wangzifan.store/privacy.html">' in privacy_html
    for social_contract in (
        '<meta property="og:title" content="隐私说明 — ZF Wang">',
        '<meta property="og:url" content="https://wangzifan.store/privacy.html">',
        '<meta property="og:image" content="https://wangzifan.store/assets/og-card.webp">',
        '<meta property="og:image:type" content="image/webp">',
        '<meta property="og:image:alt" content="王子凡的个人产品工作台分享图">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="https://wangzifan.store/assets/og-card.webp">',
    ):
        assert social_contract in privacy_html
    assert "隐私，直接说清楚。" in privacy_html
    assert '<main class="privacy-main" id="privacy-content" tabindex="-1">' in privacy_html
    assert "最近更新：2026-08-28" in privacy_html
    for disclosure in (
        "Plausible Analytics",
        "不设置分析 Cookie",
        "不进行跨站跟踪",
        "GitHub Pages",
        "wang1227928718",
    ):
        assert disclosure in privacy_html
