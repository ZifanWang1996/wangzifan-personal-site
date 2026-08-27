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
    assert sum(project["featured"] for project in projects) == 6
    assert sorted(
        project["featured_order"] for project in projects if project["featured"]
    ) == list(range(1, 7))
    assert all(
        project["featured_order"] is None
        for project in projects
        if not project["featured"]
    )
    assert len({project["category"] for project in projects if project["featured"]}) >= 4

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
    assert "WZF / ONE-PERSON PRODUCT STUDIO" in html
    assert "一个人，把具体问题做成真正能用的产品。" in html
    assert '<span class="title-line">一个人，把具体问题</span>' in html
    assert '<span class="title-line"><em>做成真正能用的产品。</em></span>' in html
    assert '<main id="main-content" tabindex="-1">' in html
    assert 'data-proof="releases">33</strong>' in html
    assert 'data-proof="live">32</strong>' in html
    assert 'data-proof="offline">1</strong>' in html
    for retired in ("WZF PRESS", "LAUNCH CONSOLE", "T-MINUS", "SHIPS LIVE"):
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
    assert html.count('data-featured-card="') == 6
    positions = [html.index(f'data-featured-card="{project["id"]}"') for project in featured]
    assert positions == sorted(positions)
    for project in featured:
        assert project["name"] in html
        assert project["problem"] in html
        assert project["solution"] in html
        assert project["evidence"] in html
        assert f'href="{project["url"]}"' in html
        assert f'src="{project["image"]}"' in html

    assert html.count('target="_blank" rel="noopener noreferrer"') >= 9
    for label in ("问题", "解法", "证据"):
        assert f'>{label}</span>' in html


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

    assert html.count('data-method-step="') == 4
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
    assert "当前离线" in offline_row.group()

    for category in ("all", "ai", "game", "tool", "creative"):
        assert f'data-ledger-filter="{category}"' in html
    assert 'id="ledger-search"' in html
    assert 'id="ledger-status"' in html
    assert 'id="ledger-count" aria-live="polite">33 / 33' in html
    assert 'class="ledger-tools" hidden' in html
    assert 'class="button ledger-more" type="button" id="ledger-more" hidden' in html

    assert html.count('href="#contact"') >= 3
    assert 'src="assets/wechat-qr.webp"' in html
    assert 'class="button copy-button" type="button" hidden' in html
    assert 'alt="王子凡微信二维码，微信号 wang1227928718"' in html
    assert 'data-copy-value="wang1227928718"' in html
    assert "适合讨论" in html and "不承诺" in html
    assert "<canvas" not in html
    assert "requestAnimationFrame" not in html


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
    assert '<meta property="og:image:alt" content="ZF Wang 一人产品工作室发布档案分享图">' in html
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
        '<meta property="og:image:alt" content="ZF Wang 一人产品工作室发布档案分享图">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="https://wangzifan.store/assets/og-card.webp">',
    ):
        assert social_contract in privacy_html
    assert "隐私，直接说清楚。" in privacy_html
    assert '<main class="privacy-main" id="privacy-content" tabindex="-1">' in privacy_html
    assert "最近更新：2026-08-27" in privacy_html
    for disclosure in (
        "Plausible Analytics",
        "不设置分析 Cookie",
        "不进行跨站跟踪",
        "GitHub Pages",
        "wang1227928718",
    ):
        assert disclosure in privacy_html
